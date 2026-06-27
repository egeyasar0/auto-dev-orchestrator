from __future__ import annotations

from pathlib import Path

from auto_dev.models import AgentResult, CodexConfig, ReasoningEffort, SandboxMode
from auto_dev.runtime.command_runner import CommandRunner


class CodexProvider:
    name = "codex"

    def __init__(self, config: CodexConfig) -> None:
        self.config = config

    def plan(self, prompt: str, project_root: Path, output_file: Path, effort: ReasoningEffort) -> AgentResult:
        return self._run(prompt, project_root, output_file, effort, "read-only", skip_git_repo_check=True)

    def implement(self, prompt: str, project_root: Path, output_file: Path, effort: ReasoningEffort) -> AgentResult:
        return self._run(prompt, project_root, output_file, effort, "workspace-write")

    def review(self, prompt: str, project_root: Path, output_file: Path, effort: ReasoningEffort) -> AgentResult:
        return self._run(prompt, project_root, output_file, effort, "read-only")

    def build_command(
        self,
        project_root: Path,
        output_file: Path,
        effort: ReasoningEffort,
        sandbox: SandboxMode,
        skip_git_repo_check: bool = False,
    ) -> list[str]:
        if sandbox == "danger-full-access":
            raise ValueError("danger-full-access is not allowed")
        command = [
            self.config.command,
            "exec",
            "--sandbox",
            sandbox,
            "--cd",
            str(project_root),
            "--config",
            f'{self.config.reasoning_effort_config_key}="{effort}"',
            "--output-last-message",
            str(output_file),
            "-",
        ]
        if self.config.model:
            command[6:6] = ["--model", self.config.model]
        if skip_git_repo_check:
            command.insert(-1, "--skip-git-repo-check")
        return command

    def _run(
        self,
        prompt: str,
        project_root: Path,
        output_file: Path,
        effort: ReasoningEffort,
        sandbox: SandboxMode,
        skip_git_repo_check: bool = False,
    ) -> AgentResult:
        command = self.build_command(project_root, output_file, effort, sandbox, skip_git_repo_check)
        result = CommandRunner(project_root).run(command, input_text=prompt, check=False)
        last_message = output_file.read_text(encoding="utf-8", errors="ignore") if output_file.exists() else result.output
        return AgentResult(command=result, last_message=last_message)
