"""
Core Flow Orchestrator.
Defines the abstract base class for a data flow (Scrape -> Extract -> Transform -> Load).
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseFlow(ABC):
    """
    Abstract base class representing a complete ETL/Scraping pipeline.
    Enforces a strict lifecycle: setup, extract (scrape), transform, load (save/report).
    """

    def __init__(self, name: str, output_dir: str = "data"):
        self.name = name
        self.output_dir = output_dir

    @abstractmethod
    async def extract(self) -> Any:
        """
        Execute the scraping/downloading phase.
        Must be implemented by subclasses.
        Returns the raw data or the path to the downloaded raw file.
        """
        pass

    @abstractmethod
    def transform(self, raw_data: Any) -> Any:
        """
        Execute the transformation phase (DataFrames, cleaning, aggregations).
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def load(self, transformed_data: Any) -> None:
        """
        Execute the final phase (save to DB, output report to stdout, save CSV, etc.).
        Must be implemented by subclasses.
        """
        pass

    async def execute(self) -> None:
        """
        Orchestrates the entire flow lifecycle.
        """
        print(f"=== Starting Flow: {self.name} ===")
        
        print(f"[{self.name}] 1. Extracting data...")
        raw_data = await self.extract()

        print(f"[{self.name}] 2. Transforming data...")
        transformed_data = self.transform(raw_data)

        print(f"[{self.name}] 3. Loading/Reporting data...")
        self.load(transformed_data)

        print(f"=== Flow {self.name} Completed ===")
