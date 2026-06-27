from __future__ import annotations

import io
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from auto_dev.cli import main
from auto_dev.models import RepoContext


class CliTests(unittest.TestCase):
    def test_plan_returns_nonzero_when_blocked(self) -> None:
        with patch("auto_dev.cli.run_plan", return_value=(None, "", "BLOCKED: provider command failed.")):
            self.assertEqual(main(["plan", "test task"]), 2)

    def test_run_stops_before_implementation_when_plan_blocked(self) -> None:
        context = RepoContext(
            root=Path.cwd(),
            has_git=True,
            branch="test",
            dirty_files=[],
            config_exists=False,
            project_types=["python"],
            test_commands=[],
        )
        with (
            patch("auto_dev.cli.run_plan", return_value=(None, "", "BLOCKED: provider command failed.")),
            patch("auto_dev.cli.inspect_repo", return_value=context),
            patch("auto_dev.cli.provider") as provider,
            redirect_stderr(io.StringIO()),
        ):
            self.assertEqual(main(["run", "test task"]), 2)
            provider.assert_not_called()


if __name__ == "__main__":
    unittest.main()
