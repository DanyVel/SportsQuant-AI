"""
Player application service.
"""

from __future__ import annotations

from sportsquant.models import Player
from sportsquant.repositories import PlayerRepository


class PlayerService:
    """
    Application service for player-related use cases.
    """

    def __init__(
        self,
        repository: PlayerRepository,
    ) -> None:
        """
        Initialize the service.

        Parameters
        ----------
        repository : PlayerRepository
            Repository used to access player data.
        """
        self._repository = repository

    def get_players(self) -> tuple[Player, ...]:
        """
        Retrieve all players.
        """
        return self._repository.get_all()

    def get_player_by_id(
        self,
        player_id: int,
    ) -> Player | None:
        """
        Retrieve a player by identifier.
        """
        return self._repository.get_by_id(player_id)