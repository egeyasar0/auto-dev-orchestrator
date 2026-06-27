from __future__ import annotations

import json
from pathlib import Path

from auto_dev.models import RepoContext
from auto_dev.repo.git_guard import current_branch, dirty_files


def inspect_repo(root: Path) -> RepoContext:
    project_types = detect_project_types(root)
    return RepoContext(
        root=root,
        has_git=(root / ".git").exists(),
        branch=current_branch(root),
        dirty_files=dirty_files(root),
        config_exists=(root / ".agent" / "config.toml").exists(),
        project_types=project_types,
        test_commands=infer_test_commands(root, project_types),
    )


def detect_project_types(root: Path) -> list[str]:
    types: list[str] = []
    checks = [
        ("python", ("pyproject.toml", "requirements.txt", "pytest.ini")),
        ("node", ("package.json", "pnpm-lock.yaml", "vite.config.js", "vite.config.ts", "tsconfig.json")),
        ("rust", ("Cargo.toml",)),
        ("go", ("go.mod",)),
    ]
    for name, files in checks:
        if any((root / file).exists() for file in files):
            types.append(name)
    return types


def infer_test_commands(root: Path, project_types: list[str]) -> list[list[str]]:
    commands: list[list[str]] = []
    if "python" in project_types and ((root / "tests").exists() or (root / "pytest.ini").exists()):
        commands.append(["python", "-m", "unittest", "discover"])
    if "node" in project_types:
        package_json = root / "package.json"
        if package_json.exists() and "test" in package_json.read_text(encoding="utf-8", errors="ignore"):
            commands.append(["pnpm" if (root / "pnpm-lock.yaml").exists() else "npm", "test"])
    if "rust" in project_types:
        commands.append(["cargo", "test"])
    if "go" in project_types:
        commands.append(["go", "test", "./..."])
    return commands


def repo_context_json(context: RepoContext) -> str:
    data = {
        "root": str(context.root),
        "has_git": context.has_git,
        "branch": context.branch,
        "dirty_files": context.dirty_files,
        "config_exists": context.config_exists,
        "project_types": context.project_types,
        "test_commands": context.test_commands,
    }
    return json.dumps(data, indent=2)

