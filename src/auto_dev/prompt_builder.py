from __future__ import annotations

from auto_dev.models import RepoContext, ReasoningEffort, RiskLevel
from auto_dev.repo.inspect import repo_context_json


def build_plan_prompt(task: str, context: RepoContext, risk: RiskLevel, effort: ReasoningEffort) -> str:
    return f"""You are the worker coding agent in a supervisor-worker workflow.

Task:
{task}

Repository context:
```json
{repo_context_json(context)}
```

Risk: {risk}
Reasoning effort: {effort}

Plan only. Do not edit files. Do not run install/network commands. Do not use yolo or danger-full-access.
Return a concise implementation plan, files likely to change, tests to run, and any approval-sensitive operations.
"""


def build_implementation_prompt(task: str, plan: str) -> str:
    return f"""Implement this approved task.

Task:
{task}

Approved plan:
{plan}

Stay inside the project root. Do not install dependencies, run network commands, touch secrets, or use destructive commands.
Run only local checks that are already available. Summarize changed files and checks run.
"""


def build_review_prompt(diff: str) -> str:
    return f"""Review the current git diff for bugs, regressions, and missing tests.

```diff
{diff}
```

Return findings first, with file references when possible. If there are no issues, say so.
"""

