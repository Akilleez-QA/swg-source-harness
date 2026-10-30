"""Ensure the shipped skill matches its explicit provenance inventory."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


class SkillBundleTests(unittest.TestCase):
    def test_validator_reads_utf8_with_cp1252_default(self):
        spec = importlib.util.spec_from_file_location(
            'validate_skill', ROOT / 'skills/poodo/scripts/validate_skill.py')
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        read_text = Path.read_text

        def windows_read_text(path, encoding=None, errors=None):
            return read_text(path, encoding=encoding or 'cp1252', errors=errors)

        with mock.patch.object(Path, 'read_text', windows_read_text):
            self.assertEqual(validator.main(), 0)

    def test_vendored_files_match_manifest(self):
        manifest = json.loads((ROOT / 'skills/poodo-source-manifest.json').read_text())
        base = ROOT / 'skills/poodo'
        actual = {str(p.relative_to(base)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
        self.assertEqual(actual, manifest['bundled_files'])
        for path, digest in manifest['upstream_files'].items():
            if actual[path] != digest:
                self.assertIn(path, manifest['adaptations'])

    def test_skill_is_explicit_and_has_setup(self):
        metadata = (ROOT / 'skills/poodo/agents/openai.yaml').read_text()
        self.assertIn('allow_implicit_invocation: false', metadata)
        self.assertTrue((ROOT / 'skills/poodo/README.md').is_file())
        self.assertTrue((ROOT / 'skills/poodo/requirements.txt').is_file())
