"""
Mapper between TeamGameStats domain models and ORM models.
"""

from __future__ import annotations

from sportsquant.models import TeamGameStats
from sportsquant.persistence.orm import TeamGameStatsORM


class TeamGameStatsMapper:
    """
    Maps TeamGameStats domain models to ORM models and vice versa.
    """

    @staticmethod
    def to_domain(stats: TeamGameStatsORM) -> TeamGameStats:
        """
        Convert an ORM model into a domain model.
        """
        return TeamGameStats(
            game_id=stats.game_id,
            team_id=stats.team_id,
            minutes=stats.minutes,
            points=stats.points,
            field_goals_made=stats.field_goals_made,
            field_goals_attempted=stats.field_goals_attempted,
            three_pointers_made=stats.three_pointers_made,
            three_pointers_attempted=stats.three_pointers_attempted,
            free_throws_made=stats.free_throws_made,
            free_throws_attempted=stats.free_throws_attempted,
            offensive_rebounds=stats.offensive_rebounds,
            defensive_rebounds=stats.defensive_rebounds,
            rebounds=stats.rebounds,
            assists=stats.assists,
            steals=stats.steals,
            blocks=stats.blocks,
            turnovers=stats.turnovers,
            personal_fouls=stats.personal_fouls,
        )

    @staticmethod
    def to_orm(stats: TeamGameStats) -> TeamGameStatsORM:
        """
        Convert a domain model into an ORM model.
        """
        return TeamGameStatsORM(
            game_id=stats.game_id,
            team_id=stats.team_id,
            minutes=stats.minutes,
            points=stats.points,
            field_goals_made=stats.field_goals_made,
            field_goals_attempted=stats.field_goals_attempted,
            three_pointers_made=stats.three_pointers_made,
            three_pointers_attempted=stats.three_pointers_attempted,
            free_throws_made=stats.free_throws_made,
            free_throws_attempted=stats.free_throws_attempted,
            offensive_rebounds=stats.offensive_rebounds,
            defensive_rebounds=stats.defensive_rebounds,
            rebounds=stats.rebounds,
            assists=stats.assists,
            steals=stats.steals,
            blocks=stats.blocks,
            turnovers=stats.turnovers,
            personal_fouls=stats.personal_fouls,
        )