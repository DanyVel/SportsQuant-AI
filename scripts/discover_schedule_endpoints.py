"""
Discovery script for NBA schedule-related endpoints.
"""

from __future__ import annotations

from pprint import pprint

from nba_api.stats.endpoints import (
    LeagueGameFinder,
    ScoreboardV2,
    ScoreboardV3,
)


def inspect_endpoint(name: str, endpoint) -> None:
    print("=" * 100)
    print(f"ENDPOINT: {name}")
    print("=" * 100)

    dataframes = endpoint.get_data_frames()

    print(f"Number of DataFrames: {len(dataframes)}")

    for i, df in enumerate(dataframes):
        print("-" * 100)
        print(f"DataFrame #{i + 1}")

        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")

        print("\nColumns:")
        pprint(list(df.columns))

        print("\nDtypes:")
        print(df.dtypes)

        print("\nFirst rows:")
        print(df.head())

        print()


def main():

    endpoints = [
        (
            "LeagueGameFinder",
            LeagueGameFinder(
                season_nullable="2023-24",
                league_id_nullable="00",
            ),
        ),
        (
            "ScoreboardV2",
            ScoreboardV2(
                game_date="11/03/2023",
            ),
        ),
        (
            "ScoreboardV3",
            ScoreboardV3(
                game_date="2023-11-03",
            ),
        ),
    ]

    for name, endpoint in endpoints:
        try:
            inspect_endpoint(name, endpoint)
        except Exception as ex:
            print(f"\n{name} FAILED")
            print(type(ex).__name__)
            print(ex)
            print()


if __name__ == "__main__":
    main()