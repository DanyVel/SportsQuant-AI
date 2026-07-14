from sportsquant.models import Streak


def test_winning_streak() -> None:
    streak = Streak(5)

    assert streak.is_winning is True
    assert streak.is_losing is False
    assert streak.games == 5


def test_losing_streak() -> None:
    streak = Streak(-3)

    assert streak.is_winning is False
    assert streak.is_losing is True
    assert streak.games == 3


def test_no_streak() -> None:
    streak = Streak(0)

    assert streak.is_winning is False
    assert streak.is_losing is False
    assert streak.games == 0