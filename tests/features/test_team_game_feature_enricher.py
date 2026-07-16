"""
Tests for enrich_team_game_feature.
"""

from __future__ import annotations

from datetime import date

from sportsquant.features.team_game_feature import TeamGameFeature
from sportsquant.features.team_game_feature_enricher import (
    enrich_team_game_feature,
)


def test_enrich_team_game_feature_populates_shooting_percentages() -> None:
    """
    enrich_team_game_feature should populate the shooting percentage fields
    using the existing calculators.
    """
    feature = _make_team_game_feature(
        field_goals_made=9,
        field_goals_attempted=18,
        three_pointers_made=5,
        three_pointers_attempted=10,
        free_throws_made=8,
        free_throws_attempted=10,
    )

    enriched = enrich_team_game_feature(feature)

    assert enriched.field_goal_percentage == 0.5
    assert enriched.three_point_percentage == 0.5
    assert enriched.free_throw_percentage == 0.8


def test_enrich_team_game_feature_handles_zero_attempts() -> None:
    """
    enrich_team_game_feature should return zero percentages when attempts
    are zero, matching the calculators' safe-divide behavior.
    """
    feature = _make_team_game_feature(
        field_goals_made=0,
        field_goals_attempted=0,
        three_pointers_made=0,
        three_pointers_attempted=0,
        free_throws_made=0,
        free_throws_attempted=0,
    )

    enriched = enrich_team_game_feature(feature)

    assert enriched.field_goal_percentage == 0
    assert enriched.three_point_percentage == 0
    assert enriched.free_throw_percentage == 0


def test_enrich_team_game_feature_does_not_mutate_input() -> None:
    """
    enrich_team_game_feature should return a new instance and leave the
    original feature untouched.
    """
    feature = _make_team_game_feature(
        field_goals_made=9,
        field_goals_attempted=18,
        three_pointers_made=5,
        three_pointers_attempted=10,
        free_throws_made=8,
        free_throws_attempted=10,
    )

    enriched = enrich_team_game_feature(feature)

    assert enriched is not feature
    assert feature.field_goal_percentage == 0.0
    assert feature.three_point_percentage == 0.0
    assert feature.free_throw_percentage == 0.0


def test_enrich_team_game_feature_preserves_other_fields() -> None:
    """
    enrich_team_game_feature should not alter any non-shooting-percentage
    fields on the returned feature.
    """
    feature = _make_team_game_feature(
        field_goals_made=9,
        field_goals_attempted=18,
        three_pointers_made=5,
        three_pointers_attempted=10,
        free_throws_made=8,
        free_throws_attempted=10,
    )

    enriched = enrich_team_game_feature(feature)

    assert enriched.game_id == feature.game_id
    assert enriched.game_date == feature.game_date
    assert enriched.team_id == feature.team_id
    assert enriched.opponent_team_id == feature.opponent_team_id
    assert enriched.is_home == feature.is_home
    assert enriched.points == feature.points
    assert enriched.opponent_points == feature.opponent_points
    assert enriched.field_goals_made == feature.field_goals_made
    assert enriched.field_goals_attempted == feature.field_goals_attempted
    assert enriched.three_pointers_made == feature.three_pointers_made
    assert (
        enriched.three_pointers_attempted
        == feature.three_pointers_attempted
    )
    assert enriched.free_throws_made == feature.free_throws_made
    assert enriched.free_throws_attempted == feature.free_throws_attempted
    assert enriched.offensive_rebounds == feature.offensive_rebounds
    assert enriched.defensive_rebounds == feature.defensive_rebounds
    assert enriched.assists == feature.assists
    assert enriched.steals == feature.steals
    assert enriched.blocks == feature.blocks
    assert enriched.turnovers == feature.turnovers
    assert enriched.personal_fouls == feature.personal_fouls


def _make_team_game_feature(
    field_goals_made: int,
    field_goals_attempted: int,
    three_pointers_made: int,
    three_pointers_attempted: int,
    free_throws_made: int,
    free_throws_attempted: int,
) -> TeamGameFeature:
    return TeamGameFeature(
        game_id="0022300001",
        game_date=date(2023, 10, 24),
        team_id=1610612738,
        opponent_team_id=1610612747,
        is_home=True,
        points=110,
        opponent_points=104,
        field_goals_made=field_goals_made,
        field_goals_attempted=field_goals_attempted,
        three_pointers_made=three_pointers_made,
        three_pointers_attempted=three_pointers_attempted,
        free_throws_made=free_throws_made,
        free_throws_attempted=free_throws_attempted,
        offensive_rebounds=10,
        defensive_rebounds=35,
        assists=25,
        steals=8,
        blocks=5,
        turnovers=12,
        personal_fouls=18,
    )