"""Adversarial public-CLI inputs; fixtures never leave disposable local repos.

Checksums are deliberately recomputed when testing report schema validation.
This is NOT an authentication/forgery test: unsigned reports are forgeable by design.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

import test_harness as fixtures


class AdversarialInputsTests(unittest.TestCase):
    setUp = fixtures.HarnessCLITests.setUp
    git = fixtures.HarnessCLITests.git
    cli = fixtures.HarnessCLITests.cli
    read = fixtures.HarnessCLITests.read
    write = fixtures.HarnessCLITests.write
    prepare_candidate = fixtures.HarnessCLITests.prepare_candidate
    make_report = fixtures.HarnessCLITests.make_report

    def raw_cli(self, command, *args):
        return subprocess.run(
            [sys.executable, str(fixtures.HARNESS), command,
             '--workspace', str(self.repo), *map(str, args)],
            capture_output=True, text=True, env=self.env, timeout=10)

    def rewrite_report(self, report):
        report.pop('integrity_sha256', None)
        encoded = json.dumps(report, sort_keys=True, separators=(',', ':'),
                             ensure_ascii=True).encode()
        report['integrity_sha256'] = hashlib.sha256(encoded).hexdigest()
        self.write(self.report_path, report)

    def test_verify_rejects_missing_required_report_fields(self):
        original = self.make_report()
        for field in ('base', 'changed_paths', 'task_digest', 'evidence',
                      'harness_version', 'created_at', 'verification_boundary'):
            with self.subTest(field=field):
                report = dict(original)
                del report[field]
                self.rewrite_report(report)
                result = self.raw_cli('verify', '--report', self.report_path)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_verify_rejects_wrong_report_field_types(self):
        original = self.make_report()
        for field, value in (('base', []), ('changed_paths', 'feature.txt'),
                             ('task_digest', 42), ('evidence', {}),
                             ('harness_version', []), ('created_at', None)):
            with self.subTest(field=field):
                report = dict(original)
                report[field] = value
                self.rewrite_report(report)
                result = self.raw_cli('verify', '--report', self.report_path)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_complete_report_requires_nonempty_evidence_and_changes(self):
        original = self.make_report()
        for field in ('evidence', 'changed_paths'):
            with self.subTest(field=field):
                report = dict(original)
                report[field] = []
                self.rewrite_report(report)
                result = self.raw_cli('verify', '--report', self.report_path)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_verify_rejects_malformed_evidence_records(self):
        original = self.make_report()
        invalid = [None, {}, {'check': 'test', 'sha256': 'not-a-digest',
                              'origin': 'contributor-supplied'},
                   {'check': [], 'sha256': '0' * 64,
                    'origin': 'contributor-supplied'}]
        for record in invalid:
            with self.subTest(record=record):
                report = dict(original)
                report['evidence'] = [record]
                self.rewrite_report(report)
                result = self.raw_cli('verify', '--report', self.report_path)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_malformed_task_json_has_controlled_error(self):
        for content in (b'{', b'[]', b'null', b'\xff',
                        b'[' * 1500 + b'0' + b']' * 1500):
            with self.subTest(content=content[:30]):
                self.task_path.write_bytes(content)
                result = self.raw_cli('check', '--task', self.task_path,
                                      '--output', self.report_path)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse(self.report_path.exists())

    def test_invalid_evidence_shapes_remain_incomplete(self):
        original = self.prepare_candidate()
        variants = [None, [], {}, {'path': 12, 'sha256': '0' * 64},
                    {'path': 'relative.log', 'sha256': '0' * 64},
                    {'path': str(self.evidence_path), 'sha256': []}]
        for index, evidence in enumerate(variants):
            with self.subTest(evidence=evidence):
                task = json.loads(json.dumps(original))
                task['checks'][0]['evidence'] = evidence
                self.write(self.task_path, task)
                result = self.raw_cli('check', '--task', self.task_path,
                                      '--output', self.root / ('bad-%d.json' % index))
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertNotIn('Traceback', result.stderr)

    def test_symlink_evidence_is_rejected(self):
        task = self.prepare_candidate()
        link = self.root / 'linked-evidence'
        try:
            link.symlink_to(self.evidence_path)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        task['checks'][0]['evidence']['path'] = str(link)
        self.write(self.task_path, task)
        self.cli('check', '--task', self.task_path, '--output', self.report_path,
                 expected=1)
        self.assertEqual(self.read(self.report_path)['evidence'], [])

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFO requires POSIX')
    def test_fifo_evidence_is_rejected_without_blocking(self):
        task = self.prepare_candidate()
        fifo = self.root / 'evidence.pipe'
        os.mkfifo(fifo)
        task['checks'][0]['evidence']['path'] = str(fifo)
        self.write(self.task_path, task)
        result = self.raw_cli('check', '--task', self.task_path,
                              '--output', self.report_path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(self.read(self.report_path)['evidence'], [])

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFO requires POSIX')
    def test_fifo_json_inputs_return_error_without_waiting_for_writer(self):
        fifo = self.root / 'input.pipe'
        os.mkfifo(fifo)
        for command, arguments in (
                ('check', ['--task', fifo, '--output', self.report_path]),
                ('verify', ['--report', fifo])):
            with self.subTest(command=command):
                try:
                    result = subprocess.run(
                        [sys.executable, str(fixtures.HARNESS), command,
                         '--workspace', str(self.repo), *map(str, arguments)],
                        capture_output=True, text=True, env=self.env, timeout=2)
                except subprocess.TimeoutExpired:
                    self.fail('JSON reader blocked opening a FIFO with no writer')
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertNotIn('Traceback', result.stderr)

    def test_report_does_not_copy_private_task_or_log_contents(self):
        task = self.prepare_candidate()
        secret = 'PRIVATE_FIXTURE_VALUE_DO_NOT_PUBLISH_43728'
        self.evidence_path.write_text(secret)
        task['environment'] = secret
        task['checks'][0]['command_or_steps'] = secret
        task['checks'][0]['observed'] = secret
        task['checks'][0]['evidence']['sha256'] = hashlib.sha256(
            self.evidence_path.read_bytes()).hexdigest()
        self.write(self.task_path, task)
        result = self.cli('check', '--task', self.task_path, '--output', self.report_path)
        self.assertNotIn(secret, self.report_path.read_text() + result.stdout + result.stderr)
        self.assertNotIn(str(self.evidence_path), self.report_path.read_text())


if __name__ == '__main__':
    unittest.main()
