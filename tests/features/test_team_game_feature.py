"""
Tests for TeamGameFeature.
"""

from dataclasses import FrozenInstanceError
from datetime import date

import pytest

from sportsquant.features import TeamGameFeature


def test_team_game_feature_creation() -> None:
    """
    TeamGameFeature should be constructed with primitive values.
    """
    feature = TeamGameFeature(
        game_id="0022300001",
        game_date=date(
            2023,
            10,
            24,
        ),
        team_id=1610612738,
        opponent_team_id=1610612747,
        is_home=True,
        points=110,
        opponent_points=104,
        field_goals_made=40,
        field_goals_attempted=90,
        three_pointers_made=12,
        three_pointers_attempted=35,
        free_throws_made=18,
        free_throws_attempted=22,
        offensive_rebounds=10,
        defensive_rebounds=35,
        assists=25,
        steals=8,
        blocks=5,
        turnovers=12,
        personal_fouls=18,
    )

    assert isinstance(
        feature,
        TeamGameFeature,
    )


def test_team_game_feature_is_immutable() -> None:
    """
    TeamGameFeature should not allow field mutation.
    """
    feature = _make_team_game_feature()

    with pytest.raises(FrozenInstanceError):
        feature.points = 111


def test_team_game_feature_preserves_field_values() -> None:
    """
    TeamGameFeature should preserve assigned field values.
    """
    feature = _make_team_game_feature()

    assert feature.game_id == "0022300001"
    assert feature.game_date == date(
        2023,
        10,
        24,
    )
    assert feature.team_id == 1610612738
    assert feature.opponent_team_id == 1610612747
    assert feature.is_home is True
    assert feature.points == 110
    assert feature.opponent_points == 104
    assert feature.field_goals_made == 40
    assert feature.field_goals_attempted == 90
    assert feature.three_pointers_made == 12
    assert feature.three_pointers_attempted == 35
    assert feature.free_throws_made == 18
    assert feature.free_throws_attempted == 22
    assert feature.offensive_rebounds == 10
    assert feature.defensive_rebounds == 35
    assert feature.assists == 25
    assert feature.steals == 8
    assert feature.blocks == 5
    assert feature.turnovers == 12
    assert feature.personal_fouls == 18


def _make_team_game_feature() -> TeamGameFeature:
    return TeamGameFeature(
        game_id="0022300001",
        game_date=date(
            2023,
            10,
            24,
        ),
        team_id=1610612738,
        opponent_team_id=1610612747,
        is_home=True,
        points=110,
        opponent_points=104,
        field_goals_made=40,
        field_goals_attempted=90,
        three_pointers_made=12,
        three_pointers_attempted=35,
        free_throws_made=18,
        free_throws_attempted=22,
        offensive_rebounds=10,
        defensive_rebounds=35,
        assists=25,
        steals=8,
        blocks=5,
        turnovers=12,
        personal_fouls=18,
    )
