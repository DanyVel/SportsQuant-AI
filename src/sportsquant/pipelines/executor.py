"""
Pipeline execution utilities.
"""

from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Iterator

from sportsquant.pipelines.config import PipelineConfig


class PipelineExecutor:
    """
    Execute pipeline work items.

    This class encapsulates the iteration strategy used by pipelines.
    More advanced capabilities (batching, retries, metrics, hooks,
    progress reporting and parallel execution) will be added in future
    milestones.
    """

    def __init__(
        self,
        config: PipelineConfig,
    ) -> None:
        """
        Initialize the executor.

        Args:
            config:
                Pipeline execution configuration.
        """
        self._config = config

    def iterate(
        self,
        items: Iterable[object],
    ) -> Iterator[object]:
        """
        Iterate over the provided items.

        Respects the configured execution limits.

        Args:
            items:
                Items to iterate.

        Yields:
            Individual work items.
        """
        count = 0

        for item in items:
            if (
                self._config.max_items is not None
                and count >= self._config.max_items
            ):
                break

            yield item
            count += 1