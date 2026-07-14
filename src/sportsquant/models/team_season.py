"""
Team season domain model.
"""

from __future__ import annotations

from dataclasses import dataclass

from sportsquant.models.record import Record
from sportsquant.models.standing import Standing
from sportsquant.models.streak import Streak


@dataclass(frozen=True, slots=True)
class TeamSeason:
    """
    Represents a team's participation during a specific NBA season.
    """

    season_id: str
    team_id: int
    record: Record
    standing: Standing | None = None
    streak: Streak | None = None

    @property
    def games_played(self) -> int:
        return self.record.games_played

    @property
    def win_percentage(self) -> float:
        return self.record.win_percentage

    @property
    def has_winning_record(self) -> bool:
        return self.record.wins > self.record.losses