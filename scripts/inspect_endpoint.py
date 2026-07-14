"""
Inspect an nba_api endpoint.
"""

from nba_api.stats.endpoints import BoxScoreTraditionalV3

from sportsquant.devtools.endpoint_inspector import EndpointInspector


GAME_ID = "0022300001"


def main() -> None:
    """
    Inspect the BoxScoreTraditionalV3 endpoint.
    """
    inspector = EndpointInspector()

    inspector.inspect(
        BoxScoreTraditionalV3(
            game_id=GAME_ID,
        )
    )


if __name__ == "__main__":
    main()