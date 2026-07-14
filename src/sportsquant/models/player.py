"""
Player domain model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Player:
    """
    Represents an NBA player in the domain layer.
    """

    id: int
    full_name: str
    is_active: bool