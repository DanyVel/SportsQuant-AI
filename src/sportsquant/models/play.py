"""
Play domain model.
"""

from __future__ import annotations

from dataclasses import dataclass

from sportsquant.models.value_objects import PlayType


@dataclass(frozen=True, slots=True)
class Play:
    """
    Represents a single event that occurred during a basketball game.
    """

    game_id: str

    event_number: int

    period: int

    clock: str

    play_type: PlayType

    description: str

    team_id: int | None = None

    player_id: int |None = None