"""
Inspect the BoxScoreSummaryV3 endpoint.

This script is used only for discovery purposes.
"""

from pprint import pprint

from nba_api.stats.endpoints import BoxScoreSummaryV3


GAME_ID = "0022300001"


def main() -> None:
    endpoint = BoxScoreSummaryV3(game_id=GAME_ID)

    datasets = endpoint.get_data_frames()

    print("=" * 80)
    print("Endpoint: BoxScoreSummaryV3")
    print("=" * 80)
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

        print("Column names:")
        pprint(list(dataframe.columns))
        print()

        if not dataframe.empty:
            print("First row:")
            pprint(dataframe.iloc[0].to_dict())

        print()
        print()


if __name__ == "__main__":
    main()