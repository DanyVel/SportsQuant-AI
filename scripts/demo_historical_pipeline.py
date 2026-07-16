"""
Demo for HistoricalDataPipeline.
"""

from sportsquant.persistence.repositories import SQLAlchemyGameRepository
from sportsquant.persistence.session import get_session
from sportsquant.pipelines import HistoricalDataPipeline


def main() -> None:
    """
    Run the pipeline demo.
    """
    session = get_session()
    repository = SQLAlchemyGameRepository(session)

    pipeline = HistoricalDataPipeline(
        persistence_repository=repository,
    )

    games = pipeline.run(
        season="2023-24",
        max_games=5,
    )

    print("=" * 80)
    print("TOTAL GAMES")
    print("=" * 80)
    print(len(games))

    print()

    if not games:
        return

    first_game = games[0]

    print("=" * 80)
    print("FIRST GAME")
    print("=" * 80)
    print(first_game.summary)

    print()

    print("=" * 80)
    print("HOME TEAM")
    print("=" * 80)
    print(first_game.home_team_stats)

    print()

    print("=" * 80)
    print("AWAY TEAM")
    print("=" * 80)
    print(first_game.away_team_stats)

    print()

    print("=" * 80)
    print("PLAYERS")
    print("=" * 80)
    print(len(first_game.player_stats))


if __name__ == "__main__":
    main()
