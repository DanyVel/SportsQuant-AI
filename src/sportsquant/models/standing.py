"""
Standing value object.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Standing:
    """
    Represents a team's position in the standings.
    """

    conference_rank: int
    division_rank: int
    league_rank: int | None = None

    def __post_init__(self) -> None:
        """
        Validate standing values.
        """
        if self.conference_rank <= 0:
            raise ValueError(
                "conference_rank must be positive."
            )

        if self.division_rank <= 0:
            raise ValueError(
                "division_rank must be positive."
            )

        if (
            self.league_rank is not None
            and self.league_rank <= 0
        ):
            raise ValueError(
                "league_rank must be positive."
            )