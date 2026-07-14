"""
Game aggregate root.
"""

from __future__ import annotations

from dataclasses import dataclass

from sportsquant.models import (
    GameSummary,
    PlayerGameStats,
    TeamGameStats,
)


@dataclass(frozen=True, slots=True)
class Game:
    """
    Aggregate Root representing a complete basketball game.

    A Game groups together the entities that describe a single
    basketball game within the SportsQuant domain.
    """

    summary: GameSummary

    home_team_stats: TeamGameStats

    away_team_stats: TeamGameStats

    player_stats: tuple[PlayerGameStats, ...]