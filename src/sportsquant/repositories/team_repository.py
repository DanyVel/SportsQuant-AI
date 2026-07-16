"""
Team repository interface.
"""

from __future__ import annotations

from abc import abstractmethod

from sportsquant.models import Team
from sportsquant.repositories.base import BaseRepository


class TeamRepository(BaseRepository):
    """
    Contract for team repositories.
    """

    @abstractmethod
    def get_all(self) -> tuple[Team, ...]:
        """
        Retrieve all teams.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        team_id: int,
    ) -> Team | None:
        """
        Retrieve a team by its identifier.
        """
        raise NotImplementedError