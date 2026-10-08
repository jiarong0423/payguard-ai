"""Presentation contract consumes backend results without recalculating."""


def compose_report(aup: dict, velocity: dict, dispute: dict, review: dict, privacy: dict) -> dict:
    if (not isinstance(aup, dict) or aup.get("match_status") not in ("NO_MATCH", "REVIEW_SIGNAL") or
            aup.get("compliance_decision") != "NOT_MADE" or aup.get("advisory_only") is not True or "status" in aup):
        raise ValueError("backend_contract_invalid_aup")
    for result in (velocity, dispute, review, privacy):
        if not isinstance(result, dict) or "status" not in result:
            raise ValueError("backend_contract_missing_status")
    return {"schema_version": "payguard.demo_report.v1", "source": "synthetic",
            "mode": "offline", "aup": aup, "velocity": velocity, "dispute": dispute,
            "review": review, "privacy": privacy, "external_submission": "FROZEN",
            "limitations": ["AUP advisory only", "velocity does not predict account freezes",
                            "delivery evidence does not decide disputes", "no PayPal or LLM connection"]}
