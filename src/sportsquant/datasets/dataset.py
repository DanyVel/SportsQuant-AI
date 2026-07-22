"""Dataset model.

Represents a delimited, coherent collection of DatasetRow instances,
as defined conceptually in docs/design/dataset.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from sportsquant.datasets.dataset_row import DatasetRow

AnalyticalFeatureT = TypeVar("AnalyticalFeatureT")
TargetT = TypeVar("TargetT")


@dataclass(frozen=True, slots=True)
class Dataset(Generic[AnalyticalFeatureT, TargetT]):
    """A delimited and coherent collection of DatasetRow observations.

    A Dataset is the stabilized result of organizing a set of
    DatasetRow instances under a shared purpose. It does not know how
    its rows were constructed, validated, or assembled; it only holds
    them as a coherent whole.

    Attributes:
        rows: The delimited collection of DatasetRow instances that
            compose this Dataset.
    """

    rows: tuple[DatasetRow[AnalyticalFeatureT, TargetT], ...]