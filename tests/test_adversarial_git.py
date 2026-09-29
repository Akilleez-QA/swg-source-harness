"""Public-CLI Git edge cases, using only disposable local repositories."""
import subprocess
import sys
import unittest

import test_harness as helpers


class AdversarialGitTests(unittest.TestCase):
    # Reuse fixture helpers without inheriting and duplicating the baseline tests.
    setUp = helpers.HarnessCLITests.setUp
    git = helpers.HarnessCLITests.git
    cli = helpers.HarnessCLITests.cli
    read = helpers.HarnessCLITests.read
    write = helpers.HarnessCLITests.write
    prepare_candidate = helpers.HarnessCLITests.prepare_candidate
    make_report = helpers.HarnessCLITests.make_report

    def run_cli(self, command, workspace=None, *args):
        return subprocess.run(
            [sys.executable, str(helpers.HARNESS), command, '--workspace',
             str(workspace or self.repo), *map(str, args)],
            capture_output=True, text=True, env=self.env, timeout=30)

    def git_at(self, path, *args):
        result = subprocess.run(['git', '-C', str(path), *args],
                                capture_output=True, text=True, env=self.env, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def create_repo(self, name):
        path = self.root / name
        path.mkdir()
        self.git_at(path, 'init', '--quiet')
        self.git_at(path, 'config', 'user.name', 'Fixture')
        self.git_at(path, 'config', 'user.email', 'fixture@example.invalid')
        self.git_at(path, 'config', 'commit.gpgsign', 'false')
        self.git_at(path, 'config', 'core.hooksPath', str(self.root / 'no-hooks'))
        (path / 'nested.txt').write_text('nested original\n')
        self.git_at(path, 'add', '.')
        self.git_at(path, 'commit', '--quiet', '-m', 'Initial nested commit')
        return path

    def add_submodule(self, nested=False):
        child = self.create_repo('child-source')
        if nested:
            leaf = self.create_repo('leaf-source')
            self.git_at(child, '-c', 'protocol.file.allow=always', 'submodule',
                        'add', '--quiet', str(leaf), 'leaf')
            self.git_at(child, 'commit', '--quiet', '-am', 'Add leaf')
        self.git('-c', 'protocol.file.allow=always', 'submodule', 'add',
                 '--quiet', str(child), 'dependency')
        if nested:
            self.git('-c', 'protocol.file.allow=always', 'submodule', 'update',
                     '--init', '--recursive')
        self.git('commit', '--quiet', '-am', 'Add dependency')
        return self.repo / 'dependency'

    def test_linked_worktree_accepts_clean_candidate_without_cross_checkout_confusion(self):
        self.prepare_candidate()
        linked = self.root / 'linked-worktree'
        self.git('worktree', 'add', '--detach', '--quiet', str(linked), self.head)
        # Unrelated main checkout dirt must not taint the selected worktree.
        self.source.write_text('main checkout changed independently\n')
        result = self.run_cli('check', linked, '--task', self.task_path,
                              '--output', self.report_path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = self.read(self.report_path)
        self.assertEqual(report['candidate']['head'], self.head)
        self.assertTrue(report['candidate']['clean'])
        self.assertFalse(report['review_eligible'])
        result = self.run_cli('verify', linked, '--report', self.report_path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unborn_head_fails_without_traceback(self):
        empty = self.root / 'empty'
        empty.mkdir()
        self.git_at(empty, 'init', '--quiet')
        result = self.run_cli('inspect', empty)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)

    def test_subdirectory_refused_even_when_git_can_find_parent(self):
        subdir = self.repo / 'directory'
        subdir.mkdir()
        result = self.run_cli('inspect', subdir)
        self.assertEqual(result.returncode, 2)
        self.assertIn('repository root', result.stderr)

    def test_moving_base_ref_cannot_stand_in_for_pinned_commit(self):
        task = self.prepare_candidate()
        task['base'] = 'HEAD~1'
        self.write(self.task_path, task)
        result = self.run_cli('check', None, '--task', self.task_path,
                              '--output', self.report_path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertTrue(any('full lowercase Git commit ID' in p
                            for p in self.read(self.report_path)['problems']))

    def test_unrelated_base_is_an_explicit_two_endpoint_comparison(self):
        # v0.1 promises comparison with a supplied commit, not ancestry policy.
        # Preserve this distinction rather than pretending it validates PR lineage.
        task = self.prepare_candidate()
        tree = self.git('rev-parse', self.base + '^{tree}').strip()
        unrelated = self.git('commit-tree', tree, '-m', 'Independent root').strip()
        task['base'] = unrelated
        self.write(self.task_path, task)
        self.cli('check', '--task', self.task_path, '--output', self.report_path)
        report = self.read(self.report_path)
        self.assertEqual(report['base'], unrelated)
        self.assertEqual(report['changed_paths'], ['feature.txt'])
        self.assertFalse(report['review_eligible'])

    def test_uninitialized_submodule_blocks_preflight(self):
        self.add_submodule()
        self.prepare_candidate()
        self.git('submodule', 'deinit', '--force', 'dependency')
        result = self.run_cli('check', None, '--task', self.task_path,
                              '--output', self.report_path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertTrue(any('Initialize submodules' in p
                            for p in self.read(self.report_path)['problems']))

    def test_mismatched_submodule_commit_blocks_preflight(self):
        dep = self.add_submodule()
        self.prepare_candidate()
        self.git_at(dep, '-c', 'user.name=Fixture',
                    '-c', 'user.email=fixture@example.invalid',
                    '-c', 'commit.gpgsign=false', 'commit', '--quiet',
                    '--allow-empty', '-m', 'Unrecorded dependency revision')
        result = self.run_cli('check', None, '--task', self.task_path,
                              '--output', self.report_path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertTrue(any('pinned revisions' in p
                            for p in self.read(self.report_path)['problems']))

    def test_nested_submodule_dirt_cannot_be_hidden_by_ignore_config(self):
        dep = self.add_submodule(nested=True)
        self.make_report()
        self.git('config', 'submodule.dependency.ignore', 'all')
        self.git_at(dep, 'config', 'submodule.leaf.ignore', 'all')
        (dep / 'leaf' / 'nested.txt').write_text('uncommitted nested change\n')
        result = self.run_cli('verify', None, '--report', self.report_path)
        self.assertNotEqual(result.returncode, 0,
                            'Nested modified source was accepted as the clean candidate')

    def test_assume_unchanged_modified_source_does_not_verify_clean(self):
        self.make_report()
        self.git('update-index', '--assume-unchanged', 'feature.txt')
        self.source.write_text('different tracked bytes than tested commit\n')
        # This ordinary Git optimization can outlive a previous workflow.
        self.assertEqual(self.git('status', '--porcelain'), '')
        flags_before = self.git('ls-files', '-v')
        result = self.run_cli('verify', None, '--report', self.report_path)
        self.assertEqual(self.git('ls-files', '-v'), flags_before,
                         'Read-only inspection must not clear contributor index flags')
        self.assertNotEqual(result.returncode, 0,
                            'Changed tracked source hidden by assume-unchanged verified clean')

    def test_skip_worktree_modified_source_cannot_complete_preflight(self):
        self.prepare_candidate()
        self.git('update-index', '--skip-worktree', 'feature.txt')
        self.source.write_text('different tracked bytes than tested commit\n')
        self.assertEqual(self.git('status', '--porcelain'), '')
        flags_before = self.git('ls-files', '-v')
        result = self.run_cli('check', None, '--task', self.task_path,
                              '--output', self.report_path)
        self.assertEqual(self.git('ls-files', '-v'), flags_before,
                         'Read-only inspection must not clear contributor index flags')
        self.assertNotEqual(result.returncode, 0,
                            'Changed tracked source hidden by skip-worktree passed preflight')


if __name__ == '__main__':
    unittest.main()
