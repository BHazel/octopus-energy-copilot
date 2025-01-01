"""
Module for UI builders.
"""

from abc import ABC, abstractmethod
from gradio import Blocks

class BaseUiBuilder(ABC):
    """
    Base class for UI builders.
    """

    @abstractmethod
    def build_ui(self) -> Blocks:
        """
        Builds the UI.
        """
