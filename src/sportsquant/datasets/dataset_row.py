"""DatasetRow model.

Represents a single, self-contained observation belonging to a
Dataset, as defined conceptually in docs/design/dataset-row.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

AnalyticalFeatureT = TypeVar("AnalyticalFeatureT")
TargetT = TypeVar("TargetT")


@dataclass(frozen=True, slots=True)
class DatasetRow(Generic[AnalyticalFeatureT, TargetT]):
    """A single, self-contained observation belonging to a Dataset.

    A DatasetRow conserves the analytical state produced by an
    Analytical Feature Model, together with its associated prediction
    target, without reinterpreting or recalculating either. It
    represents a stabilized result, not a process.

    Attributes:
        feature: The analytical state of this observation, as produced
            by an Analytical Feature Model. Its meaning is conserved
            as-is.
        target: The prediction target associated with this
            observation.
    """

    feature: AnalyticalFeatureT
    target: TargetT