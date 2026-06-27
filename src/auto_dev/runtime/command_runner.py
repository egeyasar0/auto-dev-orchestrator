from __future__ import annotations

import subprocess
from pathlib import Path

from auto_dev.models import CommandResult


class CommandRunner:
    def __init__(self, cwd: Path, timeout: int = 1800) -> None:
        self.cwd = cwd
        self.timeout = timeout

    def run(self, args: list[str], input_text: str | None = None, check: bool = True) -> CommandResult:
        completed = subprocess.run(
            args,
            cwd=self.cwd,
            input=input_text,
            text=True,
            capture_output=True,
            timeout=self.timeout,
            shell=False,
        )
        result = CommandResult(args=args, returncode=completed.returncode, stdout=completed.stdout, stderr=completed.stderr)
        if check and result.returncode != 0:
            raise RuntimeError(result.output or f"command failed: {args}")
        return result

