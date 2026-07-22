"""Dataset model package.

Exposes the Dataset and DatasetRow models, as defined conceptually in
docs/design/dataset.md and docs/design/dataset-row.md, and specified
for implementation in docs/specifications/dataset-model.md.
"""

from sportsquant.datasets.dataset import Dataset
from sportsquant.datasets.dataset_row import DatasetRow

__all__ = ["Dataset", "DatasetRow"]