"""
Season type value object.
"""

from __future__ import annotations

from enum import Enum


class SeasonType(str, Enum):
    """
    Represents the type of an NBA season.
    """

    PRESEASON = "Pre Season"
    REGULAR = "Regular Season"
    PLAYOFFS = "Playoffs"
    ALL_STAR = "All Star"
    PLAY_IN = "Play In"