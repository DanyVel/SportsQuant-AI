"""
Mapper between GameSummary domain models and ORM models.
"""

from __future__ import annotations

from sportsquant.models import GameSummary
from sportsquant.persistence.orm import GameORM


class GameMapper:
    """
    Maps GameSummary domain models to ORM models and vice versa.
    """

    @staticmethod
    def to_domain(game: GameORM) -> GameSummary:
        """
        Convert an ORM model into a domain model.
        """
        return GameSummary(
            game_id=game.game_id,
            game_date=game.game_date,
            home_team_id=game.home_team_id,
            away_team_id=game.away_team_id,
            matchup=game.matchup,
        )

    @staticmethod
    def to_orm(game: GameSummary) -> GameORM:
        """
        Convert a domain model into an ORM model.
        """
        return GameORM(
            game_id=game.game_id,
            game_date=game.game_date,
            home_team_id=game.home_team_id,
            away_team_id=game.away_team_id,
            matchup=game.matchup,
        )