"""
Constants for the NBA Stats API.
"""

from __future__ import annotations

from enum import Enum


NBA_BASE_URL = "https://stats.nba.com/stats"


NBA_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
}


class NBAEndpoint(str, Enum):
    """
    NBA Stats API endpoints.
    """

    SCOREBOARD = "scoreboardv2"
    TEAM_YEARS = "commonteamyears"
    PLAYER_STATS = "leaguedashplayerstats"