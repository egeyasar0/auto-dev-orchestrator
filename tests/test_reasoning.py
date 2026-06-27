from __future__ import annotations

import unittest

from auto_dev.reasoning import route_reasoning


class ReasoningTests(unittest.TestCase):
    def test_routes_from_risk_when_default_medium(self) -> None:
        self.assertEqual(route_reasoning("low"), "low")
        self.assertEqual(route_reasoning("xhigh"), "xhigh")

    def test_config_default_overrides(self) -> None:
        self.assertEqual(route_reasoning("low", "high"), "high")


if __name__ == "__main__":
    unittest.main()

