"""
Tests for the Record value object.
"""

from sportsquant.models import Record


def test_games_played() -> None:
    record = Record(
        wins=64,
        losses=18,
    )

    assert record.games_played == 82


def test_win_percentage() -> None:
    record = Record(
        wins=64,
        losses=18,
    )

    assert record.win_percentage == 64 / 82


def test_negative_wins() -> None:
    try:
        Record(
            wins=-1,
            losses=10,
        )
        assert False
    except ValueError:
        assert True


def test_negative_losses() -> None:
    try:
        Record(
            wins=10,
            losses=-1,
        )
        assert False
    except ValueError:
        assert True