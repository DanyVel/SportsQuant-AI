"""
Database session utilities.
"""

from __future__ import annotations

from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


class SessionFactory:
    """
    SQLAlchemy session factory.
    """

    @staticmethod
    def create(
        engine: Engine,
    ) -> sessionmaker[Session]:
        """
        Create a session factory.

        Args:
            engine:
                SQLAlchemy engine.

        Returns:
            Configured session factory.
        """
        return sessionmaker(
            bind=engine,
            autoflush=False,
            expire_on_commit=False,
        )