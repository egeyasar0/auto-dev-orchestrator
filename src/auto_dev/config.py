from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from .models import AppConfig, CodexConfig, ReasoningEffort, SafetyConfig

VALID_EFFORTS = {"low", "medium", "high", "xhigh"}


def load_config(project_root: Path) -> AppConfig:
    path = project_root / ".agent" / "config.toml"
    if not path.exists():
        return AppConfig()

    with path.open("rb") as handle:
        data = tomllib.load(handle)

    default_effort = _effort(data.get("default_reasoning_effort", "medium"))
    codex_data = data.get("providers", {}).get("codex", {})
    safety_data = data.get("safety", {})

    return AppConfig(
        default_provider=str(data.get("default_provider", "codex")),
        default_reasoning_effort=default_effort,
        max_fix_attempts=int(data.get("max_fix_attempts", 2)),
        require_clean_git=bool(data.get("require_clean_git", True)),
        auto_approve_low_risk_plan=bool(data.get("auto_approve_low_risk_plan", True)),
        providers={
            "codex": CodexConfig(
                command=str(codex_data.get("command", "codex")),
                model=str(codex_data.get("model", "gpt-5-codex")),
                reasoning_effort_config_key=str(
                    codex_data.get("reasoning_effort_config_key", "model_reasoning_effort")
                ),
            )
        },
        safety=SafetyConfig(
            allow_yolo=bool(safety_data.get("allow_yolo", False)),
            allow_network=bool(safety_data.get("allow_network", False)),
            require_user_approval_for_dependencies=bool(
                safety_data.get("require_user_approval_for_dependencies", True)
            ),
            require_user_approval_for_security_changes=bool(
                safety_data.get("require_user_approval_for_security_changes", True)
            ),
            require_user_approval_for_db_migrations=bool(
                safety_data.get("require_user_approval_for_db_migrations", True)
            ),
            require_user_approval_for_deploy_changes=bool(
                safety_data.get("require_user_approval_for_deploy_changes", True)
            ),
        ),
    )


def _effort(value: Any) -> ReasoningEffort:
    if value not in VALID_EFFORTS:
        raise ValueError(f"invalid reasoning effort: {value!r}")
    return value

