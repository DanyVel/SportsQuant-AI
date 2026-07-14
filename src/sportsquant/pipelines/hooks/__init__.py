"""
Pipeline hook abstractions.
"""

from sportsquant.pipelines.hooks.null_pipeline_hook import NullPipelineHook
from sportsquant.pipelines.hooks.pipeline_hook import PipelineHook

__all__ = [
    "PipelineHook",
    "NullPipelineHook",
]