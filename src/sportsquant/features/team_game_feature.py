"""
Team game feature model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class TeamGameFeature:
    """
    Analytical row derived from one game for one team.
    """

    game_id: str
    game_date: date

    team_id: int
    opponent_team_id: int
    is_home: bool

    points: int
    opponent_points: int

    field_goals_made: int
    field_goals_attempted: int

    three_pointers_made: int
    three_pointers_attempted: int

    free_throws_made: int
    free_throws_attempted: int

    offensive_rebounds: int
    defensive_rebounds: int

    assists: int
    steals: int
    blocks: int

    turnovers: int
    personal_fouls: int

    field_goal_percentage: float = 0.0
    three_point_percentage: float = 0.0
    free_throw_percentage: float = 0.0