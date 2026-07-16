"""
Persistence repositories.
"""

from .sqlalchemy_game_repository import SQLAlchemyGameRepository

__all__ = [
    "SQLAlchemyGameRepository",
]