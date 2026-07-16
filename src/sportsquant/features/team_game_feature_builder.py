"""
Build team game features from game aggregates.
"""

from __future__ import annotations

from sportsquant.aggregates import Game
from sportsquant.features.team_game_feature import TeamGameFeature
from sportsquant.models import GameSummary
from sportsquant.models import TeamGameStats


def team_game_features_from_game(
    game: Game,
) -> tuple[TeamGameFeature, TeamGameFeature]:
    """
    Build team game features for both teams in a game.
    """
    return (
        _build_feature(
            summary=game.summary,
            team_stats=game.home_team_stats,
            opponent_stats=game.away_team_stats,
            is_home=True,
        ),
        _build_feature(
            summary=game.summary,
            team_stats=game.away_team_stats,
            opponent_stats=game.home_team_stats,
            is_home=False,
        ),
    )


def _build_feature(
    summary: GameSummary,
    team_stats: TeamGameStats,
    opponent_stats: TeamGameStats,
    is_home: bool,
) -> TeamGameFeature:
    opponent_team_id = (
        summary.away_team_id
        if is_home
        else summary.home_team_id
    )

    return TeamGameFeature(
        game_id=summary.game_id,
        game_date=summary.game_date,
        team_id=team_stats.team_id,
        opponent_team_id=opponent_team_id,
        is_home=is_home,
        points=team_stats.points,
        opponent_points=opponent_stats.points,
        field_goals_made=team_stats.field_goals_made,
        field_goals_attempted=team_stats.field_goals_attempted,
        three_pointers_made=team_stats.three_pointers_made,
        three_pointers_attempted=team_stats.three_pointers_attempted,
        free_throws_made=team_stats.free_throws_made,
        free_throws_attempted=team_stats.free_throws_attempted,
        offensive_rebounds=team_stats.offensive_rebounds,
        defensive_rebounds=team_stats.defensive_rebounds,
        assists=team_stats.assists,
        steals=team_stats.steals,
        blocks=team_stats.blocks,
        turnovers=team_stats.turnovers,
        personal_fouls=team_stats.personal_fouls,
    )
