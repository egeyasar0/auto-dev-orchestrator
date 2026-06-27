from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


RiskLevel = Literal["low", "medium", "high", "xhigh"]
ReasoningEffort = Literal["low", "medium", "high", "xhigh"]
SandboxMode = Literal["read-only", "workspace-write"]


@dataclass(frozen=True)
class CodexConfig:
    command: str = "codex"
    model: str | None = None
    reasoning_effort_config_key: str = "model_reasoning_effort"


@dataclass(frozen=True)
class SafetyConfig:
    allow_yolo: bool = False
    allow_network: bool = False
    require_user_approval_for_dependencies: bool = True
    require_user_approval_for_security_changes: bool = True
    require_user_approval_for_db_migrations: bool = True
    require_user_approval_for_deploy_changes: bool = True


@dataclass(frozen=True)
class AppConfig:
    default_provider: str = "codex"
    default_reasoning_effort: ReasoningEffort = "medium"
    max_fix_attempts: int = 2
    require_clean_git: bool = True
    auto_approve_low_risk_plan: bool = True
    providers: dict[str, CodexConfig] = field(default_factory=lambda: {"codex": CodexConfig()})
    safety: SafetyConfig = field(default_factory=SafetyConfig)


@dataclass(frozen=True)
class RepoContext:
    root: Path
    has_git: bool
    branch: str | None
    dirty_files: list[str]
    config_exists: bool
    project_types: list[str]
    test_commands: list[list[str]]


@dataclass(frozen=True)
class RunPaths:
    root: Path
    user_request: Path
    repo_context: Path
    generated_prompt: Path
    plan_output: Path
    plan_review: Path
    implementation_output: Path
    test_output: Path
    review_output: Path
    git_diff: Path
    final_summary: Path


@dataclass(frozen=True)
class CommandResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def output(self) -> str:
        return "\n".join(part for part in [self.stdout, self.stderr] if part)


@dataclass(frozen=True)
class AgentResult:
    command: CommandResult
    last_message: str
