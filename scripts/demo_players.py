"""
Test NBA player pipeline.
"""

from sportsquant.providers.nba import NBAProvider


def main() -> None:
    """
    Test the player pipeline.
    """
    provider = NBAProvider()

    players = provider.get_players()

    print(f"Players loaded: {len(players)}")
    print()

    for player in players[:10]:
        print(player)


if __name__ == "__main__":
    main()