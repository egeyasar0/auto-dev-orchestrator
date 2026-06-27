from __future__ import annotations

import argparse
import sys
from pathlib import Path

from auto_dev.config import load_config
from auto_dev.models import AppConfig, RepoContext, RunPaths
from auto_dev.plan_review import review_plan
from auto_dev.prompt_builder import build_implementation_prompt, build_plan_prompt, build_review_prompt
from auto_dev.providers.codex import CodexProvider
from auto_dev.reasoning import route_reasoning
from auto_dev.repo.git_guard import dirty_outside_agent, git_diff
from auto_dev.repo.inspect import inspect_repo, repo_context_json
from auto_dev.risk import classify_risk
from auto_dev.runtime.run_store import create_run, latest_run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="auto-dev")
    sub = parser.add_subparsers(dest="command", required=True)
    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("task")
    run_parser = sub.add_parser("run")
    run_parser.add_argument("task")
    sub.add_parser("review")
    sub.add_parser("status")
    args = parser.parse_args(argv)

    root = Path.cwd().resolve()
    if args.command == "status":
        return status(root)
    if args.command == "plan":
        _, _, recommendation = run_plan(root, args.task)
        return 2 if is_blocked(recommendation) else 0
    if args.command == "run":
        return run_task(root, args.task)
    if args.command == "review":
        return review(root)
    return 1


def provider(config: AppConfig) -> CodexProvider:
    return CodexProvider(config.providers["codex"])


def run_plan(root: Path, task: str) -> tuple[RunPaths, str, str]:
    config = load_config(root)
    context = inspect_repo(root)
    risk = classify_risk(task)
    effort = route_reasoning(risk, config.default_reasoning_effort)
    run = create_run(root)
    prompt = build_plan_prompt(task, context, risk, effort)

    run.user_request.write_text(task, encoding="utf-8")
    run.repo_context.write_text(repo_context_json(context), encoding="utf-8")
    run.generated_prompt.write_text(prompt, encoding="utf-8")

    result = provider(config).plan(prompt, root, run.plan_output, effort)
    if not run.plan_output.exists():
        run.plan_output.write_text(result.last_message, encoding="utf-8")
    if result.command.returncode != 0:
        recommendation = "BLOCKED: provider command failed."
        run.plan_review.write_text(recommendation + "\n", encoding="utf-8")
        print(run.plan_output.read_text(encoding="utf-8", errors="ignore"))
        print("\n--- deterministic review ---")
        print(recommendation)
        print(f"\nRun artifacts: {run.root}")
        return run, run.plan_output.read_text(encoding="utf-8", errors="ignore"), recommendation
    plan_text = run.plan_output.read_text(encoding="utf-8", errors="ignore")
    recommendation = review_plan(plan_text, risk, config.auto_approve_low_risk_plan)
    run.plan_review.write_text(recommendation + "\n", encoding="utf-8")

    print(plan_text)
    print("\n--- deterministic review ---")
    print(recommendation)
    print(f"\nRun artifacts: {run.root}")
    return run, plan_text, recommendation


def run_task(root: Path, task: str) -> int:
    config = load_config(root)
    run, plan_text, recommendation = run_plan(root, task)
    context = inspect_repo(root)
    risk = classify_risk(task)
    effort = route_reasoning(risk, config.default_reasoning_effort)

    if not context.has_git:
        print("Blocked: this command requires a Git repository.", file=sys.stderr)
        return 2
    if is_blocked(recommendation):
        print(recommendation, file=sys.stderr)
        return 2
    dirty = dirty_outside_agent(root)
    if config.require_clean_git and dirty:
        print("Blocked: working tree has non-.agent changes:", file=sys.stderr)
        for path in dirty:
            print(f"  {path}", file=sys.stderr)
        return 2
    if risk != "low" or not recommendation.startswith("AUTO-APPROVABLE"):
        answer = input(f"Risk is {risk}. Continue with implementation? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Cancelled.")
            return 1

    prompt = build_implementation_prompt(task, plan_text)
    result = provider(config).implement(prompt, root, run.implementation_output, effort)
    if not run.implementation_output.exists():
        run.implementation_output.write_text(result.last_message, encoding="utf-8")
    run.git_diff.write_text(git_diff(root), encoding="utf-8")
    summary = "Implementation complete. Fix loop skipped in MVP.\n"
    run.final_summary.write_text(summary, encoding="utf-8")
    print(summary)
    print(f"Run artifacts: {run.root}")
    return result.command.returncode


def review(root: Path) -> int:
    config = load_config(root)
    if not (root / ".git").exists():
        print("Blocked: review requires a Git repository.", file=sys.stderr)
        return 2
    run = create_run(root)
    diff = git_diff(root)
    run.git_diff.write_text(diff, encoding="utf-8")
    prompt = build_review_prompt(diff)
    run.generated_prompt.write_text(prompt, encoding="utf-8")
    result = provider(config).review(prompt, root, run.review_output, config.default_reasoning_effort)
    if not run.review_output.exists():
        run.review_output.write_text(result.last_message, encoding="utf-8")
    print(run.review_output.read_text(encoding="utf-8", errors="ignore"))
    print(f"\nRun artifacts: {run.root}")
    return result.command.returncode


def status(root: Path) -> int:
    context: RepoContext = inspect_repo(root)
    latest = latest_run(root)
    print(f"project root: {root}")
    print(f"git repo: {'yes' if context.has_git else 'no'}")
    print(f"branch: {context.branch or '-'}")
    print(f"dirty: {'yes' if context.dirty_files else 'no'}")
    if context.branch in {"main", "master"}:
        print("warning: current branch is main/master")
    print(f"config: {'yes' if context.config_exists else 'no'}")
    print(f"latest run: {latest or '-'}")
    print(f"project types: {', '.join(context.project_types) if context.project_types else '-'}")
    return 0


def is_blocked(recommendation: str) -> bool:
    return recommendation.startswith("BLOCKED:")


if __name__ == "__main__":
    raise SystemExit(main())
