from __future__ import annotations

import unittest

from auto_dev.plan_review import review_plan


class PlanReviewTests(unittest.TestCase):
    def test_no_installs_is_not_dependency_approval(self) -> None:
        review = review_plan("Approval-sensitive operations: none. No installs planned.", "low", True)
        self.assertTrue(review.startswith("AUTO-APPROVABLE"))


if __name__ == "__main__":
    unittest.main()

