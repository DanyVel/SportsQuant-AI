"""
Tests for TeamInfoParser.
"""

from __future__ import annotations

import pandas as pd

from sportsquant.models import Record
from sportsquant.parsers.nba import TeamInfoParser


def test_parse_team_info() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "W": 64,
                "L": 18,
            }
        ]
    )

    record = TeamInfoParser.parse(dataframe)

    assert isinstance(record, Record)
    assert record.wins == 64
    assert record.losses == 18
    assert record.games_played == 82