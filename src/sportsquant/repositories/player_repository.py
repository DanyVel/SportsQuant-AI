"""
Player repository interface.
"""

from __future__ import annotations

from abc import abstractmethod

from sportsquant.models import Player
from sportsquant.repositories.base import BaseRepository


class PlayerRepository(BaseRepository):
    """
    Contract for player repositories.
    """

    @abstractmethod
    def get_all(self) -> tuple[Player, ...]:
        """
        Retrieve all players.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, player_id: int) -> Player | None:
        """
        Retrieve a player by ID.
        """
        raise NotImplementedError