"""
NBA player parser.
"""

from __future__ import annotations

import pandas as pd

from sportsquant.models import Player


class PlayerParser:
    """
    Converts NBA API player data into domain models.
    """

    @staticmethod
    def parse_players(dataframe: pd.DataFrame) -> list[Player]:
        """
        Parse a DataFrame returned by CommonAllPlayers into Player objects.
        """
        players: list[Player] = []

        for row in dataframe.itertuples(index=False):
            players.append(
                Player(
                    id=row.PERSON_ID,
                    full_name=row.DISPLAY_FIRST_LAST,
                    is_active=row.ROSTERSTATUS == 1,
                )
            )

        return players