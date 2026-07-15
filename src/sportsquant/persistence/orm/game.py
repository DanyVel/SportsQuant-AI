"""
SQLAlchemy ORM model for NBA games.
"""

from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from sportsquant.persistence.orm.base import Base


class GameORM(Base):
    """
    SQLAlchemy ORM model representing an NBA game.
    """

    __tablename__ = "games"

    game_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
    )

    game_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    home_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
    )

    away_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
    )

    matchup: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )