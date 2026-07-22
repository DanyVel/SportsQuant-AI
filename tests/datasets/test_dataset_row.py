"""Unit tests for the DatasetRow model."""

import dataclasses

import pytest

from sportsquant.datasets.dataset_row import DatasetRow


def test_dataset_row_can_be_constructed_as_a_valid_observation() -> None:
    row: DatasetRow[str, int] = DatasetRow(feature="feature-state", target=1)

    assert row.feature == "feature-state"
    assert row.target == 1


def test_dataset_row_cannot_be_modified_once_constructed() -> None:
    row: DatasetRow[str, int] = DatasetRow(feature="feature-state", target=1)

    with pytest.raises(dataclasses.FrozenInstanceError):
        row.target = 0  # type: ignore[misc]