"""
Basic integration test for the NBA provider.
"""

from __future__ import annotations

from sportsquant.providers.nba import NBAProvider


def main() -> None:
    """
    Run provider integration test.
    """

    provider = NBAProvider()

    teams = provider.get_teams()

    print("=" * 60)
    print("SportsQuant-AI Provider Test")
    print("=" * 60)

    print(f"Retrieved {len(teams)} Team objects.\n")

    print("First five teams:\n")

    for team in teams[:5]:
        print(team)
        print("-" * 60)


if __name__ == "__main__":
    main()
    