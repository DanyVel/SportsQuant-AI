"""
Standing parser.
"""

from __future__ import annotations

import pandas as pd

from sportsquant.models import Standing


class StandingParser:
    """
    Parses LeagueStandingsV3 data into Standing domain models.
    """

    @staticmethod
    def _optional_int(
        value: object,
    ) -> int | None:
        """
        Convert a numeric NBA API value into an integer.

        Returns
        -------
        int | None
            Parsed integer or None if the value is missing.
        """
        if pd.isna(value):
            return None

        return int(value)

    @classmethod
    def parse(
        cls,
        dataframe: pd.DataFrame,
    ) -> list[Standing]:
        """
        Parse standings from a LeagueStandingsV3 dataframe.

        Parameters
        ----------
        dataframe : pd.DataFrame
            League standings dataframe.

        Returns
        -------
        list[Standing]
            Parsed standings.
        """
        standings: list[Standing] = []

        for row in dataframe.itertuples(index=False):
            standings.append(
                Standing(
                    conference_rank=int(row.PlayoffRank),
                    division_rank=int(row.DivisionRank),
                    league_rank=cls._optional_int(
                        row.LeagueRank,
                    ),
                )
            )

        return standings