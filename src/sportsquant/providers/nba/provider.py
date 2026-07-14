"""
NBA data provider.
"""

from __future__ import annotations

from sportsquant.clients.nba import NBAClient
from sportsquant.clients.nba.endpoints import CommonAllPlayers
from sportsquant.models import (
    GameSummary,
    Player,
    PlayerGameStats,
    Record,
    Standing,
    Team,
    TeamGameStats,
)
from sportsquant.parsers.nba import (
    GameSummaryParser,
    PlayerGameStatsParser,
    PlayerParser,
    StandingParser,
    TeamGameStatsParser,
    TeamInfoParser,
)
from sportsquant.providers.base import BaseProvider


class NBAProvider(BaseProvider):
    """
    Provides NBA domain objects.
    """

    def __init__(self) -> None:
        """
        Initialize the NBA provider.
        """
        self._client = NBAClient()

    def _build_team(
        self,
        team_data: dict,
    ) -> Team:
        """
        Build a Team domain model from raw NBA API data.
        """
        return Team(
            id=team_data["id"],
            full_name=team_data["full_name"],
            abbreviation=team_data["abbreviation"],
            city=team_data["city"],
            nickname=team_data["nickname"],
            state=team_data["state"],
            year_founded=team_data["year_founded"],
        )

    def get_teams(self) -> list[Team]:
        """
        Retrieve all NBA teams.
        """
        return [
            self._build_team(team)
            for team in self._client.get_teams()
        ]

    def get_players_data(self) -> CommonAllPlayers:
        """
        Retrieve the raw CommonAllPlayers endpoint.
        """
        return self._client.get_players()

    def get_players(self) -> list[Player]:
        """
        Retrieve all NBA players.
        """
        endpoint = self.get_players_data()

        dataframe = endpoint.get_data_frames()[0]

        return PlayerParser.parse_players(
            dataframe,
        )

    def get_player_game_stats(
        self,
        game_id: str,
    ) -> list[PlayerGameStats]:
        """
        Retrieve player statistics for a game.
        """
        endpoint = self._client.get_boxscore_traditional(
            game_id=game_id,
        )

        return PlayerGameStatsParser.parse_player_stats(
            endpoint.get_data_frames()[0],
        )

    def get_team_game_stats(
        self,
        game_id: str,
    ) -> list[TeamGameStats]:
        """
        Retrieve team statistics for a game.
        """
        endpoint = self._client.get_boxscore_traditional(
            game_id=game_id,
        )

        return TeamGameStatsParser.parse_team_stats(
            endpoint.get_data_frames()[2],
        )

    def get_game_summary(
        self,
        game_id: str,
    ) -> GameSummary:
        """
        Retrieve summary information for a game.
        """
        endpoint = self._client.get_boxscore_summary(
            game_id=game_id,
        )

        dataframes = endpoint.get_data_frames()

        return GameSummaryParser.parse(
            game=dataframes[0],
            game_info=dataframes[1],
            line_score=dataframes[4],
        )

    def get_game_ids_by_season(
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
            Unique game identifiers sorted in ascending order.
        """
        endpoint = self._client.get_league_game_finder(
            season=season,
        )

        dataframe = endpoint.get_data_frames()[0]

        return tuple(
            sorted(
                dataframe["GAME_ID"].unique(),
            )
        )

    def get_team_record(
        self,
        team_id: int,
        season: str,
    ) -> Record:
        """
        Retrieve a team's season record.
        """
        endpoint = self._client.get_team_info_common(
            team_id=team_id,
            season=season,
        )

        dataframe = endpoint.get_data_frames()[0]

        return TeamInfoParser.parse(
            dataframe,
        )

    def get_team_standing(
        self,
        team_id: int,
        season: str,
    ) -> Standing | None:
        """
        Retrieve a team's standing.
        """
        endpoint = self._client.get_league_standings(
            season=season,
        )

        dataframe = endpoint.get_data_frames()[0]

        standings = StandingParser.parse(
            dataframe,
        )

        try:
            index = dataframe["TeamID"].tolist().index(team_id)
        except ValueError:
            return None

        return standings[index]