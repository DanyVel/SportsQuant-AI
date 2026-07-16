"""
Historical NBA data pipeline.
"""

from __future__ import annotations

from sportsquant.aggregates import Game
from sportsquant.persistence.repositories import SQLAlchemyGameRepository
from sportsquant.pipelines.base import BasePipeline
from sportsquant.pipelines.config import PipelineConfig
from sportsquant.repositories import GameRepository
from sportsquant.repositories.nba import NBAGameRepository


class HistoricalDataPipeline(BasePipeline):
    """
    Pipeline responsible for retrieving historical NBA data.
    """

    def __init__(
        self,
        persistence_repository: SQLAlchemyGameRepository,
        repository: GameRepository | None = None,
        config: PipelineConfig | None = None,
    ) -> None:
        """
        Initialize the historical pipeline.
        """
        super().__init__(config)

        self._repository = repository or NBAGameRepository()
        self._persistence_repository = persistence_repository

    def run(
        self,
        season: str,
        max_games: int | None = None,
    ) -> tuple[Game, ...]:
        """
        Retrieve Game aggregates for a season.

        Parameters
        ----------
        season : str
            NBA season (e.g. "2023-24").

        max_games : int | None, default=None
            Maximum number of games to process.
            If None, every game is processed.

        Returns
        -------
        tuple[Game, ...]
            Complete Game aggregates.
        """
        game_ids = self._discover_game_ids(
            season,
        )

        if max_games is not None:
            game_ids = game_ids[:max_games]

        return self._build_games(
            game_ids,
        )

    def _discover_game_ids(
        self,
        season: str,
    ) -> tuple[str, ...]:
        """
        Retrieve every game identifier for a season.
        """
        return self._repository.get_ids_by_season(
            season,
        )

    def _build_games(
        self,
        game_ids: tuple[str, ...],
    ) -> tuple[Game, ...]:
        """
        Build Game aggregates from game identifiers.
        """
        games: list[Game] = []

        for game_id in self.executor.iterate(game_ids):
            game = self._repository.get_by_id(
                game_id,
            )

            if game is not None:
                self._persistence_repository.save(
                    game,
                )

                games.append(
                    game,
                )

        return tuple(
            games,
        )
