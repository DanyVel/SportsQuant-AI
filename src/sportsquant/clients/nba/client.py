"""
NBA Stats API client.
"""

from __future__ import annotations

from sportsquant.clients.base_client import BaseClient
from sportsquant.clients.nba.constants import (
    NBA_BASE_URL,
    NBA_HEADERS,
    NBAEndpoint,
)
from sportsquant.clients.nba.endpoints import (
    BoxScoreSummaryV3,
    BoxScoreTraditionalV3,
    CommonAllPlayers,
    LeagueGameFinder,
    LeagueStandingsV3,
    PlayByPlayV3,
    ScoreboardV3,
    TeamInfoCommon,
    teams,
)
from sportsquant.data.models import ResponseData


class NBAClient(BaseClient):
    """
    Client for interacting with the NBA Stats API.
    """

    def __init__(self) -> None:
        """
        Initialize the NBA API client.
        """
        super().__init__(
            base_url=NBA_BASE_URL,
            default_headers=NBA_HEADERS,
        )

    def get_scoreboard(self) -> ResponseData:
        """
        Retrieve the NBA scoreboard.

        Returns
        -------
        ResponseData
            Scoreboard endpoint response.
        """
        return self.get(endpoint=NBAEndpoint.SCOREBOARD.value)

    def get_team_years(self) -> ResponseData:
        """
        Retrieve NBA team history.

        Returns
        -------
        ResponseData
            Team history endpoint response.
        """
        return self.get(endpoint=NBAEndpoint.TEAM_YEARS.value)

    def get_player_stats(self) -> ResponseData:
        """
        Retrieve league player statistics.

        Returns
        -------
        ResponseData
            League player statistics.
        """
        return self.get(endpoint=NBAEndpoint.PLAYER_STATS.value)

    def get_teams(self) -> list[dict]:
        """
        Retrieve all NBA teams using nba_api.

        Returns
        -------
        list[dict]
            List containing information for all NBA franchises.
        """
        return teams.get_teams()

    def get_players(self) -> CommonAllPlayers:
        """
        Retrieve all NBA players using nba_api.

        Returns
        -------
        CommonAllPlayers
            Raw CommonAllPlayers endpoint object.
        """
        return CommonAllPlayers()

    def get_league_game_finder(
        self,
        season: str,
    ) -> LeagueGameFinder:
        """
        Retrieve a LeagueGameFinder endpoint for a season.

        Parameters
        ----------
        season : str
            NBA season (e.g. "2023-24").

        Returns
        -------
        LeagueGameFinder
            Raw LeagueGameFinder endpoint object.
        """
        return LeagueGameFinder(
            season_nullable=season,
            league_id_nullable="00",
        )

    def get_boxscore_summary(
        self,
        game_id: str,
    ) -> BoxScoreSummaryV3:
        """
        Retrieve a BoxScoreSummaryV3 endpoint.

        Parameters
        ----------
        game_id : str
            NBA game identifier.

        Returns
        -------
        BoxScoreSummaryV3
            Raw BoxScoreSummaryV3 endpoint object.
        """
        return BoxScoreSummaryV3(
            game_id=game_id,
        )

    def get_boxscore_traditional(
        self,
        game_id: str,
    ) -> BoxScoreTraditionalV3:
        """
        Retrieve a BoxScoreTraditionalV3 endpoint.

        Parameters
        ----------
        game_id : str
            NBA game identifier.

        Returns
        -------
        BoxScoreTraditionalV3
            Raw BoxScoreTraditionalV3 endpoint object.
        """
        return BoxScoreTraditionalV3(
            game_id=game_id,
        )

    def get_play_by_play(
        self,
        game_id: str,
    ) -> PlayByPlayV3:
        """
        Retrieve a PlayByPlayV3 endpoint.

        Parameters
        ----------
        game_id : str
            NBA game identifier.

        Returns
        -------
        PlayByPlayV3
            Raw PlayByPlayV3 endpoint object.
        """
        return PlayByPlayV3(
            game_id=game_id,
        )

    def get_league_standings(
        self,
        season: str,
    ) -> LeagueStandingsV3:
        """
        Retrieve a LeagueStandingsV3 endpoint.

        Parameters
        ----------
        season : str
            NBA season (e.g. "2023-24").

        Returns
        -------
        LeagueStandingsV3
            Raw LeagueStandingsV3 endpoint object.
        """
        return LeagueStandingsV3(
            season=season,
        )

    def get_team_info_common(
        self,
        team_id: int,
        season: str,
    ) -> TeamInfoCommon:
        """
        Retrieve a TeamInfoCommon endpoint.

        Parameters
        ----------
        team_id : int
            NBA team identifier.

        season : str
            NBA season (e.g. "2023-24").

        Returns
        -------
        TeamInfoCommon
            Raw TeamInfoCommon endpoint object.
        """
        return TeamInfoCommon(
            team_id=team_id,
            season_nullable=season,
        )

    def get_scoreboard_v3(
        self,
        game_date: str,
    ) -> ScoreboardV3:
        """
        Retrieve a ScoreboardV3 endpoint.

        Parameters
        ----------
        game_date : str
            Date formatted as YYYY-MM-DD.

        Returns
        -------
        ScoreboardV3
            Raw ScoreboardV3 endpoint object.
        """
        return ScoreboardV3(
            game_date=game_date,
        )