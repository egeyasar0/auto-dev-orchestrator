# Contributing

Thanks for helping improve `auto-dev-orchestrator`.

Before opening a PR:

- Run tests: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v`
- Keep provider-specific logic inside provider classes.
- Do not add unsafe default behavior.
- Avoid unnecessary dependencies.
- Preserve local-first behavior.
- Do not commit `.agent/runs/`, local config, secrets, logs, caches, or virtual environments.
