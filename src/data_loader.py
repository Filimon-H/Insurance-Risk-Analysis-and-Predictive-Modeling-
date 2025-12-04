"""Data loading utilities for the insurance risk analysis project.

This module provides a simple DataLoader class to read the
MachineLearningRating_v3.txt dataset into a pandas DataFrame.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd

from src.config import get_config


@dataclass
class DataLoader:
    """Load project datasets from disk.

    Parameters
    ----------
    data_dir:
        Base directory where raw and processed data are stored.
    """

    data_dir: Path

    @classmethod
    def from_config(cls) -> "DataLoader":
        """Construct a DataLoader using the global configuration."""

        cfg = get_config()
        return cls(data_dir=cfg.data_dir)

    def load_machine_learning_rating(self, filename: Optional[str] = None) -> pd.DataFrame:
        """Load the MachineLearningRating_v3 dataset.

        Parameters
        ----------
        filename:
            Optional custom filename relative to `data_dir / "raw"`.
            Defaults to "MachineLearningRating_v3.txt".

        Returns
        -------
        pandas.DataFrame
            The loaded dataset with parsed columns.
        """

        if filename is None:
            filename = "MachineLearningRating_v3.txt"

        raw_path = self.data_dir / "raw" / filename

        if not raw_path.exists():
            raise FileNotFoundError(f"Data file not found: {raw_path}")

        df = pd.read_csv(
            raw_path,
            sep="|",
            engine="python",
        )

        return df
