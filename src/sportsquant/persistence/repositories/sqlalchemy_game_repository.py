"""
SQLAlchemy repository for persisting Game aggregates.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from sportsquant.aggregates import Game
from sportsquant.persistence.mappers import (
    GameMapper,
    PlayerGameStatsMapper,
    TeamGameStatsMapper,
)


class SQLAlchemyGameRepository:
    """
    Repository responsible for persisting Game aggregates using SQLAlchemy.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the repository with a SQLAlchemy session.
        """
        self._session = session

    def save(self, game: Game) -> None:
        """
        Persist a Game aggregate.
        """
        try:
            self._session.add(GameMapper.to_orm(game.summary))

            self._session.add(
                TeamGameStatsMapper.to_orm(game.home_team_stats)
            )

            self._session.add(
                TeamGameStatsMapper.to_orm(game.away_team_stats)
            )

            for player_stats in game.player_stats:
                self._session.add(
                    PlayerGameStatsMapper.to_orm(player_stats)
                )

            self._session.commit()

        except Exception:
            self._session.rollback()
            raise