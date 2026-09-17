import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = PROJECT_ROOT / "config" / "policy.json"


def load_policy():
    """Load the Agent Harness policy configuration."""

    with POLICY_PATH.open("r", encoding="utf-8") as policy_file:
        return json.load(policy_file)


def evaluate_intent(intent):
    """Evaluate whether the detected intent is permitted."""

    policy = load_policy()

    if intent in policy["blocked_operations"]:
        return {
            "decision": "blocked",
            "reason": "This operation is prohibited by policy.",
        }

    if intent in policy["approval_required_operations"]:
        return {
            "decision": "approval_required",
            "reason": (
                "The request could modify a ServiceNow record "
                "and requires human approval."
            ),
        }

    if intent in policy["allowed_operations"]:
        return {
            "decision": "allowed",
            "reason": "The requested operation is permitted.",
        }

    return {
        "decision": "blocked",
        "reason": "The operation is not on the approved allow list.",
    }
