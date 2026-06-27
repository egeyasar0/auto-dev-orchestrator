from __future__ import annotations

from .models import ReasoningEffort, RiskLevel


def route_reasoning(risk: RiskLevel, default: ReasoningEffort = "medium") -> ReasoningEffort:
    if default != "medium":
        return default
    return {"low": "low", "medium": "medium", "high": "high", "xhigh": "xhigh"}[risk]

