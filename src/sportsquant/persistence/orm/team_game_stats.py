"""
SQLAlchemy ORM model for team game statistics.
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from sportsquant.persistence.orm.base import Base


class TeamGameStatsORM(Base):
    """
    SQLAlchemy ORM model representing a team's statistics for a single game.
    """

    __tablename__ = "team_game_stats"

    game_id: Mapped[str] = mapped_column(
        ForeignKey("games.game_id"),
        primary_key=True,
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        primary_key=True,
    )

    minutes: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    points: Mapped[int] = mapped_column(Integer, nullable=False)

    field_goals_made: Mapped[int] = mapped_column(Integer, nullable=False)
    field_goals_attempted: Mapped[int] = mapped_column(Integer, nullable=False)

    three_pointers_made: Mapped[int] = mapped_column(Integer, nullable=False)
    three_pointers_attempted: Mapped[int] = mapped_column(Integer, nullable=False)

    free_throws_made: Mapped[int] = mapped_column(Integer, nullable=False)
    free_throws_attempted: Mapped[int] = mapped_column(Integer, nullable=False)

    offensive_rebounds: Mapped[int] = mapped_column(Integer, nullable=False)
    defensive_rebounds: Mapped[int] = mapped_column(Integer, nullable=False)
    rebounds: Mapped[int] = mapped_column(Integer, nullable=False)

    assists: Mapped[int] = mapped_column(Integer, nullable=False)
    steals: Mapped[int] = mapped_column(Integer, nullable=False)
    blocks: Mapped[int] = mapped_column(Integer, nullable=False)

    turnovers: Mapped[int] = mapped_column(Integer, nullable=False)
    personal_fouls: Mapped[int] = mapped_column(Integer, nullable=False)