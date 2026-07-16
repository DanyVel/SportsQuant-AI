"""
Pure feature calculation helpers.
"""

from __future__ import annotations


def safe_divide(
    numerator: float,
    denominator: float,
) -> float:
    """
    Divide two values, returning zero when the denominator is zero.
    """
    if denominator == 0:
        return 0

    return numerator / denominator


def field_goal_percentage(
    field_goals_made: int,
    field_goals_attempted: int,
) -> float:
    """
    Calculate field goal percentage.
    """
    return safe_divide(
        field_goals_made,
        field_goals_attempted,
    )


def three_point_percentage(
    three_pointers_made: int,
    three_pointers_attempted: int,
) -> float:
    """
    Calculate three point percentage.
    """
    return safe_divide(
        three_pointers_made,
        three_pointers_attempted,
    )


def free_throw_percentage(
    free_throws_made: int,
    free_throws_attempted: int,
) -> float:
    """
    Calculate free throw percentage.
    """
    return safe_divide(
        free_throws_made,
        free_throws_attempted,
    )
