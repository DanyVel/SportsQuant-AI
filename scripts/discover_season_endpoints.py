"""
Discovery script for NBA season-related endpoints.
"""

from __future__ import annotations

from pprint import pprint

import pandas as pd

from nba_api.stats.endpoints import (
    CommonTeamYears,
    TeamInfoCommon,
    FranchiseHistory,
)


def inspect_endpoint(name: str, endpoint) -> None:
    """
    Print useful metadata for an NBA endpoint.
    """
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
            "CommonTeamYears",
            CommonTeamYears(),
        ),
        (
            "TeamInfoCommon",
            TeamInfoCommon(team_id=1610612738),
        ),
        (
            "FranchiseHistory",
            FranchiseHistory(),
        ),
    ]

    for name, endpoint in endpoints:
        inspect_endpoint(name, endpoint)


if __name__ == "__main__":
    main()