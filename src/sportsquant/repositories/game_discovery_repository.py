"""
Game discovery repository interface.
"""

from __future__ import annotations

from abc import abstractmethod

from sportsquant.repositories.base import BaseRepository


class GameDiscoveryRepository(BaseRepository):
    """
    Contract for discovering games.
    """

    @abstractmethod
    def get_game_ids(
        self,
        season: str,
    ) -> tuple[str, ...]:
        """
        Retrieve every game identifier
        for a season.
        """
        raise NotImplementedError