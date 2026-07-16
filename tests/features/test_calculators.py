"""
Tests for feature calculators.
"""

from sportsquant.features.calculators import field_goal_percentage
from sportsquant.features.calculators import free_throw_percentage
from sportsquant.features.calculators import safe_divide
from sportsquant.features.calculators import three_point_percentage


def test_safe_divide_returns_quotient() -> None:
    assert safe_divide(
        10,
        2,
    ) == 5


def test_safe_divide_returns_zero_when_numerator_is_zero() -> None:
    assert safe_divide(
        0,
        5,
    ) == 0


def test_safe_divide_returns_zero_when_denominator_is_zero() -> None:
    assert safe_divide(
        10,
        0,
    ) == 0


def test_safe_divide_returns_zero_when_both_values_are_zero() -> None:
    assert safe_divide(
        0,
        0,
    ) == 0


def test_field_goal_percentage() -> None:
    assert field_goal_percentage(
        9,
        18,
    ) == 0.5


def test_field_goal_percentage_returns_zero_when_attempts_are_zero() -> None:
    assert field_goal_percentage(
        0,
        0,
    ) == 0


def test_three_point_percentage() -> None:
    assert three_point_percentage(
        5,
        10,
    ) == 0.5


def test_three_point_percentage_returns_zero_when_attempts_are_zero() -> None:
    assert three_point_percentage(
        0,
        0,
    ) == 0


def test_free_throw_percentage() -> None:
    assert free_throw_percentage(
        8,
        10,
    ) == 0.8


def test_free_throw_percentage_returns_zero_when_attempts_are_zero() -> None:
    assert free_throw_percentage(
        0,
        0,
    ) == 0
