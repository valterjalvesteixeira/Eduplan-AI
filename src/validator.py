from src.schemas import EduPlan


def validate_total_duration(plan: EduPlan) -> None:
    """
    Validate that the sum of activity durations matches the total duration.
    Raises ValueError if invalid.
    """
    total = sum(a.duration_minutes for a in plan.activities)
    expected = plan.meta.duration_total_minutes

    if total != expected:
        raise ValueError(
            f"Duration mismatch: activities sum to {total} minutes, but meta says {expected} minutes."
        )