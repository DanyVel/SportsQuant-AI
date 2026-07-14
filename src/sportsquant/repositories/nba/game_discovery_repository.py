"""
NBA game discovery repository.
"""

from __future__ import annotations

from sportsquant.repositories import GameDiscoveryRepository


class NBAGameDiscoveryRepository(
    GameDiscoveryRepository,
):
    """
    NBA implementation.
    """

    def get_game_ids(
        self,
        season: str,
    ) -> tuple[str, ...]:
        raise NotImplementedError