"""
Database session configuration.

This module is responsible for creating and exposing SQLAlchemy sessions
used by the persistence layer.
"""

from sqlalchemy.orm import Session, sessionmaker

from sportsquant.persistence.database import get_engine

_SessionFactory = sessionmaker(
    bind=get_engine(),
)


def get_session() -> Session:
    """
    Create and return a new database session.
    """
    return _SessionFactory()