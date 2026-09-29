"""Additional independent contract checks for strict parsing and source binding."""
import json
import unittest
import test_harness as fixtures
import test_adversarial_inputs as inputs


class ReportContractTests(unittest.TestCase):
    setUp = fixtures.HarnessCLITests.setUp
    git = fixtures.HarnessCLITests.git
    cli = fixtures.HarnessCLITests.cli
    read = fixtures.HarnessCLITests.read
    write = fixtures.HarnessCLITests.write
    prepare_candidate = fixtures.HarnessCLITests.prepare_candidate
    make_report = fixtures.HarnessCLITests.make_report
    rewrite_report = inputs.AdversarialInputsTests.rewrite_report

    def test_duplicate_fields_and_nonfinite_numbers_rejected(self):
        for raw in ('{"schema":"wrong","schema":"swg-task/v1"}', '{"value":NaN}', '{"value":Infinity}', '{"value":1e999}'):
            self.task_path.write_text(raw)
            result = self.cli('check', '--task', self.task_path, '--output', self.report_path, expected=2)
            self.assertNotIn('Traceback', result.stderr)

    def test_rehashed_changed_paths_still_must_match_git(self):
        report = self.make_report()
        report['changed_paths'] = ['different.txt']
        self.rewrite_report(report)
        result = self.cli('verify', '--report', self.report_path, expected=2)
        self.assertIn('do not match', result.stderr)

    def test_same_report_stays_unsigned_after_narrative_change(self):
        # A deliberate negative control: checksums cannot authenticate narrative.
        report = self.make_report()
        report['verification_boundary'] = 'A different contributor claim'
        self.rewrite_report(report)
        self.cli('verify', '--report', self.report_path)
        self.assertFalse(report['review_eligible'])
        self.assertFalse(report['signed'])
