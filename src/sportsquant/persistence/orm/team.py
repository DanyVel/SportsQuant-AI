"""
SQLAlchemy ORM model for NBA teams.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from sportsquant.persistence.orm.base import Base


class TeamORM(Base):
    """
    SQLAlchemy ORM model representing an NBA team.
    """

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    abbreviation: Mapped[str] = mapped_column(String(3), nullable=False)

    city: Mapped[str] = mapped_column(String(50), nullable=False)

    nickname: Mapped[str] = mapped_column(String(50), nullable=False)

    state: Mapped[str] = mapped_column(String(50), nullable=False)

    year_founded: Mapped[int] = mapped_column(Integer, nullable=False)