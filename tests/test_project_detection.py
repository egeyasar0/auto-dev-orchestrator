from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from auto_dev.repo.inspect import detect_project_types, infer_test_commands


class ProjectDetectionTests(unittest.TestCase):
    def test_detects_python(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("", encoding="utf-8")
            self.assertEqual(detect_project_types(root), ["python"])

    def test_infers_unittest_for_python_tests(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tests").mkdir()
            self.assertEqual(infer_test_commands(root, ["python"]), [["python", "-m", "unittest", "discover"]])


if __name__ == "__main__":
    unittest.main()

