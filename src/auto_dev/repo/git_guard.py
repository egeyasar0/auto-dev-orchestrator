from __future__ import annotations

from pathlib import Path

from auto_dev.runtime.command_runner import CommandRunner


def current_branch(root: Path) -> str | None:
    if not (root / ".git").exists():
        return None
    result = CommandRunner(root).run(["git", "branch", "--show-current"], check=False)
    branch = result.stdout.strip()
    return branch or None


def dirty_files(root: Path) -> list[str]:
    if not (root / ".git").exists():
        return []
    result = CommandRunner(root).run(["git", "status", "--porcelain"], check=False)
    return [line[3:] for line in result.stdout.splitlines() if len(line) > 3]


def dirty_outside_agent(root: Path) -> list[str]:
    return [path for path in dirty_files(root) if not path.startswith(".agent/") and path != ".agent"]


def git_diff(root: Path) -> str:
    if not (root / ".git").exists():
        return ""
    return CommandRunner(root).run(["git", "diff"], check=False).stdout

