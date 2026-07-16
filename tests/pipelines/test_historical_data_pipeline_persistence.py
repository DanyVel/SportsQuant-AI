"""
Integration tests for HistoricalDataPipeline persistence.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from sportsquant.aggregates import Game
from sportsquant.models import GameSummary
from sportsquant.models import PlayerGameStats
from sportsquant.models import TeamGameStats
from sportsquant.persistence.orm import GameORM
from sportsquant.persistence.orm import PlayerGameStatsORM
from sportsquant.persistence.orm import PlayerORM
from sportsquant.persistence.orm import TeamGameStatsORM
from sportsquant.persistence.orm import TeamORM
from sportsquant.persistence.orm.base import Base
from sportsquant.persistence.repositories import SQLAlchemyGameRepository
from sportsquant.pipelines import HistoricalDataPipeline
from sportsquant.repositories import GameRepository


class FakeGameRepository(GameRepository):
    """
    Deterministic repository for pipeline integration tests.
    """

    def __init__(
        self,
        game_ids: tuple[str, ...],
        games: dict[str, Game],
    ) -> None:
        self._game_ids = game_ids
        self._games = games
        self.requested_game_ids: list[str] = []

    def get_by_id(
        self,
        game_id: str,
    ) -> Game | None:
        self.requested_game_ids.append(
            game_id,
        )

        return self._games.get(
            game_id,
        )

    def get_ids_by_season(
        self,
        season: str,
    ) -> tuple[str, ...]:
        return self._game_ids

    def save(
        self,
        game: Game,
    ) -> None:
        raise NotImplementedError

    def save_many(
        self,
        games: Iterable[Game],
    ) -> None:
        raise NotImplementedError


def test_run_returns_and_persists_game_aggregate(
    tmp_path: Path,
) -> None:
    """
    Pipeline should return and persist complete Game aggregates.
    """
    session = _create_session(
        tmp_path,
    )

    game = _make_game(
        game_id="0022300001",
        home_team_id=1610612738,
        away_team_id=1610612747,
        player_ids=(101, 102),
    )

    _seed_reference_data(
        session,
        (game,),
    )

    source_repository = FakeGameRepository(
        game_ids=("0022300001",),
        games={
            "0022300001": game,
        },
    )

    persistence_repository = SQLAlchemyGameRepository(
        session,
    )

    pipeline = HistoricalDataPipeline(
        persistence_repository=persistence_repository,
        repository=source_repository,
    )

    try:
        result = pipeline.run(
            season="2023-24",
        )

        persisted_games = session.scalars(
            select(GameORM),
        ).all()

        persisted_team_stats = session.scalars(
            select(TeamGameStatsORM),
        ).all()

        persisted_player_stats = session.scalars(
            select(PlayerGameStatsORM),
        ).all()

        assert result == (game,)

        assert len(persisted_games) == 1
        assert persisted_games[0].game_id == "0022300001"

        assert len(persisted_team_stats) == 2
        assert {
            stats.team_id
            for stats in persisted_team_stats
        } == {
            1610612738,
            1610612747,
        }

        assert len(persisted_player_stats) == 2
        assert {
            stats.player_id
            for stats in persisted_player_stats
        } == {
            101,
            102,
        }

    finally:
        session.close()


def test_max_games_limits_persisted_games_and_none_results_are_ignored(
    tmp_path: Path,
) -> None:
    """
    Pipeline should persist only produced games within the max_games limit.
    """
    session = _create_session(
        tmp_path,
    )

    first_game = _make_game(
        game_id="0022300001",
        home_team_id=1610612738,
        away_team_id=1610612747,
        player_ids=(101,),
    )

    second_game = _make_game(
        game_id="0022300002",
        home_team_id=1610612744,
        away_team_id=1610612752,
        player_ids=(201,),
    )

    _seed_reference_data(
        session,
        (
            first_game,
            second_game,
        ),
    )

    source_repository = FakeGameRepository(
        game_ids=(
            "0022300001",
            "missing-game",
            "0022300002",
        ),
        games={
            "0022300001": first_game,
            "0022300002": second_game,
        },
    )

    persistence_repository = SQLAlchemyGameRepository(
        session,
    )

    pipeline = HistoricalDataPipeline(
        persistence_repository=persistence_repository,
        repository=source_repository,
    )

    try:
        result = pipeline.run(
            season="2023-24",
            max_games=2,
        )

        persisted_games = session.scalars(
            select(GameORM),
        ).all()

        assert result == (first_game,)
        assert source_repository.requested_game_ids == [
            "0022300001",
            "missing-game",
        ]

        assert len(persisted_games) == 1
        assert persisted_games[0].game_id == "0022300001"

    finally:
        session.close()


def _create_session(
    tmp_path: Path,
) -> Session:
    database_path = tmp_path / "sportsquant_test.db"
    engine = create_engine(
        f"sqlite:///{database_path}",
    )

    Base.metadata.create_all(
        engine,
    )

    session_factory = sessionmaker(
        bind=engine,
    )

    return session_factory()


def _seed_reference_data(
    session: Session,
    games: tuple[Game, ...],
) -> None:
    team_ids = {
        game.summary.home_team_id
        for game in games
    } | {
        game.summary.away_team_id
        for game in games
    }

    player_ids = {
        stats.player_id
        for game in games
        for stats in game.player_stats
    }

    session.add_all(
        [
            TeamORM(
                id=team_id,
                full_name=f"Team {team_id}",
                abbreviation="TST",
                city="Test",
                nickname=f"Team {team_id}",
                state="Test",
                year_founded=1946,
            )
            for team_id in sorted(team_ids)
        ],
    )

    session.add_all(
        [
            PlayerORM(
                id=player_id,
                full_name=f"Player {player_id}",
                is_active=True,
            )
            for player_id in sorted(player_ids)
        ],
    )

    session.commit()


def _make_game(
    game_id: str,
    home_team_id: int,
    away_team_id: int,
    player_ids: tuple[int, ...],
) -> Game:
    return Game(
        summary=GameSummary(
            game_id=game_id,
            game_date=date(
                2023,
                10,
                24,
            ),
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            matchup="BOS @ LAL",
        ),
        home_team_stats=_make_team_game_stats(
            game_id=game_id,
            team_id=home_team_id,
            points=110,
        ),
        away_team_stats=_make_team_game_stats(
            game_id=game_id,
            team_id=away_team_id,
            points=104,
        ),
        player_stats=tuple(
            _make_player_game_stats(
                game_id=game_id,
                player_id=player_id,
                team_id=home_team_id,
            )
            for player_id in player_ids
        ),
    )


def _make_team_game_stats(
    game_id: str,
    team_id: int,
    points: int,
) -> TeamGameStats:
    return TeamGameStats(
        game_id=game_id,
        team_id=team_id,
        minutes="240",
        points=points,
        field_goals_made=40,
        field_goals_attempted=90,
        three_pointers_made=12,
        three_pointers_attempted=35,
        free_throws_made=18,
        free_throws_attempted=22,
        offensive_rebounds=10,
        defensive_rebounds=35,
        rebounds=45,
        assists=25,
        steals=8,
        blocks=5,
        turnovers=12,
        personal_fouls=18,
    )


def _make_player_game_stats(
    game_id: str,
    player_id: int,
    team_id: int,
) -> PlayerGameStats:
    return PlayerGameStats(
        game_id=game_id,
        player_id=player_id,
        team_id=team_id,
        minutes="32",
        points=24,
        field_goals_made=9,
        field_goals_attempted=18,
        three_pointers_made=3,
        three_pointers_attempted=7,
        free_throws_made=3,
        free_throws_attempted=4,
        offensive_rebounds=1,
        defensive_rebounds=6,
        rebounds=7,
        assists=5,
        steals=2,
        blocks=1,
        turnovers=3,
        personal_fouls=2,
    )
