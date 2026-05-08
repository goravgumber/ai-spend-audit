import pytest
from app.services.audit_engine import audit_single_tool, run_full_audit


def test_cursor_teams_overkill_for_solo():
    """Single user on Teams plan should be recommended Individual."""
    result = audit_single_tool(
        tool="cursor",
        current_plan="teams",
        monthly_spend=40,
        seats=1,
        use_case="coding",
    )
    assert result["monthly_savings"] > 0
    assert result["action"] == "downgrade"


def test_correct_plan_no_savings():
    """User on cheapest available paid plan with no cheaper alternatives."""
    result = audit_single_tool(
        tool="chatgpt",
        current_plan="go",
        monthly_spend=8,
        seats=1,
        use_case="writing",
    )
    assert result["monthly_savings"] == 0
    assert result["action"] == "keep"


def test_overpaying_detected():
    """User paying more than plan price should be flagged."""
    result = audit_single_tool(
        tool="cursor",
        current_plan="individual",
        monthly_spend=50,  # should be $20
        seats=1,
        use_case="coding",
    )
    assert result["monthly_savings"] > 0
    assert result["action"] == "verify_billing"


def test_annual_savings_is_12x_monthly():
    """Annual savings must always equal monthly × 12."""
    result = audit_single_tool(
        tool="cursor",
        current_plan="teams",
        monthly_spend=40,
        seats=1,
        use_case="coding",
    )
    assert result["annual_savings"] == result["monthly_savings"] * 12


def test_full_audit_totals():
    """Total savings should equal sum of individual tool savings."""
    entries = [
        {"tool": "cursor", "plan": "teams", "monthly_spend": 40, "seats": 1, "use_case": "coding"},
        {"tool": "chatgpt", "plan": "plus", "monthly_spend": 20, "seats": 1, "use_case": "writing"},
    ]
    audit = run_full_audit(entries)
    expected_total = sum(r["monthly_savings"] for r in audit["tool_results"])
    assert audit["total_monthly_savings"] == round(expected_total, 2)


def test_credex_opportunity_flagged_for_large_savings():
    """Savings over $100/mo should flag credex_opportunity."""
    result = audit_single_tool(
        tool="windsurf",
        current_plan="max",
        monthly_spend=200,
        seats=1,
        use_case="coding",
    )
    if result["monthly_savings"] > 100:
        assert result["credex_opportunity"] is True


def test_empty_tool_list():
    """Empty input should return zero savings."""
    audit = run_full_audit([])
    assert audit["total_monthly_savings"] == 0
    assert audit["tool_results"] == []