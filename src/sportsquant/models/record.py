"""
Season record value object.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Record:
    """
    Represents a team's win-loss record.
    """

    wins: int
    losses: int

    def __post_init__(self) -> None:
        if self.wins < 0:
            raise ValueError("wins cannot be negative.")

        if self.losses < 0:
            raise ValueError("losses cannot be negative.")

    @property
    def games_played(self) -> int:
        return self.wins + self.losses

    @property
    def win_percentage(self) -> float:
        if self.games_played == 0:
            return 0.0

        return self.wins / self.games_played