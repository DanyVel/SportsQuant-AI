"""
NBA Player repository implementation.
"""

from __future__ import annotations

from sportsquant.models import Player
from sportsquant.providers import NBAProvider
from sportsquant.repositories import PlayerRepository


class NBAPlayerRepository(PlayerRepository):
    """
    NBA implementation of PlayerRepository.
    """

    def __init__(
        self,
        provider: NBAProvider | None = None,
    ) -> None:
        """
        Initialize repository.
        """
        self._provider = provider or NBAProvider()

    def get_all(
        self,
    ) -> tuple[Player, ...]:
        """
        Retrieve every NBA player.
        """
        return tuple(
            self._provider.get_players()
        )

    def get_by_id(
        self,
        player_id: int,
    ) -> Player | None:
        """
        Retrieve a player by identifier.
        """
        for player in self.get_all():
            if player.id == player_id:
                return player

        return None