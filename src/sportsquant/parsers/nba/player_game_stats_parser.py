"""
NBA player game statistics parser.
"""

from __future__ import annotations

import pandas as pd

from sportsquant.models import PlayerGameStats


class PlayerGameStatsParser:
    """
    Converts BoxScoreTraditionalV3 player statistics into
    PlayerGameStats domain models.
    """

    @staticmethod
    def parse_player_stats(dataframe: pd.DataFrame) -> list[PlayerGameStats]:
        """
        Parse a BoxScoreTraditionalV3 DataFrame into
        PlayerGameStats objects.
        """
        player_stats: list[PlayerGameStats] = []

        for row in dataframe.itertuples(index=False):
            player_stats.append(
                PlayerGameStats(
                    game_id=row.gameId,
                    player_id=row.personId,
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

        return player_stats