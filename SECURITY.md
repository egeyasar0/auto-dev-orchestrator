# Security

`auto-dev-orchestrator` runs local coding agents and local commands. Treat generated plans, diffs, and run artifacts as project-sensitive output.

## Safe Defaults

- Plan and review use read-only sandbox mode.
- Implementation uses workspace-write sandbox mode.
- `--yolo` and `danger-full-access` are not used by default.
- Dirty non-`.agent/` working trees block implementation.

## Secrets

Never commit secrets, tokens, credentials, `.env` files, or local config.

`.agent/runs/` may contain prompts, model output, file paths, and repository context. It is ignored and should not be committed.

## Reporting Security Issues

This project does not yet have a private security reporting channel. Until one exists, avoid posting sensitive exploit details publicly; open a minimal issue asking for a secure contact path.
