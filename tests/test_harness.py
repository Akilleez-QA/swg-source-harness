"""Exercise the public CLI against disposable repositories and evidence files."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HARNESS = Path(__file__).resolve().parents[1] / 'harness.py'


class HarnessCLITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='swg-harness-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.env = os.environ.copy()
        # A developer's Git signing/hooks/configuration must not affect fixtures.
        for key in list(self.env):
            if key.startswith('GIT_'):
                del self.env[key]
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        SWG_HARNESS_UPDATE_CHECK='0', GIT_TERMINAL_PROMPT='0')
        self.git('init', '--quiet')
        self.git('config', 'user.name', 'Harness Test')
        self.git('config', 'user.email', 'harness-test@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(self.root / 'no-hooks'))
        self.source = self.repo / 'feature.txt'
        self.source.write_text('original behavior\n', encoding='utf-8')
        self.git('add', 'feature.txt')
        self.git('commit', '--quiet', '-m', 'Baseline')
        self.base = self.git('rev-parse', 'HEAD').strip()
        self.task_path = self.root / 'task.json'
        self.report_path = self.root / 'report.json'
        self.evidence_path = self.root / 'evidence.txt'

    def git(self, *args):
        result = subprocess.run(['git', '-C', str(self.repo), *args],
                                capture_output=True, text=True, env=self.env, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def cli(self, command, *args, expected=0):
        result = subprocess.run([sys.executable, str(HARNESS), command,
                                 '--workspace', str(self.repo), *map(str, args)],
                                capture_output=True, text=True, env=self.env, timeout=30)
        self.assertEqual(result.returncode, expected,
                         'stdout:\n%s\nstderr:\n%s' % (result.stdout, result.stderr))
        return result

    def read(self, path):
        return json.loads(path.read_text(encoding='utf-8'))

    def write(self, path, value):
        path.write_text(json.dumps(value), encoding='utf-8')

    def prepare_candidate(self):
        self.cli('init', '--output', self.task_path)
        self.source.write_text('corrected behavior\n', encoding='utf-8')
        self.git('add', 'feature.txt')
        self.git('commit', '--quiet', '-m', 'Correct feature behavior')
        self.head = self.git('rev-parse', 'HEAD').strip()
        self.evidence_path.write_text('Private local log: actual corrected behavior observed.\n',
                                      encoding='utf-8')
        task = self.read(self.task_path)
        task.update(repository='example/swgs-test', goal='Correct the feature',
                    expected_behavior='Feature returns the corrected result',
                    environment='Disposable local test fixture',
                    ai_contribution='AI authored code; contributor inspected and tested it',
                    ai_pr_text='AI helped draft the description')
        task['checks'] = [{
            'name': 'Feature behavior',
            'command_or_steps': 'Exercise feature with the documented fixture input',
            'expected': 'Corrected result', 'observed': 'Corrected result',
            'status': 'passed', 'tested_commit': self.head,
            'evidence': {'path': str(self.evidence_path),
                         'sha256': hashlib.sha256(self.evidence_path.read_bytes()).hexdigest()}}]
        self.write(self.task_path, task)
        return task

    def make_report(self):
        self.prepare_candidate()
        self.cli('check', '--task', self.task_path, '--output', self.report_path)
        return self.read(self.report_path)

    def test_symlink_evidence_is_rejected(self):
        task = self.prepare_candidate()
        link = self.root / 'evidence-link.txt'
        try:
            link.symlink_to(self.evidence_path)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        task['checks'][0]['evidence']['path'] = str(link)
        self.write(self.task_path, task)
        self.cli('check', '--task', self.task_path, '--output', self.report_path, expected=1)
        self.assertTrue(any('unavailable' in p for p in self.read(self.report_path)['problems']))

    def test_malformed_task_and_large_input_fail_cleanly(self):
        self.write(self.task_path, [])
        self.cli('check', '--task', self.task_path, '--output', self.report_path, expected=2)
        self.task_path.write_bytes(b' ' * (2 * 1024 * 1024 + 1))
        self.cli('check', '--task', self.task_path, '--output', self.report_path, expected=2)

    def test_verify_incomplete_report_is_not_success(self):
        task = self.prepare_candidate()
        task['checks'][0]['status'] = 'failed'
        self.write(self.task_path, task)
        self.cli('check', '--task', self.task_path, '--output', self.report_path, expected=1)
        result = self.cli('verify', '--report', self.report_path, expected=1)
        self.assertIn('incomplete', result.stdout)

    def test_relative_evidence_path_is_rejected(self):
        task = self.prepare_candidate()
        task['checks'][0]['evidence']['path'] = 'README.md'
        self.write(self.task_path, task)
        self.cli('check', '--task', self.task_path, '--output', self.report_path, expected=1)
        self.assertTrue(any('absolute' in p for p in self.read(self.report_path)['problems']))

    def test_update_command_needs_no_workspace_and_respects_disable(self):
        result = subprocess.run([sys.executable, str(HARNESS), 'updates', '--force'],
                                capture_output=True, text=True, env=self.env, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('No update notice', result.stdout)

    def test_init_records_baseline_but_does_not_invent_validation(self):
        self.cli('init', '--output', self.task_path)
        task = self.read(self.task_path)
        self.assertEqual(task['schema'], 'swg-task/v1')
        self.assertEqual(task['base'], self.base)
        self.assertFalse(task['change_review']['required'])
        self.assertEqual(task['change_review']['affected_surfaces'], [])
        self.assertEqual(task['change_review']['companion_revisions'], [])
        self.assertEqual(task['checks'][0]['status'], 'not-run')
        self.assertEqual(task['checks'][0]['tested_commit'], '')
        self.assertEqual(self.git('status', '--porcelain'), '')

    def test_change_review_is_optional_and_conditionally_complete(self):
        task = self.prepare_candidate()
        legacy = dict(task)
        del legacy['change_review']
        self.write(self.task_path, legacy)
        self.cli('check', '--task', self.task_path,
                 '--output', self.root / 'legacy-report.json')

        task['change_review']['required'] = True
        self.write(self.task_path, task)
        incomplete = self.root / 'incomplete-review.json'
        self.cli('check', '--task', self.task_path, '--output', incomplete, expected=1)
        problems = self.read(incomplete)['problems']
        self.assertIn('Complete change_review field: scope', problems)
        self.assertIn('List at least one affected surface in change_review.', problems)

        task['change_review'].update(
            scope='Update the feature behavior only',
            preserved_behavior='Keep the existing neighboring path unchanged',
            affected_surfaces=['script/game-logic'],
            companion_revisions=[],
            owner_and_integration='Existing feature owner and event path',
            precedents_and_alternatives='Compared the neighboring event path; no parallel manager',
            risks_and_unknowns='No remaining material unknowns in this fixture',
            player_visible_effects='Corrected result; no timing or feedback change',
            final_diff_notes='Final diff matches the selected owner and preservation boundary')
        self.write(self.task_path, task)
        self.cli('check', '--task', self.task_path,
                 '--output', self.root / 'complete-review.json')

    def test_unfilled_template_reports_missing_information(self):
        self.cli('init', '--output', self.task_path)
        self.cli('check', '--task', self.task_path, '--output', self.report_path, expected=1)
        report = self.read(self.report_path)
        self.assertEqual(report['local_status'], 'needs-information')
        self.assertFalse(report['review_eligible'])
        self.assertIn('Complete task field: goal', report['problems'])
        self.assertIn('No committed changes relative to base.', report['problems'])
        self.assertTrue(any('not reported passed' in p for p in report['problems']))

    def test_complete_report_remains_unsigned_local_evidence(self):
        report = self.make_report()
        self.assertEqual(report['local_status'], 'preflight-complete')
        self.assertEqual(report['problems'], [])
        self.assertFalse(report['review_eligible'])
        self.assertFalse(report['signed'])
        self.assertEqual(report['candidate']['head'], self.head)
        self.assertEqual(report['base'], self.base)
        self.assertEqual(report['changed_paths'], ['feature.txt'])
        serialized = self.report_path.read_text()
        self.assertNotIn(str(self.evidence_path), serialized)
        self.assertNotIn('Private local log', serialized)
        result = self.cli('verify', '--report', self.report_path)
        self.assertIn('Not a signature', result.stdout)

    def test_wrong_evidence_hash_is_not_a_pass(self):
        task = self.prepare_candidate()
        task['checks'][0]['evidence']['sha256'] = '0' * 64
        self.write(self.task_path, task)
        self.cli('check', '--task', self.task_path, '--output', self.report_path, expected=1)
        report = self.read(self.report_path)
        self.assertEqual(report['local_status'], 'needs-information')
        self.assertTrue(any('digest does not match' in p for p in report['problems']))

    def test_check_result_bound_to_different_commit_is_rejected(self):
        task = self.prepare_candidate()
        task['checks'][0]['tested_commit'] = self.base
        self.write(self.task_path, task)
        self.cli('check', '--task', self.task_path, '--output', self.report_path, expected=1)
        self.assertTrue(any('not bound to candidate HEAD' in p
                            for p in self.read(self.report_path)['problems']))

    def test_tampered_report_fails_integrity(self):
        report = self.make_report()
        report['changed_paths'] = ['an-unrelated-file']
        self.write(self.report_path, report)
        result = self.cli('verify', '--report', self.report_path, expected=2)
        self.assertIn('integrity mismatch', result.stderr)

    def test_recomputed_checksum_cannot_claim_trusted_eligibility(self):
        report = self.make_report()
        report.pop('integrity_sha256')
        report['review_eligible'] = True
        canonical = json.dumps(report, sort_keys=True, separators=(',', ':'),
                               ensure_ascii=True).encode()
        report['integrity_sha256'] = hashlib.sha256(canonical).hexdigest()
        self.write(self.report_path, report)
        result = self.cli('verify', '--report', self.report_path, expected=2)
        self.assertIn('cannot assert trusted review eligibility', result.stderr)

    def test_new_commit_invalidates_report_even_with_unchanged_tree(self):
        self.make_report()
        self.git('commit', '--quiet', '--allow-empty', '-m', 'New candidate identity')
        result = self.cli('verify', '--report', self.report_path, expected=2)
        self.assertIn('stale', result.stderr)

    def test_dirty_tracked_file_invalidates_report(self):
        self.make_report()
        self.source.write_text('uncommitted replacement\n')
        result = self.cli('verify', '--report', self.report_path, expected=2)
        self.assertIn('dirty', result.stderr)

    def test_untracked_file_invalidates_report(self):
        self.make_report()
        (self.repo / 'new-source.txt').write_text('uncommitted input\n')
        result = self.cli('verify', '--report', self.report_path, expected=2)
        self.assertIn('dirty', result.stderr)

    def test_existing_task_and_report_outputs_are_not_overwritten(self):
        self.make_report()
        original_task = self.task_path.read_bytes()
        original_report = self.report_path.read_bytes()
        self.cli('init', '--output', self.task_path, expected=2)
        self.cli('check', '--task', self.task_path, '--output', self.report_path, expected=2)
        self.assertEqual(self.task_path.read_bytes(), original_task)
        self.assertEqual(self.report_path.read_bytes(), original_report)

    def test_output_inside_workspace_is_refused(self):
        output = self.repo / 'task.json'
        result = self.cli('init', '--output', output, expected=2)
        self.assertIn('outside', result.stderr)
        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
