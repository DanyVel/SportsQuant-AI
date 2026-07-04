"""
Base classes for the data layer.
"""

from abc import ABC

from sportsquant.logging.logger import get_logger


class BaseDataComponent(ABC):
    """
    Base class for all data layer components.
    """

    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)