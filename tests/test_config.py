from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from auto_dev.config import load_config


class ConfigTests(unittest.TestCase):
    def test_defaults_when_config_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = load_config(Path(tmp))
        self.assertEqual(config.default_provider, "codex")
        self.assertEqual(config.default_reasoning_effort, "medium")
        self.assertFalse(config.safety.allow_yolo)

    def test_loads_codex_reasoning_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agent").mkdir()
            (root / ".agent" / "config.toml").write_text(
                '[providers.codex]\nreasoning_effort_config_key = "reasoning.effort"\n',
                encoding="utf-8",
            )
            config = load_config(root)
        self.assertEqual(config.providers["codex"].reasoning_effort_config_key, "reasoning.effort")


if __name__ == "__main__":
    unittest.main()

