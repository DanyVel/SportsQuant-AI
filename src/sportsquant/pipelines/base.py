"""
Base pipeline abstractions.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from sportsquant.pipelines.config import PipelineConfig
from sportsquant.pipelines.executor import PipelineExecutor


class BasePipeline(ABC):
    """
    Base class for every pipeline.
    """

    def __init__(
        self,
        config: PipelineConfig | None = None,
    ) -> None:
        """
        Initialize the pipeline.

        Args:
            config:
                Pipeline execution configuration.
        """
        self._config = config or PipelineConfig()
        self._executor = PipelineExecutor(self._config)

    @property
    def config(self) -> PipelineConfig:
        """
        Return the pipeline configuration.
        """
        return self._config

    @property
    def executor(self) -> PipelineExecutor:
        """
        Return the pipeline executor.
        """
        return self._executor

    @abstractmethod
    def run(self) -> None:
        """
        Execute the pipeline.
        """
        raise NotImplementedError