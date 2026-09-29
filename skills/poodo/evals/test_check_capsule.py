#!/usr/bin/env python3

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_capsule.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


class CapsuleLinterTests(unittest.TestCase):
    def run_fixture(self, name: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / name)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_valid_capsule(self) -> None:
        result = self.run_fixture("valid-capsule.yaml")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("epistemic and behavioral correctness remain untested", result.stdout)

    def test_rejects_failed_prediction_resurrection(self) -> None:
        result = self.run_fixture("invalid-resurrection.yaml")
        self.assertEqual(result.returncode, 1)
        self.assertIn("terminal prediction was resurrected", result.stderr)

    def test_rejects_truncated_evidence(self) -> None:
        result = self.run_fixture("invalid-truncated-evidence.yaml")
        self.assertEqual(result.returncode, 1)
        self.assertIn("partial or truncated evidence", result.stderr)


if __name__ == "__main__":
    unittest.main()
