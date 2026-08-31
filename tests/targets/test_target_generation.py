"""
Tests for target generation.
"""

import inspect

import pytest

import sportsquant.targets.target_generation as target_generation_module
from sportsquant.targets.target_generation import UndeterminableTargetError
from sportsquant.targets.target_generation import generate_win_loss_target


def test_generate_win_loss_target_returns_one_for_victory() -> None:
    assert generate_win_loss_target(
        110,
        100,
    ) == 1


def test_generate_win_loss_target_returns_zero_for_loss() -> None:
    assert generate_win_loss_target(
        95,
        102,
    ) == 0


def test_generate_win_loss_target_is_deterministic() -> None:
    first_result = generate_win_loss_target(
        110,
        100,
    )
    second_result = generate_win_loss_target(
        110,
        100,
    )

    assert first_result == second_result


def test_generate_win_loss_target_raises_when_team_points_missing() -> None:
    with pytest.raises(UndeterminableTargetError):
        generate_win_loss_target(
            None,
            100,
        )


def test_generate_win_loss_target_raises_when_opponent_points_missing() -> None:
    with pytest.raises(UndeterminableTargetError):
        generate_win_loss_target(
            110,
            None,
        )


def test_target_generation_module_has_no_infrastructure_imports() -> None:
    """Ensures Target Generation stays free of forbidden dependencies.

    This is a structural safeguard, not a substitute for architectural
    review: it inspects the module's own source to verify that no
    forbidden dependency (persistence, ORM, providers, NBA API,
    pandas, etc.) has been introduced.
    """
    source = inspect.getsource(target_generation_module)
    lowered_source = source.lower()

    forbidden_tokens = (
        "sqlalchemy",
        "persistence",
        "repositories",
        "providers",
        "nba_api",
        "pandas",
    )

    for forbidden_token in forbidden_tokens:
        assert forbidden_token not in lowered_source