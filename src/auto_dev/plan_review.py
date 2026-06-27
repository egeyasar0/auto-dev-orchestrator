from __future__ import annotations

from .models import RiskLevel

BLOCKED = ("--yolo", "danger-full-access", "dangerously-bypass-approvals-and-sandbox")
APPROVAL = ("install", "dependency", "auth", "security", "migration", "deploy", "secret", "delete")


def review_plan(plan: str, risk: RiskLevel, auto_approve_low_risk: bool) -> str:
    text = plan.lower()
    blocked = [word for word in BLOCKED if word in text]
    approval_text = text
    for phrase in ("no install", "no installs", "do not install", "without installing"):
        approval_text = approval_text.replace(phrase, "")
    approvals = [word for word in APPROVAL if word in approval_text]
    if blocked:
        return f"BLOCKED: plan mentions forbidden option(s): {', '.join(blocked)}"
    if risk == "low" and auto_approve_low_risk and not approvals:
        return "AUTO-APPROVABLE: low risk and no approval-sensitive operations detected."
    if approvals:
        return f"NEEDS APPROVAL: plan mentions approval-sensitive operation(s): {', '.join(sorted(set(approvals)))}"
    return f"NEEDS APPROVAL: risk is {risk}."
