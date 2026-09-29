"""Release-boundary regressions, using only disposable local repositories."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

SOURCE = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='swg-package-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'release source with spaces'
        self.env = os.environ.copy()
        for key in list(self.env):
            if key.startswith('GIT_'):
                del self.env[key]
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        SWG_HARNESS_UPDATE_CHECK='0', GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1')
        self.run_ok(['git', 'clone', '--quiet', '--no-hardlinks', str(SOURCE), str(self.repo)])
        self.git('config', 'user.name', 'Package Test')
        self.git('config', 'user.email', 'package-test@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(self.root / 'no-hooks'))
        # Test current tracked implementation, including fixes not yet committed,
        # but establish a clean committed fixture for release-boundary checks.
        tracked = subprocess.check_output(['git', '-C', str(SOURCE), 'ls-files', '-z'],
                                          env=self.env).split(b'\0')
        for raw in filter(None, tracked):
            relative = os.fsdecode(raw)
            source = SOURCE / relative
            target = self.repo / relative
            if target.is_symlink() or target.is_file():
                target.unlink()
            if source.is_symlink():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(os.readlink(source))
            elif source.is_file():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
        self.git('add', '--all')
        self.git('commit', '--quiet', '--allow-empty', '-m', 'Current implementation fixture')

    def run_ok(self, args, cwd=None):
        result = subprocess.run(list(map(str, args)), cwd=cwd, env=self.env,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result.stdout

    def git(self, *args):
        return self.run_ok(['git', '-C', self.repo, *args])

    def package(self):
        return subprocess.run([sys.executable, str(self.repo / 'tools/package.py')],
                              cwd=self.root, env=self.env, capture_output=True,
                              text=True, timeout=30)

    def good_archive(self):
        result = self.package()
        self.assertEqual(result.returncode, 0, result.stderr)
        return Path(result.stdout.strip())

    def test_repeat_packaging_is_byte_reproducible_and_checksum_matches(self):
        archive = self.good_archive()
        first = archive.read_bytes()
        self.good_archive()
        self.assertEqual(first, archive.read_bytes())
        checksum = archive.with_suffix('.zip.sha256').read_text().split()[0]
        self.assertEqual(checksum, hashlib.sha256(first).hexdigest())

    def test_untracked_and_ignored_private_files_are_excluded(self):
        (self.repo / 'private-note.txt').write_text('private fixture text')
        (self.repo / '.git/info/exclude').write_text('ignored-secret.txt\n')
        (self.repo / 'ignored-secret.txt').write_text('private fixture credential')
        with zipfile.ZipFile(self.good_archive()) as z:
            names = z.namelist()
            self.assertFalse(any('/.git/' in n for n in names))
            self.assertFalse(any(n.endswith(('private-note.txt', 'ignored-secret.txt')) for n in names))

    def test_unstaged_tracked_edits_cannot_silently_reuse_release_identity(self):
        self.good_archive()
        with (self.repo / 'README.md').open('a') as f:
            f.write('\nUNREVIEWED LOCAL CONTENT\n')
        self.assertNotEqual(self.package().returncode, 0,
                            'A versioned release must reject dirty tracked inputs, not silently replace it.')

    def test_staged_tracked_edits_cannot_silently_reuse_release_identity(self):
        (self.repo / 'README.md').write_text('Uncommitted staged release content\n')
        self.git('add', 'README.md')
        self.assertNotEqual(self.package().returncode, 0,
                            'Staged content is still not a committed release revision.')

    def test_failed_packaging_preserves_existing_archive_and_checksum(self):
        archive = self.good_archive()
        before = archive.read_bytes()
        checksum = archive.with_suffix('.zip.sha256').read_bytes()
        target = self.root / 'private.txt'
        target.write_text('synthetic private fixture')
        try:
            (self.repo / '00-private-link').symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        self.git('add', '00-private-link')
        self.git('commit', '--quiet', '-m', 'Unsupported linked release entry')
        self.assertNotEqual(self.package().returncode, 0)
        self.assertEqual(archive.read_bytes(), before,
                         'A failed package replaced a prior valid ZIP with a partial ZIP.')
        self.assertEqual(archive.with_suffix('.zip.sha256').read_bytes(), checksum)

    def test_symlink_parent_cannot_include_external_tracked_path_contents(self):
        outside = self.root / 'external-docs'
        shutil.copytree(self.repo / 'docs', outside)
        marker = b'SYNTHETIC PRIVATE FILE OUTSIDE RELEASE ROOT'
        (outside / 'README.md').write_bytes(marker)
        shutil.rmtree(self.repo / 'docs')
        try:
            (self.repo / 'docs').symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        result = self.package()
        self.assertNotEqual(result.returncode, 0,
                            'Checking only the leaf symlink permits external parent traversal.')

    def test_extracted_zip_supports_newcomer_cli_without_harness_git_history(self):
        archive = self.good_archive()
        extracted = self.root / 'unpacked folder'
        with zipfile.ZipFile(archive) as z:
            z.extractall(extracted)
        package_root = next(extracted.iterdir())
        self.assertFalse((package_root / '.git').exists())
        cli = package_root / 'harness.py'
        self.run_ok([sys.executable, cli, '--help'], cwd=self.root)
        workspace = self.root / 'new contributor workspace'
        workspace.mkdir()
        self.run_ok(['git', 'init', '--quiet', workspace])
        self.run_ok(['git', '-C', workspace, 'config', 'user.name', 'Fixture'])
        self.run_ok(['git', '-C', workspace, 'config', 'user.email', 'fixture@example.invalid'])
        (workspace / 'sample.txt').write_text('baseline\n')
        self.run_ok(['git', '-C', workspace, 'add', 'sample.txt'])
        self.run_ok(['git', '-C', workspace, '-c', 'commit.gpgsign=false', 'commit', '--quiet', '-m', 'Baseline'])
        task = self.root / 'new task.json'
        self.run_ok([sys.executable, cli, 'inspect', '--workspace', workspace], cwd=self.root)
        self.run_ok([sys.executable, cli, 'init', '--workspace', workspace, '--output', task], cwd=self.root)
        self.assertTrue(json.loads(task.read_text())['base'])
        (workspace / 'sample.txt').write_text('updated behavior\n')
        self.run_ok(['git', '-C', workspace, 'add', 'sample.txt'])
        self.run_ok(['git', '-C', workspace, '-c', 'commit.gpgsign=false', 'commit', '--quiet', '-m', 'Update'])
        head = self.run_ok(['git', '-C', workspace, 'rev-parse', 'HEAD']).strip()
        evidence = self.root / 'evidence.txt'
        evidence.write_text('Observed updated fixture behavior\n')
        record = json.loads(task.read_text())
        record.update(repository='example/disposable', goal='Update fixture behavior',
                      expected_behavior='Updated fixture', environment='Disposable repository',
                      ai_contribution='No generative AI', ai_pr_text='No generative AI')
        record['checks'] = [{'name': 'Inspect fixture', 'command_or_steps': 'Read sample.txt',
                             'expected': 'updated behavior', 'observed': 'updated behavior',
                             'status': 'passed', 'tested_commit': head,
                             'evidence': {'path': str(evidence),
                                          'sha256': hashlib.sha256(evidence.read_bytes()).hexdigest()}}]
        task.write_text(json.dumps(record))
        report = self.root / 'report.json'
        self.run_ok([sys.executable, cli, 'check', '--workspace', workspace,
                     '--task', task, '--output', report], cwd=self.root)
        self.run_ok([sys.executable, cli, 'verify', '--workspace', workspace,
                     '--report', report], cwd=self.root)

    def test_packaged_docs_have_resolvable_relative_links_and_no_home_paths(self):
        with zipfile.ZipFile(self.good_archive()) as z:
            names = set(z.namelist())
            for name in sorted(names):
                if not name.endswith('.md'):
                    continue
                text = z.read(name).decode('utf-8')
                self.assertNotIn('/home/akilleez/', text, name)
                for link in re.findall(r'\]\(([^)]+)\)', text):
                    if '://' in link or link.startswith('#') or link.startswith('mailto:'):
                        continue
                    path = link.split('#')[0]
                    if not path:
                        continue
                    resolved = os.path.normpath(str(Path(name).parent / path)).replace(os.sep, '/')
                    self.assertIn(resolved, names, f'{name}: missing packaged link {link}')


if __name__ == '__main__':
    unittest.main()
