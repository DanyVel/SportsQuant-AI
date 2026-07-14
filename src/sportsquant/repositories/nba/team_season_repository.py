"""
NBA TeamSeason repository implementation.
"""

from __future__ import annotations

from sportsquant.models import TeamSeason
from sportsquant.providers import NBAProvider
from sportsquant.repositories import TeamSeasonRepository


class NBATeamSeasonRepository(TeamSeasonRepository):
    """
    NBA implementation of the TeamSeasonRepository contract.
    """

    def __init__(
        self,
        provider: NBAProvider | None = None,
    ) -> None:
        """
        Initialize the repository.
        """
        self._provider = provider or NBAProvider()

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
            NBA season identifier.

        Returns
        -------
        TeamSeason | None
            TeamSeason aggregate if found.
        """
        #
        # La NBA API usa el formato "2023-24"
        # mientras que nuestro dominio usa "22023".
        #
        season = f"{season_id[1:5]}-{str(int(season_id[1:5]) + 1)[2:]}"

        record = self._provider.get_team_record(
            team_id=team_id,
            season=season,
        )

        standing = self._provider.get_team_standing(
            team_id=team_id,
            season=season,
        )

        return TeamSeason(
            season_id=season_id,
            team_id=team_id,
            record=record,
            standing=standing,
        )