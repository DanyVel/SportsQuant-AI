"""Unit tests for the Dataset model."""

import dataclasses

import pytest

from sportsquant.datasets.dataset import Dataset
from sportsquant.datasets.dataset_row import DatasetRow


def test_dataset_can_be_constructed_from_a_set_of_dataset_rows() -> None:
    rows = (
        DatasetRow(feature="feature-state-1", target=1),
        DatasetRow(feature="feature-state-2", target=0),
    )

    dataset: Dataset[str, int] = Dataset(rows=rows)

    assert dataset.rows == rows


def test_dataset_cannot_be_modified_once_constructed() -> None:
    rows = (DatasetRow(feature="feature-state", target=1),)
    dataset: Dataset[str, int] = Dataset(rows=rows)

    with pytest.raises(dataclasses.FrozenInstanceError):
        dataset.rows = ()  # type: ignore[misc]


def test_dataset_can_be_constructed_from_an_empty_collection() -> None:
    dataset: Dataset[str, int] = Dataset(rows=())

    assert dataset.rows == ()