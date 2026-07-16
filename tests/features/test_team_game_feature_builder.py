"""
Tests for team game feature builder.
"""

from datetime import date

from sportsquant.aggregates import Game
from sportsquant.features.team_game_feature_builder import (
    team_game_features_from_game,
)
from sportsquant.models import GameSummary
from sportsquant.models import TeamGameStats


def test_team_game_features_from_game_builds_two_features() -> None:
    """
    Builder should create one feature for each team.
    """
    features = team_game_features_from_game(
        _make_game(),
    )

    assert len(features) == 2


def test_team_game_features_from_game_assigns_home_and_away() -> None:
    """
    Builder should preserve home and away team assignments.
    """
    home_feature, away_feature = team_game_features_from_game(
        _make_game(),
    )

    assert home_feature.team_id == 1610612738
    assert away_feature.team_id == 1610612747


def test_team_game_features_from_game_assigns_opponent_team_ids() -> None:
    """
    Builder should assign the opposite team as opponent.
    """
    home_feature, away_feature = team_game_features_from_game(
        _make_game(),
    )

    assert home_feature.opponent_team_id == 1610612747
    assert away_feature.opponent_team_id == 1610612738


def test_team_game_features_from_game_assigns_opponent_points() -> None:
    """
    Builder should assign opponent points from the opposite team stats.
    """
    home_feature, away_feature = team_game_features_from_game(
        _make_game(),
    )

    assert home_feature.opponent_points == 104
    assert away_feature.opponent_points == 110


def test_team_game_features_from_game_assigns_home_flags() -> None:
    """
    Builder should mark home and away features correctly.
    """
    home_feature, away_feature = team_game_features_from_game(
        _make_game(),
    )

    assert home_feature.is_home is True
    assert away_feature.is_home is False


def test_team_game_features_from_game_preserves_base_stats() -> None:
    """
    Builder should copy base stats from TeamGameStats.
    """
    home_feature, away_feature = team_game_features_from_game(
        _make_game(),
    )

    assert home_feature.points == 110
    assert home_feature.field_goals_made == 40
    assert home_feature.field_goals_attempted == 90
    assert home_feature.three_pointers_made == 12
    assert home_feature.three_pointers_attempted == 35
    assert home_feature.free_throws_made == 18
    assert home_feature.free_throws_attempted == 22
    assert home_feature.offensive_rebounds == 10
    assert home_feature.defensive_rebounds == 35
    assert home_feature.assists == 25
    assert home_feature.steals == 8
    assert home_feature.blocks == 5
    assert home_feature.turnovers == 12
    assert home_feature.personal_fouls == 18

    assert away_feature.points == 104
    assert away_feature.field_goals_made == 38
    assert away_feature.field_goals_attempted == 88
    assert away_feature.three_pointers_made == 10
    assert away_feature.three_pointers_attempted == 30
    assert away_feature.free_throws_made == 18
    assert away_feature.free_throws_attempted == 20
    assert away_feature.offensive_rebounds == 9
    assert away_feature.defensive_rebounds == 32
    assert away_feature.assists == 22
    assert away_feature.steals == 7
    assert away_feature.blocks == 4
    assert away_feature.turnovers == 13
    assert away_feature.personal_fouls == 19


def _make_game() -> Game:
    return Game(
        summary=GameSummary(
            game_id="0022300001",
            game_date=date(
                2023,
                10,
                24,
            ),
            home_team_id=1610612738,
            away_team_id=1610612747,
            matchup="BOS @ LAL",
        ),
        home_team_stats=_make_team_game_stats(
            team_id=1610612738,
            points=110,
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
        ),
        away_team_stats=_make_team_game_stats(
            team_id=1610612747,
            points=104,
            field_goals_made=38,
            field_goals_attempted=88,
            three_pointers_made=10,
            three_pointers_attempted=30,
            free_throws_made=18,
            free_throws_attempted=20,
            offensive_rebounds=9,
            defensive_rebounds=32,
            assists=22,
            steals=7,
            blocks=4,
            turnovers=13,
            personal_fouls=19,
        ),
        player_stats=(),
    )


def _make_team_game_stats(
    team_id: int,
    points: int,
    field_goals_made: int,
    field_goals_attempted: int,
    three_pointers_made: int,
    three_pointers_attempted: int,
    free_throws_made: int,
    free_throws_attempted: int,
    offensive_rebounds: int,
    defensive_rebounds: int,
    assists: int,
    steals: int,
    blocks: int,
    turnovers: int,
    personal_fouls: int,
) -> TeamGameStats:
    return TeamGameStats(
        game_id="0022300001",
        team_id=team_id,
        minutes="240",
        points=points,
        field_goals_made=field_goals_made,
        field_goals_attempted=field_goals_attempted,
        three_pointers_made=three_pointers_made,
        three_pointers_attempted=three_pointers_attempted,
        free_throws_made=free_throws_made,
        free_throws_attempted=free_throws_attempted,
        offensive_rebounds=offensive_rebounds,
        defensive_rebounds=defensive_rebounds,
        rebounds=offensive_rebounds + defensive_rebounds,
        assists=assists,
        steals=steals,
        blocks=blocks,
        turnovers=turnovers,
        personal_fouls=personal_fouls,
    )
