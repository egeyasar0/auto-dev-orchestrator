from __future__ import annotations

import unittest

from auto_dev.risk import classify_risk


class RiskTests(unittest.TestCase):
    def test_low(self) -> None:
        self.assertEqual(classify_risk("fix typo in README"), "low")

    def test_high(self) -> None:
        self.assertEqual(classify_risk("change auth token handling"), "high")

    def test_xhigh(self) -> None:
        self.assertEqual(classify_risk("build agentic supervisor worker orchestrator"), "xhigh")


if __name__ == "__main__":
    unittest.main()

