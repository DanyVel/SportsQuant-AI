"""
Tests for NBAGameRepository.
"""

from sportsquant.aggregates import Game
from sportsquant.repositories.nba import NBAGameRepository


def test_get_by_id() -> None:
    """
    Repository should retrieve a Game aggregate.
    """
    repository = NBAGameRepository()

    game = repository.get_by_id(
        "0022300001",
    )

    assert game is not None
    assert isinstance(game, Game)


def test_get_ids_by_season() -> None:
    """
    Repository should retrieve every game ID for a season.
    """
    repository = NBAGameRepository()

    game_ids = repository.get_ids_by_season(
        "2023-24",
    )

    assert isinstance(game_ids, tuple)
    assert len(game_ids) > 0

    assert all(
        isinstance(game_id, str)
        for game_id in game_ids
    )

    assert len(game_ids) == len(
        set(game_ids),
    )

    assert "0022300001" in game_ids