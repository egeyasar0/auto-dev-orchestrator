from __future__ import annotations

from .models import RiskLevel

LOW = ("typo", "spelling", "copy", "text", "readme", "comment", "docs")
HIGH = ("auth", "security", "secret", "database", "migration", "deploy", "production", "payment")
XHIGH = ("agentic", "orchestrator", "supervisor", "worker", "architecture", "complex", "difficult debugging")
MEDIUM = ("feature", "test", "refactor", "api", "cli")


def classify_risk(task: str) -> RiskLevel:
    text = task.lower()
    if any(word in text for word in XHIGH):
        return "xhigh"
    if any(word in text for word in HIGH):
        return "high"
    if any(word in text for word in LOW) and not any(word in text for word in MEDIUM):
        return "low"
    return "medium"

