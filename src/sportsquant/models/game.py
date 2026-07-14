"""
Game aggregate root.
"""

from __future__ import annotations

from dataclasses import dataclass

from sportsquant.models.game_summary import GameSummary
from sportsquant.models.player_game_stats import PlayerGameStats
from sportsquant.models.team_game_stats import TeamGameStats


@dataclass(frozen=True, slots=True)
class Game:
    """
    Aggregate Root representing a complete basketball game.

    A Game aggregates all domain entities that describe a single game.
    """

    summary: GameSummary

    home_team_stats: TeamGameStats

    away_team_stats: TeamGameStats

    player_stats: tuple[PlayerGameStats, ...]