"""
Discovery script for NBA standings endpoints.
"""

from __future__ import annotations

from pprint import pprint

from nba_api.stats.endpoints import (
    LeagueStandings,
    LeagueStandingsV3,
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
            "LeagueStandings",
            LeagueStandings(
                season="2023-24",
            ),
        ),
        (
            "LeagueStandingsV3",
            LeagueStandingsV3(
                season="2023-24",
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