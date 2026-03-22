"""
Core Transformer.
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Any

class BaseTransformer(ABC):
    """
    Abstract base class for all data transformations.
    Expects to take raw data (file path or dict) and return structured DataFrames or objects.
    """

    @abstractmethod
    def process(self, raw_data: Any) -> Any:
        """
        Main transformation logic.
        Must be implemented by subclasses.
        """
        pass

    def load_excel(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Helper method to standardize Excel loading.
        """
        return pd.read_excel(file_path, **kwargs)

    def load_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Helper method to standardize CSV loading.
        """
        return pd.read_csv(file_path, **kwargs)
