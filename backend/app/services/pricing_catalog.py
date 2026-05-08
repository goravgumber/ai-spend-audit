from typing import Optional

# Every plan for every tool
# Structure: tool -> plan_name -> monthly cost per user
PRICING_CATALOG = {
    "cursor": {
        "hobby": {"price_per_user": 0, "min_seats": 1, "max_seats": None},
        "individual": {"price_per_user": 20, "min_seats": 1, "max_seats": None},
        "teams": {"price_per_user": 40, "min_seats": 2, "max_seats": None},
        "enterprise": {"price_per_user": None, "min_seats": 20, "max_seats": None},
    },
    "github_copilot": {
        "individual": {"price_per_user": 10, "min_seats": 1, "max_seats": 1},
        "business": {"price_per_user": 19, "min_seats": 1, "max_seats": None},
        "enterprise": {"price_per_user": 39, "min_seats": 1, "max_seats": None},
    },
    "claude": {
        "free": {"price_per_user": 0, "min_seats": 1, "max_seats": None},
        "pro": {"price_per_user": 20, "min_seats": 1, "max_seats": None},
        "max": {"price_per_user": 100, "min_seats": 1, "max_seats": None},
        "team": {"price_per_user": 30, "min_seats": 1, "max_seats": None},
        "enterprise": {"price_per_user": None, "min_seats": 1, "max_seats": None},
    },
    "chatgpt": {
        "free": {"price_per_user": 0, "min_seats": 1, "max_seats": None},
        "go": {"price_per_user": 8, "min_seats": 1, "max_seats": None},
        "plus": {"price_per_user": 20, "min_seats": 1, "max_seats": None},
        "pro": {"price_per_user": 100, "min_seats": 1, "max_seats": None},
        "team": {"price_per_user": 30, "min_seats": 2, "max_seats": None},
        "enterprise": {"price_per_user": None, "min_seats": 150, "max_seats": None},
    },
    "windsurf": {
        "free": {"price_per_user": 0, "min_seats": 1, "max_seats": None},
        "pro": {"price_per_user": 20, "min_seats": 1, "max_seats": None},
        "max": {"price_per_user": 200, "min_seats": 1, "max_seats": None},
        "teams": {"price_per_user": 40, "min_seats": 2, "max_seats": None},
        "enterprise": {"price_per_user": None, "min_seats": 1, "max_seats": None},
    },
    "gemini": {
        "free": {"price_per_user": 0, "min_seats": 1, "max_seats": None},
        "advanced": {"price_per_user": 20, "min_seats": 1, "max_seats": None},
        "business": {"price_per_user": 24, "min_seats": 1, "max_seats": None},
        "enterprise": {"price_per_user": None, "min_seats": 1, "max_seats": None},
    },
    "anthropic_api": {
        "pay_as_you_go": {"price_per_user": None, "min_seats": 1, "max_seats": None},
    },
    "openai_api": {
        "pay_as_you_go": {"price_per_user": None, "min_seats": 1, "max_seats": None},
    },
}

# Cheaper alternatives by use case
# When a user is paying for X and use case is Y, suggest Z
ALTERNATIVES = {
    "coding": {
        "cursor": ["windsurf", "github_copilot"],
        "windsurf": ["cursor", "github_copilot"],
        "chatgpt": ["cursor", "claude"],
    },
    "writing": {
        "chatgpt": ["claude"],
        "claude": ["chatgpt"],
        "cursor": ["chatgpt", "claude"],
    },
    "research": {
        "chatgpt": ["claude", "gemini"],
        "cursor": ["claude", "chatgpt"],
    },
    "data": {
        "chatgpt": ["claude", "gemini"],
        "claude": ["chatgpt", "gemini"],
    },
}

def get_plan_price(tool: str, plan: str) -> Optional[float]:
    """Returns monthly price per user for a given tool and plan."""
    tool_data = PRICING_CATALOG.get(tool.lower())
    if not tool_data:
        return None
    plan_data = tool_data.get(plan.lower())
    if not plan_data:
        return None
    return plan_data.get("price_per_user")

def get_cheapest_plan(tool: str, seats: int, paid_only: bool = False) -> Optional[dict]:
    """Returns the cheapest valid plan for a tool given number of seats."""
    tool_data = PRICING_CATALOG.get(tool.lower())
    if not tool_data:
        return None

    valid_plans = []
    for plan_name, plan_info in tool_data.items():
        price = plan_info.get("price_per_user")
        min_seats = plan_info.get("min_seats", 1)
        if price is None:
            continue  # skip enterprise
        if paid_only and price == 0:
            continue  # skip free tiers when user is on paid plan
        if seats >= min_seats:
            valid_plans.append({
                "plan": plan_name,
                "price_per_user": price,
                "total_monthly": price * seats
            })

    if not valid_plans:
        return None

    return min(valid_plans, key=lambda x: x["total_monthly"])