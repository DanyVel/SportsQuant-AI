"""
Pipeline configuration objects.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PipelineConfig:
    """
    Configuration for pipeline execution behavior.

    Attributes:
        max_items:
            Maximum number of items to process.
            None means process all items.

        batch_size:
            Number of items processed per batch.

        show_progress:
            Whether progress information should be displayed.

        parallel:
            Whether execution should use parallel workers.
    """

    max_items: int | None = None
    batch_size: int = 100
    show_progress: bool = True
    parallel: bool = False