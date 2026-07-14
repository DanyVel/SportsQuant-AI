"""
Tests for PlayerService.
"""

from sportsquant.repositories.nba import NBAPlayerRepository
from sportsquant.services import PlayerService


def test_get_player_by_id() -> None:
    """
    PlayerService should retrieve a player by ID.
    """
    repository = NBAPlayerRepository()

    service = PlayerService(repository)

    players = service.get_players()

    assert players

    first_player = players[0]

    result = service.get_player_by_id(
        first_player.id,
    )

    assert result == first_player