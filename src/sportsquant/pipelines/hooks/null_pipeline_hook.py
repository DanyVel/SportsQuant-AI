"""
Default pipeline hook implementation.
"""

from __future__ import annotations

from sportsquant.pipelines.hooks.pipeline_hook import PipelineHook


class NullPipelineHook(PipelineHook):
    """
    Default pipeline hook.

    This implementation intentionally performs no actions and
    allows the execution framework to avoid conditional checks
    when no custom hook is configured.
    """

    def before_run(self) -> None:
        """
        Do nothing before pipeline execution.
        """
        return

    def after_run(self) -> None:
        """
        Do nothing after pipeline execution.
        """
        return