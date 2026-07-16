"""
Team game feature enricher.
"""

from __future__ import annotations

from dataclasses import replace

from sportsquant.features.calculators import field_goal_percentage
from sportsquant.features.calculators import free_throw_percentage
from sportsquant.features.calculators import three_point_percentage
from sportsquant.features.team_game_feature import TeamGameFeature


def enrich_team_game_feature(
    feature: TeamGameFeature,
) -> TeamGameFeature:
    """
    Return a new TeamGameFeature with shooting percentage fields populated.

    The input feature is not mutated.
    """
    return replace(
        feature,
        field_goal_percentage=field_goal_percentage(
            feature.field_goals_made,
            feature.field_goals_attempted,
        ),
        three_point_percentage=three_point_percentage(
            feature.three_pointers_made,
            feature.three_pointers_attempted,
        ),
        free_throw_percentage=free_throw_percentage(
            feature.free_throws_made,
            feature.free_throws_attempted,
        ),
    )