# Mirrors frontend/src/lib/buckets.ts — keep the two in sync.
# Maps the range-bucket strings collected by the frontend form to the same
# representative numeric estimates stored in *_range's companion
# estimated_* column, so the backend can derive numbers from a request that
# only carries the range label.

INCOME_BUCKETS: dict[str, float] = {
    "Less than $30,000": 25000,
    "$30,000 – $50,000": 40000,
    "$50,000 – $75,000": 62500,
    "$75,000 – $100,000": 87500,
    "$100,000 – $150,000": 125000,
    "$150,000+": 175000,
}

GOAL_AMOUNT_BUCKETS: dict[str, float] = {
    "Less than $10,000": 7500,
    "$10,000 – $50,000": 30000,
    "$50,000 – $100,000": 75000,
    "$100,000 – $500,000": 300000,
    "$500,000+": 750000,
}

GOAL_TIMEFRAME_BUCKETS: dict[str, int] = {
    "Less than 5 years": 3,
    "5–10 years": 7,
    "10–20 years": 15,
    "20+ years": 25,
}

MONTHLY_CONTRIBUTION_BUCKETS: dict[str, float] = {
    "$0 – $100": 50,
    "$100 – $250": 175,
    "$250 – $500": 375,
    "$500 – $1,000": 750,
    "$1,000 – $2,500": 1750,
    "$2,500 – $5,000": 3750,
    "$5,000 – $10,000": 7500,
    "$10,000+": 12500,
}

# Common savings-rate benchmark used to derive a monthly contribution when
# the user has no specific monthly goal in mind.
DEFAULT_SAVINGS_RATE = 0.15


def estimate_monthly_contribution_from_income(estimated_annual_income: float) -> float:
    return estimated_annual_income * DEFAULT_SAVINGS_RATE / 12


def midpoint_for(buckets: dict[str, float], label: str) -> float:
    try:
        return buckets[label]
    except KeyError as exc:
        raise ValueError(f"Unknown bucket label: {label!r}") from exc
