"""
Database engine configuration.

This module is responsible for creating and exposing the SQLAlchemy
engine used by the persistence layer.
"""

from sqlalchemy import Engine, create_engine

from sportsquant.config.settings import DATABASE_URL

_ENGINE = create_engine(
    DATABASE_URL,
)


def get_engine() -> Engine:
    """
    Return the application's SQLAlchemy engine.
    """
    return _ENGINE