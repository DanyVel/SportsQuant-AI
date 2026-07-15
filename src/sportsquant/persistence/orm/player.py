"""
SQLAlchemy ORM model for NBA players.
"""

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from sportsquant.persistence.orm.base import Base


class PlayerORM(Base):
    """
    SQLAlchemy ORM model representing an NBA player.
    """

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )