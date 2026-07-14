"""
Team domain model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Team:
    """
    Represents an NBA franchise.
    """

    id: int
    full_name: str
    abbreviation: str
    city: str
    nickname: str
    state: str
    year_founded: int