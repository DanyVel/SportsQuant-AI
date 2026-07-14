"""
Simple integration test for the NBA Game Repository.
"""

from sportsquant.repositories.nba import NBAGameRepository


GAME_ID = "0022300001"


def main() -> None:
    repository = NBAGameRepository()

    game = repository.get_by_id(GAME_ID)

    if game is None:
        print("Game not found.")
        return

    print("=" * 80)
    print("GAME SUMMARY")
    print("=" * 80)
    print(game.summary)
    print()

    print("=" * 80)
    print("HOME TEAM")
    print("=" * 80)
    print(game.home_team_stats)
    print()

    print("=" * 80)
    print("AWAY TEAM")
    print("=" * 80)
    print(game.away_team_stats)
    print()

    print("=" * 80)
    print("PLAYERS")
    print("=" * 80)
    print(f"Players: {len(game.player_stats)}")
    print()

    if game.player_stats:
        print("First player:")
        print(game.player_stats[0])


if __name__ == "__main__":
    main()