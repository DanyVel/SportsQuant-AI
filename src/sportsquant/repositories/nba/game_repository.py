"""
NBA Game repository implementation.
"""

from __future__ import annotations

from sportsquant.aggregates import Game
from sportsquant.providers import NBAProvider
from sportsquant.repositories import GameRepository


class NBAGameRepository(GameRepository):
    """
    NBA implementation of the GameRepository contract.
    """

    def __init__(
        self,
        provider: NBAProvider | None = None,
    ) -> None:
        """
        Initialize the repository.
        """
        self._provider = provider or NBAProvider()

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
            Complete Game aggregate if the game exists,
            otherwise None.
        """
        summary = self._provider.get_game_summary(
            game_id,
        )

        player_stats = self._provider.get_player_game_stats(
            game_id,
        )

        team_stats = self._provider.get_team_game_stats(
            game_id,
        )

        if len(team_stats) != 2:
            return None

        home_team_stats = next(
            stats
            for stats in team_stats
            if stats.team_id == summary.home_team_id
        )

        away_team_stats = next(
            stats
            for stats in team_stats
            if stats.team_id == summary.away_team_id
        )

        return Game(
            summary=summary,
            home_team_stats=home_team_stats,
            away_team_stats=away_team_stats,
            player_stats=tuple(player_stats),
        )

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
            Tuple containing every game identifier.
        """
        return self._provider.get_game_ids_by_season(
            season,
        )