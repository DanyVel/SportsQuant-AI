"""
Game repository interface.
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable

from sportsquant.aggregates import Game
from sportsquant.repositories.base import BaseRepository


class GameRepository(BaseRepository):
    """
    Contract for game repositories.
    """

    @abstractmethod
    def get_by_id(
        self,
        game_id: str,
    ) -> Game | None:
        """
        Retrieve a Game aggregate by its identifier.

        Parameters
        ----------
        game_id : str
            NBA game identifier.

        Returns
        -------
        Game | None
            Game aggregate if found, otherwise None.
        """
        raise NotImplementedError

    @abstractmethod
    def get_ids_by_season(
        self,
        season: str,
    ) -> tuple[str, ...]:
        """
        Retrieve every game identifier for a season.

        Parameters
        ----------
        season : str
            NBA season (e.g. "2023-24").

        Returns
        -------
        tuple[str, ...]
            Tuple containing every game identifier
            for the requested season.
        """
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        game: Game,
    ) -> None:
        """
        Persist a Game aggregate.
        """
        raise NotImplementedError

    @abstractmethod
    def save_many(
        self,
        games: Iterable[Game],
    ) -> None:
        """
        Persist multiple Game aggregates.
        """
        raise NotImplementedError