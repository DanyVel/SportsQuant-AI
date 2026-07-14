"""
Game summary domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class GameSummary:
    """
    Aggregate Root representing a single NBA game.

    This entity contains the minimum information required to uniquely
    identify a game within the SportsQuant domain.

    Additional game-related entities (team statistics, player statistics,
    box scores, play-by-play events and possessions) reference this
    aggregate.
    """

    game_id: str
    game_date: date

    home_team_id: int
    away_team_id: int

    matchup: str