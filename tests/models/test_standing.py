"""
Tests for Standing.
"""

import pytest

from sportsquant.models import Standing


def test_standing_creation() -> None:
    standing = Standing(
        conference_rank=1,
        division_rank=1,
        league_rank=2,
    )

    assert standing.conference_rank == 1
    assert standing.division_rank == 1
    assert standing.league_rank == 2


def test_invalid_conference_rank() -> None:
    with pytest.raises(ValueError):
        Standing(
            conference_rank=0,
            division_rank=1,
            league_rank=1,
        )