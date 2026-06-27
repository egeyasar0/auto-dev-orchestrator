from __future__ import annotations

from datetime import datetime
from pathlib import Path

from auto_dev.models import RunPaths


def create_run(project_root: Path) -> RunPaths:
    runs_root = project_root / ".agent" / "runs"
    runs_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_root = runs_root / stamp
    suffix = 1
    while run_root.exists():
        run_root = runs_root / f"{stamp}-{suffix}"
        suffix += 1
    run_root.mkdir()
    return RunPaths(
        root=run_root,
        user_request=run_root / "user_request.txt",
        repo_context=run_root / "repo_context.json",
        generated_prompt=run_root / "generated_prompt.md",
        plan_output=run_root / "plan_output.md",
        plan_review=run_root / "plan_review.md",
        implementation_output=run_root / "implementation_output.md",
        test_output=run_root / "test_output.txt",
        review_output=run_root / "review_output.md",
        git_diff=run_root / "git_diff.patch",
        final_summary=run_root / "final_summary.md",
    )


def latest_run(project_root: Path) -> Path | None:
    runs_root = project_root / ".agent" / "runs"
    if not runs_root.exists():
        return None
    runs = sorted((path for path in runs_root.iterdir() if path.is_dir()), reverse=True)
    return runs[0] if runs else None

