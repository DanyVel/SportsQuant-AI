"""
Tests for NBATeamSeasonRepository.
"""

from sportsquant.repositories.nba import NBATeamSeasonRepository


def test_repository_creation() -> None:
    repository = NBATeamSeasonRepository()

    assert repository is not None