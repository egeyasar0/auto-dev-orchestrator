from __future__ import annotations

from pathlib import Path
from typing import Protocol

from auto_dev.models import AgentResult, ReasoningEffort


class CodingAgentProvider(Protocol):
    name: str

    def plan(self, prompt: str, project_root: Path, output_file: Path, effort: ReasoningEffort) -> AgentResult:
        ...

    def implement(self, prompt: str, project_root: Path, output_file: Path, effort: ReasoningEffort) -> AgentResult:
        ...

    def review(self, prompt: str, project_root: Path, output_file: Path, effort: ReasoningEffort) -> AgentResult:
        ...

