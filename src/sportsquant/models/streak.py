"""
Streak value object.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Streak:
    """
    Represents a team's current streak.
    """

    value: int

    @property
    def is_winning(self) -> bool:
        return self.value > 0

    @property
    def is_losing(self) -> bool:
        return self.value < 0

    @property
    def games(self) -> int:
        return abs(self.value)