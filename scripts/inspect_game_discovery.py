"""
Inspect the endpoint used for season game discovery.
"""

from nba_api.stats.endpoints import LeagueGameFinder


def main() -> None:
    endpoint = LeagueGameFinder(
        season_nullable="2023-24",
        league_id_nullable="00",
    )

    dataframe = endpoint.get_data_frames()[0]

    print("=" * 80)
    print("ROWS")
    print("=" * 80)
    print(len(dataframe))

    print()

    print("=" * 80)
    print("COLUMNS")
    print("=" * 80)
    print(dataframe.columns.tolist())

    print()

    print("=" * 80)
    print("UNIQUE GAME IDS")
    print("=" * 80)
    print(dataframe["GAME_ID"].nunique())

    print()

    print("=" * 80)
    print("FIRST ROWS")
    print("=" * 80)
    print(
        dataframe[
            [
                "GAME_ID",
                "GAME_DATE",
                "MATCHUP",
                "TEAM_ID",
            ]
        ].head(20)
    )


if __name__ == "__main__":
    main()