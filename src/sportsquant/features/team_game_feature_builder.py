"""
Build team game features from game aggregates.
"""

from __future__ import annotations

from sportsquant.aggregates import Game
from sportsquant.features.team_game_feature import TeamGameFeature


def team_game_features_from_game(
    game: Game,
) -> tuple[TeamGameFeature, TeamGameFeature]:
    """
    Build team game features for both teams in a game.
    """
    return (
        TeamGameFeature(
            game_id=game.summary.game_id,
            game_date=game.summary.game_date,
            team_id=game.home_team_stats.team_id,
            opponent_team_id=game.summary.away_team_id,
            is_home=True,
            points=game.home_team_stats.points,
            opponent_points=game.away_team_stats.points,
            field_goals_made=game.home_team_stats.field_goals_made,
            field_goals_attempted=game.home_team_stats.field_goals_attempted,
            three_pointers_made=game.home_team_stats.three_pointers_made,
            three_pointers_attempted=(
                game.home_team_stats.three_pointers_attempted
            ),
            free_throws_made=game.home_team_stats.free_throws_made,
            free_throws_attempted=game.home_team_stats.free_throws_attempted,
            offensive_rebounds=game.home_team_stats.offensive_rebounds,
            defensive_rebounds=game.home_team_stats.defensive_rebounds,
            assists=game.home_team_stats.assists,
            steals=game.home_team_stats.steals,
            blocks=game.home_team_stats.blocks,
            turnovers=game.home_team_stats.turnovers,
            personal_fouls=game.home_team_stats.personal_fouls,
        ),
        TeamGameFeature(
            game_id=game.summary.game_id,
            game_date=game.summary.game_date,
            team_id=game.away_team_stats.team_id,
            opponent_team_id=game.summary.home_team_id,
            is_home=False,
            points=game.away_team_stats.points,
            opponent_points=game.home_team_stats.points,
            field_goals_made=game.away_team_stats.field_goals_made,
            field_goals_attempted=game.away_team_stats.field_goals_attempted,
            three_pointers_made=game.away_team_stats.three_pointers_made,
            three_pointers_attempted=(
                game.away_team_stats.three_pointers_attempted
            ),
            free_throws_made=game.away_team_stats.free_throws_made,
            free_throws_attempted=game.away_team_stats.free_throws_attempted,
            offensive_rebounds=game.away_team_stats.offensive_rebounds,
            defensive_rebounds=game.away_team_stats.defensive_rebounds,
            assists=game.away_team_stats.assists,
            steals=game.away_team_stats.steals,
            blocks=game.away_team_stats.blocks,
            turnovers=game.away_team_stats.turnovers,
            personal_fouls=game.away_team_stats.personal_fouls,
        ),
    )
