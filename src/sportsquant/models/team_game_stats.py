"""
Team game statistics domain model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TeamGameStats:
    """
    Statistics recorded by a team during a single NBA game.
    """

    game_id: str
    team_id: int

    minutes: str

    points: int


    field_goals_made: int
    field_goals_attempted: int

    three_pointers_made: int
    three_pointers_attempted: int

    free_throws_made: int
    free_throws_attempted: int

    offensive_rebounds: int
    defensive_rebounds: int
    rebounds: int

    assists: int
    steals: int
    blocks: int

    turnovers: int
    personal_fouls: int