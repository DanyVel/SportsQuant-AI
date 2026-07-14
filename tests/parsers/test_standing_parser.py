"""
Tests for StandingParser.
"""

from __future__ import annotations

import pandas as pd

from sportsquant.models import Standing
from sportsquant.parsers.nba import StandingParser


def test_parse_standing() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "PlayoffRank": 1,
                "DivisionRank": 1,
                "LeagueRank": 2,
            }
        ]
    )

    standings = StandingParser.parse(dataframe)

    assert len(standings) == 1

    standing = standings[0]

    assert isinstance(standing, Standing)
    assert standing.conference_rank == 1
    assert standing.division_rank == 1
    assert standing.league_rank == 2