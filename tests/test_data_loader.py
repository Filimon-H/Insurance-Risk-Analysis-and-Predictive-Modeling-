"""Tests for the DataLoader utilities.

These tests focus on basic behaviour: file-not-found handling and
correct use of the configured data directory. We avoid loading the
full real dataset here.
"""

from pathlib import Path

import pandas as pd
import pytest

from src.config import Config, PROJECT_ROOT
from src.data_loader import DataLoader


def test_data_loader_from_config_uses_config_data_dir(tmp_path, monkeypatch):
    """DataLoader.from_config should respect the data_dir from Config."""

    custom_data_dir = tmp_path / "data"
    custom_data_dir.mkdir()

    # Patch Config.from_env to return a Config with our custom data_dir
    def fake_from_env() -> Config:
        return Config(
            data_dir=custom_data_dir,
            models_dir=PROJECT_ROOT / "models",
            logs_dir=PROJECT_ROOT / "logs",
            debug=False,
        )

    monkeypatch.setattr("src.config.Config.from_env", staticmethod(fake_from_env))

    loader = DataLoader.from_config()

    assert loader.data_dir == custom_data_dir


def test_load_machine_learning_rating_raises_if_file_missing(tmp_path, monkeypatch):
    """Loading should raise FileNotFoundError if the dataset does not exist."""

    custom_data_dir = tmp_path / "data"
    (custom_data_dir / "raw").mkdir(parents=True)

    def fake_from_env() -> Config:
        return Config(
            data_dir=custom_data_dir,
            models_dir=PROJECT_ROOT / "models",
            logs_dir=PROJECT_ROOT / "logs",
            debug=False,
        )

    monkeypatch.setattr("src.config.Config.from_env", staticmethod(fake_from_env))

    loader = DataLoader.from_config()

    with pytest.raises(FileNotFoundError):
        loader.load_machine_learning_rating()


def test_load_machine_learning_rating_reads_pipe_separated_file(tmp_path, monkeypatch):
    """Loader should correctly read a small pipe-separated file into a DataFrame."""

    custom_data_dir = tmp_path / "data"
    raw_dir = custom_data_dir / "raw"
    raw_dir.mkdir(parents=True)

    sample_path = raw_dir / "MachineLearningRating_v3.txt"
    sample_content = (
        "UnderwrittenCoverID|PolicyID|TotalPremium|TotalClaims\n"
        "1|10|100.0|10.0\n"
        "2|20|200.0|0.0\n"
    )
    sample_path.write_text(sample_content)

    def fake_from_env() -> Config:
        return Config(
            data_dir=custom_data_dir,
            models_dir=PROJECT_ROOT / "models",
            logs_dir=PROJECT_ROOT / "logs",
            debug=False,
        )

    monkeypatch.setattr("src.config.Config.from_env", staticmethod(fake_from_env))

    loader = DataLoader.from_config()
    df = loader.load_machine_learning_rating()

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == [
        "UnderwrittenCoverID",
        "PolicyID",
        "TotalPremium",
        "TotalClaims",
    ]
    assert len(df) == 2
