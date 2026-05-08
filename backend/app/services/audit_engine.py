from typing import Optional
from app.services.pricing_catalog import (
    PRICING_CATALOG,
    ALTERNATIVES,
    get_plan_price,
    get_cheapest_plan,
)


def audit_single_tool(
    tool: str,
    current_plan: str,
    monthly_spend: float,
    seats: int,
    use_case: str,
) -> dict:
    tool = tool.lower()
    current_plan = current_plan.lower()

    result = {
        "tool": tool,
        "current_plan": current_plan,
        "current_monthly_spend": monthly_spend,
        "recommended_plan": current_plan,
        "recommended_monthly_spend": monthly_spend,
        "monthly_savings": 0,
        "annual_savings": 0,
        "reason": "Your current plan looks appropriate.",
        "action": "keep",
        "credex_opportunity": False,
    }

    # --- CHECK 1: Are they overpaying vs expected plan price? ---
    expected_price = get_plan_price(tool, current_plan)
    if expected_price is not None:
        expected_total = expected_price * seats
        if monthly_spend > expected_total * 1.1:
            overpay = monthly_spend - expected_total
            result["reason"] = (
                f"You appear to be overpaying. "
                f"{tool.title()} {current_plan.title()} for {seats} seat(s) "
                f"should cost ${expected_total:.0f}/mo, not ${monthly_spend:.0f}/mo."
            )
            result["recommended_monthly_spend"] = expected_total
            result["monthly_savings"] = overpay
            result["annual_savings"] = overpay * 12
            result["action"] = "verify_billing"
            return result

    # --- CHECK 2: Is there a cheaper plan from same vendor? ---
    current_price_per_user = get_plan_price(tool, current_plan) or 0
    user_is_on_paid_plan = current_price_per_user > 0

    cheapest = get_cheapest_plan(tool, seats, paid_only=user_is_on_paid_plan)

    if cheapest and cheapest["plan"] != current_plan:
        if user_is_on_paid_plan and cheapest["price_per_user"] == 0:
            cheapest = None

    if cheapest and cheapest["plan"] != current_plan:
        current_total = monthly_spend
        cheaper_total = cheapest["total_monthly"]
        if cheaper_total < current_total * 0.9:
            savings = current_total - cheaper_total
            result["recommended_plan"] = cheapest["plan"]
            result["recommended_monthly_spend"] = cheaper_total
            result["monthly_savings"] = round(savings, 2)
            result["annual_savings"] = round(savings * 12, 2)
            result["reason"] = (
                f"Switch from {current_plan.title()} to "
                f"{cheapest['plan'].title()} plan. "
                f"For {seats} seat(s), you'd pay ${cheaper_total:.0f}/mo "
                f"instead of ${current_total:.0f}/mo."
            )
            result["action"] = "downgrade"
            if savings > 100:
                result["credex_opportunity"] = True
            return result

    # --- CHECK 3: Is there a cheaper alternative tool? ---
    use_case_alts = ALTERNATIVES.get(use_case.lower(), {})
    tool_alts = use_case_alts.get(tool, [])

    for alt_tool in tool_alts:
        alt_cheapest = get_cheapest_plan(alt_tool, seats, paid_only=user_is_on_paid_plan)
        if not alt_cheapest:
            continue
        if alt_cheapest["total_monthly"] < monthly_spend * 0.7:
            savings = monthly_spend - alt_cheapest["total_monthly"]
            result["recommended_plan"] = f"{alt_tool} {alt_cheapest['plan']}"
            result["recommended_monthly_spend"] = alt_cheapest["total_monthly"]
            result["monthly_savings"] = round(savings, 2)
            result["annual_savings"] = round(savings * 12, 2)
            result["reason"] = (
                f"Consider switching to {alt_tool.replace('_', ' ').title()} "
                f"({alt_cheapest['plan'].title()} plan) for "
                f"${alt_cheapest['total_monthly']:.0f}/mo. "
                f"Similar capability for your {use_case} use case."
            )
            result["action"] = "switch_tool"
            if savings > 100:
                result["credex_opportunity"] = True
            return result

    return result


def run_full_audit(tool_entries: list[dict]) -> dict:
    results = []
    total_monthly_savings = 0
    total_current_spend = 0

    for entry in tool_entries:
        tool_result = audit_single_tool(
            tool=entry.get("tool", ""),
            current_plan=entry.get("plan", ""),
            monthly_spend=float(entry.get("monthly_spend", 0)),
            seats=int(entry.get("seats", 1)),
            use_case=entry.get("use_case", "mixed"),
        )
        results.append(tool_result)
        total_monthly_savings += tool_result["monthly_savings"]
        total_current_spend += entry.get("monthly_spend", 0)

    credex_opportunity = any(r["credex_opportunity"] for r in results)

    return {
        "tool_results": results,
        "total_current_monthly_spend": round(total_current_spend, 2),
        "total_monthly_savings": round(total_monthly_savings, 2),
        "total_annual_savings": round(total_monthly_savings * 12, 2),
        "credex_opportunity": credex_opportunity,
        "summary": None,
    }