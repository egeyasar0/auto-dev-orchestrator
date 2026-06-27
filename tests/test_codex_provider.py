from __future__ import annotations

import unittest
from pathlib import Path

from auto_dev.models import CodexConfig
from auto_dev.providers.codex import CodexProvider


class CodexProviderTests(unittest.TestCase):
    def test_builds_read_only_plan_command(self) -> None:
        provider = CodexProvider(CodexConfig(model="gpt-test", reasoning_effort_config_key="reasoning.effort"))
        command = provider.build_command(Path("repo"), Path("out.md"), "high", "read-only")
        self.assertIn("codex", command)
        self.assertIn("exec", command)
        self.assertIn("gpt-test", command)
        self.assertIn("read-only", command)
        self.assertIn('reasoning.effort="high"', command)

    def test_omits_model_when_not_configured(self) -> None:
        provider = CodexProvider(CodexConfig())
        command = provider.build_command(Path("repo"), Path("out.md"), "medium", "read-only")
        self.assertNotIn("--model", command)

    def test_plan_can_skip_git_repo_check(self) -> None:
        provider = CodexProvider(CodexConfig())
        command = provider.build_command(
            Path("repo"), Path("out.md"), "medium", "read-only", skip_git_repo_check=True
        )
        self.assertIn("--skip-git-repo-check", command)

    def test_builds_workspace_write_command(self) -> None:
        provider = CodexProvider(CodexConfig())
        command = provider.build_command(Path("repo"), Path("out.md"), "medium", "workspace-write")
        self.assertIn("workspace-write", command)

    def test_never_adds_yolo_or_danger_full_access(self) -> None:
        provider = CodexProvider(CodexConfig())
        command = provider.build_command(Path("repo"), Path("out.md"), "low", "read-only")
        joined = " ".join(command)
        self.assertNotIn("--yolo", joined)
        self.assertNotIn("danger-full-access", joined)
        self.assertNotIn("dangerously-bypass-approvals-and-sandbox", joined)


if __name__ == "__main__":
    unittest.main()
