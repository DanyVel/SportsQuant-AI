"""
Parser for NBA game summaries.
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd

from sportsquant.models import GameSummary


class GameSummaryParser:
    """
    Converts BoxScoreSummaryV3 datasets into a GameSummary domain model.
    """

    @staticmethod
    def parse(
        game: pd.DataFrame,
        game_info: pd.DataFrame,
        line_score: pd.DataFrame,
    ) -> GameSummary:
        """
        Parse the BoxScoreSummaryV3 datasets into a GameSummary.

        Parameters
        ----------
        game
            Dataset 1 returned by BoxScoreSummaryV3.
        game_info
            Dataset 2 returned by BoxScoreSummaryV3.
        line_score
            Dataset 5 returned by BoxScoreSummaryV3.

        Returns
        -------
        GameSummary
        """

        game_row = game.iloc[0]
        info_row = game_info.iloc[0]

        home_team = line_score.loc[
            line_score["teamId"] == game_row["homeTeamId"]
        ].iloc[0]

        away_team = line_score.loc[
            line_score["teamId"] == game_row["awayTeamId"]
        ].iloc[0]

        game_date = datetime.fromisoformat(
            info_row["gameDate"].replace("Z", "+00:00")
        ).date()

        matchup = (
            f"{away_team['teamTricode']} @ "
            f"{home_team['teamTricode']}"
        )

        return GameSummary(
            game_id=game_row["gameId"],
            game_date=game_date,
            home_team_id=int(game_row["homeTeamId"]),
            away_team_id=int(game_row["awayTeamId"]),
            matchup=matchup,
        )