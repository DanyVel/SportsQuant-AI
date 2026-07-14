"""
Inspect the LeagueGameFinder endpoint.
"""

from __future__ import annotations

from nba_api.stats.endpoints import LeagueGameFinder


def main() -> None:
    """
    Inspect the LeagueGameFinder endpoint.
    """
    print("=" * 80)
    print("LeagueGameFinder Debug")
    print("=" * 80)
    print()

    print("1. Creating endpoint...")

    endpoint = LeagueGameFinder()

    print("2. Endpoint created successfully.")

    print("3. Retrieving DataFrames...")

    datasets = endpoint.get_data_frames()

    print("4. DataFrames retrieved successfully.")
    print()

    print(f"Datasets: {len(datasets)}")
    print()

    for index, dataframe in enumerate(datasets, start=1):
        print("-" * 80)
        print(f"Dataset {index}")
        print("-" * 80)

        print(f"Rows: {len(dataframe)}")
        print(f"Columns: {len(dataframe.columns)}")
        print()

        for column in dataframe.columns:
            print(column)

        print()


if __name__ == "__main__":
    main()