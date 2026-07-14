"""
Inspect Season-related nba_api endpoints.
"""

from inspect import signature

from sportsquant.clients.nba.endpoints import (
    LeagueStandingsV3,
    ScoreboardV3,
    TeamInfoCommon,
)

print("=" * 80)
print("LeagueStandingsV3")
print("=" * 80)
print(signature(LeagueStandingsV3))

print()

print("=" * 80)
print("TeamInfoCommon")
print("=" * 80)
print(signature(TeamInfoCommon))

print()

print("=" * 80)
print("ScoreboardV3")
print("=" * 80)
print(signature(ScoreboardV3))