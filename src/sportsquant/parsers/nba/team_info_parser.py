"""
TeamInfo parser.
"""

from __future__ import annotations

import pandas as pd

from sportsquant.models import Record


class TeamInfoParser:
    """
    Parses TeamInfoCommon data into Record value objects.
    """

    @staticmethod
    def parse(
        dataframe: pd.DataFrame,
    ) -> Record:
        """
        Parse a team's season record.

        Parameters
        ----------
        dataframe : pd.DataFrame
            TeamInfoCommon dataframe.

        Returns
        -------
        Record
            Parsed team record.
        """
        row = dataframe.iloc[0]

        return Record(
            wins=int(row["W"]),
            losses=int(row["L"]),
        )