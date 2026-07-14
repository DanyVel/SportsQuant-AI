"""
Season domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class Season:
    """
    Represents an NBA season.

    A Season is a lightweight domain entity that defines the temporal
    boundaries of a competition. It intentionally contains no standings,
    schedules, or statistical information.
    """

    season_id: str
    season_name: str
    start_date: date | None = None
    end_date: date | None = None
    season_type: str = "Regular Season"