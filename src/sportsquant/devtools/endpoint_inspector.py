"""
Development tool for inspecting nba_api endpoints.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


class EndpointInspector:
    """
    Inspect nba_api endpoint objects.
    """

    def inspect(self, endpoint: Any) -> None:
        """
        Inspect an nba_api endpoint and print DataFrame information.
        """
        dataframes = endpoint.get_data_frames()

        print("=" * 80)
        print(f"Endpoint: {endpoint.__class__.__name__}")
        print("=" * 80)

        print(f"\nDatasets: {len(dataframes)}")

        for index, dataframe in enumerate(dataframes, start=1):
            print("\n" + "-" * 80)
            print(f"Dataset {index}")
            print("-" * 80)

            print(f"Rows: {len(dataframe)}")
            print(f"Columns: {len(dataframe.columns)}")

            print("\nColumn names:")
            for column in dataframe.columns:
                print(f"  - {column}")

            print("\nFirst row:")

            if dataframe.empty:
                print("  <empty>")
            else:
                first_row = dataframe.iloc[0]

                for column in dataframe.columns:
                    print(f"  {column}: {first_row[column]}")