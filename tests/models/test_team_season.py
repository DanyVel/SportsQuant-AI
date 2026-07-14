"""
Tests for TeamSeason.
"""

from sportsquant.models import Record
from sportsquant.models import TeamSeason


def test_team_season_creation() -> None:
    team_season = TeamSeason(
        season_id="22023",
        team_id=1610612738,
        record=Record(
            wins=64,
            losses=18,
        ),
    )

    assert team_season.team_id == 1610612738
    assert team_season.season_id == "22023"
    assert team_season.record.games_played == 82


def test_team_season_win_percentage() -> None:
    team_season = TeamSeason(
        season_id="22023",
        team_id=1610612738,
        record=Record(
            wins=64,
            losses=18,
        ),
    )

    assert team_season.win_percentage == 64 / 82

def test_has_winning_record() -> None:
    team_season = TeamSeason(
        season_id="22023",
        team_id=1610612738,
        record=Record(
            wins=64,
            losses=18,
        ),
    )

    assert team_season.has_winning_record is True