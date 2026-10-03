"""Date and progression rules shared by the competition API."""
from datetime import date, timedelta

TIERS = ("bronze", "silver", "gold", "sapphire", "ruby", "diamond")


def week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())


def period_bounds(period: str, today: date) -> tuple[date | None, date]:
    if period == "day":
        start = today
    elif period == "week":
        start = week_start(today)
    elif period == "month":
        start = today.replace(day=1)
    elif period == "all":
        start = None
    else:
        raise ValueError("Unsupported period")
    return start, today + timedelta(days=1)


def next_tier(tier: int, rank: int, participants: int, xp: int) -> int:
    """Shared ranks never use user IDs to split a promotion/demotion tie."""
    if participants < 5:
        return tier
    quota = max(1, participants // 5)
    if xp > 0 and rank <= quota:
        return min(tier + 1, len(TIERS) - 1)
    if rank > participants - quota:
        return max(tier - 1, 0)
    return tier
