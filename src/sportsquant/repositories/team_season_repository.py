"""
TeamSeason repository interface.
"""

from __future__ import annotations

from abc import abstractmethod

from sportsquant.models import TeamSeason
from sportsquant.repositories.base import BaseRepository


class TeamSeasonRepository(BaseRepository):
    """
    Contract for TeamSeason repositories.
    """

    @abstractmethod
    def get_by_team_and_season(
        self,
        team_id: int,
        season_id: str,
    ) -> TeamSeason | None:
        """
        Retrieve a TeamSeason aggregate.

        Parameters
        ----------
        team_id : int
            NBA team identifier.

        season_id : str
            NBA season identifier (e.g. "22023").

        Returns
        -------
        TeamSeason | None
            TeamSeason aggregate if found, otherwise None.
        """
        raise NotImplementedError