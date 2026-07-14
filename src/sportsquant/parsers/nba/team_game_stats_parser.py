"""
NBA team game statistics parser.
"""

from __future__ import annotations

import pandas as pd

from sportsquant.models import TeamGameStats


class TeamGameStatsParser:
    """
    Converts BoxScoreTraditionalV3 team statistics into
    TeamGameStats domain models.
    """

    @staticmethod
    def parse_team_stats(dataframe: pd.DataFrame) -> list[TeamGameStats]:
        """
        Parse a BoxScoreTraditionalV3 DataFrame into
        TeamGameStats objects.
        """
        team_stats: list[TeamGameStats] = []

        for row in dataframe.itertuples(index=False):
            team_stats.append(
                TeamGameStats(
                    game_id=row.gameId,
                    team_id=row.teamId,
                    minutes=row.minutes,
                    points=row.points,
                    field_goals_made=row.fieldGoalsMade,
                    field_goals_attempted=row.fieldGoalsAttempted,
                    three_pointers_made=row.threePointersMade,
                    three_pointers_attempted=row.threePointersAttempted,
                    free_throws_made=row.freeThrowsMade,
                    free_throws_attempted=row.freeThrowsAttempted,
                    offensive_rebounds=row.reboundsOffensive,
                    defensive_rebounds=row.reboundsDefensive,
                    rebounds=row.reboundsTotal,
                    assists=row.assists,
                    steals=row.steals,
                    blocks=row.blocks,
                    turnovers=row.turnovers,
                    personal_fouls=row.foulsPersonal,
                )
            )

        return team_stats