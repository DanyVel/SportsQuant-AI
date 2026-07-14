"""
Pipeline execution utilities.
"""

from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Iterator
from typing import TypeVar

from sportsquant.pipelines.config import PipelineConfig

T = TypeVar("T")


class PipelineExecutor:
    """
    Execute pipeline work items.

    This class encapsulates the execution strategy used by pipelines.

    Future capabilities include:

    - Batch processing
    - Retry policies
    - Progress reporting
    - Metrics collection
    - Parallel execution
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
        items: Iterable[T],
    ) -> Iterator[T]:
        """
        Iterate over work items.

        Respects the configured execution limits.
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

    def iter_batches(
        self,
        items: Iterable[T],
    ) -> Iterator[tuple[T, ...]]:
        """
        Iterate over work items grouped into batches.

        Batch size is defined by the pipeline configuration.

        Args:
            items:
                Items to process.

        Yields:
            Tuples containing one execution batch.
        """
        batch: list[T] = []

        for item in self.iterate(items):
            batch.append(item)

            if len(batch) >= self._config.batch_size:
                yield tuple(batch)
                batch.clear()

        if batch:
            yield tuple(batch)