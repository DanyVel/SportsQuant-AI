"""
Validate the TeamGameStats parser using LeagueGameFinder.
"""

from __future__ import annotations

from nba_api.stats.endpoints import LeagueGameFinder

from sportsquant.parsers.nba import TeamGameStatsParser


GAME_ID = "0022300001"


def main() -> None:
    """
    Execute the parser validation.
    """
    endpoint = LeagueGameFinder(game_id_nullable=GAME_ID)

    dataframe = endpoint.get_data_frames()[0]

    team_stats = TeamGameStatsParser.parse_team_stats(dataframe)

    print("=" * 80)
    print(f"GAME_ID: {GAME_ID}")
    print("=" * 80)
    print()

    print(f"Rows returned by endpoint : {len(dataframe)}")
    print(f"Parsed TeamGameStats      : {len(team_stats)}")
    print()

    for stats in team_stats:
        print(stats)
        print("-" * 80)


if __name__ == "__main__":
    main()