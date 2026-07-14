"""
Play type value object.
"""

from __future__ import annotations

from enum import Enum


class PlayType(str, Enum):
    """
    Represents the type of a play within a basketball game.
    """

    FIELD_GOAL_MADE = "field_goal_made"
    FIELD_GOAL_MISSED = "field_goal_missed"

    FREE_THROW_MADE = "free_throw_made"
    FREE_THROW_MISSED = "free_throw_missed"

    REBOUND = "rebound"

    TURNOVER = "turnover"

    FOUL = "foul"

    STEAL = "steal"

    BLOCK = "block"

    ASSIST = "assist"

    SUBSTITUTION = "substitution"

    TIMEOUT = "timeout"

    JUMP_BALL = "jump_ball"

    PERIOD_START = "period_start"
    PERIOD_END = "period_end"

    UNKNOWN = "unknown"