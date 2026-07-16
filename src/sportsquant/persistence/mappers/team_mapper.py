"""
Mapper between Team domain models and ORM models.
"""

from __future__ import annotations

from sportsquant.models import Team
from sportsquant.persistence.orm import TeamORM


class TeamMapper:
    """
    Maps Team domain models to ORM models and vice versa.
    """

    @staticmethod
    def to_domain(team: TeamORM) -> Team:
        """
        Convert an ORM model into a domain model.
        """
        return Team(
            id=team.id,
            full_name=team.full_name,
            abbreviation=team.abbreviation,
            city=team.city,
            nickname=team.nickname,
            state=team.state,
            year_founded=team.year_founded,
        )

    @staticmethod
    def to_orm(team: Team) -> TeamORM:
        """
        Convert a domain model into an ORM model.
        """
        return TeamORM(
            id=team.id,
            full_name=team.full_name,
            abbreviation=team.abbreviation,
            city=team.city,
            nickname=team.nickname,
            state=team.state,
            year_founded=team.year_founded,
        )