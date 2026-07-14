"""
Database utilities.
"""

from __future__ import annotations

from sqlalchemy import Engine
from sqlalchemy import create_engine


class Database:
    """
    Database engine factory.
    """

    @staticmethod
    def create(
        url: str,
        *,
        echo: bool = False,
    ) -> Engine:
        """
        Create a SQLAlchemy engine.

        Args:
            url:
                Database connection URL.

            echo:
                Whether SQL statements should be logged.

        Returns:
            Configured SQLAlchemy engine.
        """
        return create_engine(
            url,
            echo=echo,
            future=True,
        )