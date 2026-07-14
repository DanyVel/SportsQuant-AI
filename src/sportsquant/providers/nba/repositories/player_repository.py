"""
NBA player repository implementation.
"""

from __future__ import annotations

from sportsquant.models import Player
from sportsquant.providers.nba.provider import NBAProvider
from sportsquant.repositories import PlayerRepository


class NBAPlayerRepository(PlayerRepository):
    """
    Repository implementation backed by the NBA provider.
    """

    def __init__(self, provider: NBAProvider) -> None:
        """
        Initialize the repository.

        Parameters
        ----------
        provider : NBAProvider
            NBA data provider.
        """
        self._provider = provider

    def get_all(self) -> tuple[Player, ...]:
        """
        Retrieve all available players.
        """
        return tuple(self._provider.get_players())

    def get_by_id(self, player_id: int) -> Player | None:
        """
        Retrieve a player by ID.
        """
        return next(
            (
                player
                for player in self._provider.get_players()
                if player.id == player_id
            ),
            None,
        )