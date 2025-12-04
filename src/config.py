"""Configuration module for the insurance risk analysis project.

This module provides a Config class that centralises project-wide
settings such as data directories and environment flags. Values can
optionally be overridden via environment variables or a `.env` file.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from a local .env file if present.
# This call is safe if the file does not exist.
load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    """Application configuration.

    Attributes
    ----------
    data_dir:
        Base directory for all data files.
    models_dir:
        Directory for trained model artefacts.
    logs_dir:
        Directory for log files.
    debug:
        Flag to enable more verbose behaviour in development.
    """

    data_dir: Path
    models_dir: Path
    logs_dir: Path
    debug: bool = False

    @classmethod
    def from_env(cls) -> "Config":
        """Create a Config instance using environment variables when available.

        Environment variables (optional)
        --------------------------------
        DATA_DIR, MODELS_DIR, LOGS_DIR, DEBUG
        """

        data_dir = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))
        models_dir = Path(os.getenv("MODELS_DIR", PROJECT_ROOT / "models"))
        logs_dir = Path(os.getenv("LOGS_DIR", PROJECT_ROOT / "logs"))

        debug_str = os.getenv("DEBUG", "false").lower()
        debug = debug_str in {"1", "true", "yes", "y"}

        return cls(
            data_dir=data_dir,
            models_dir=models_dir,
            logs_dir=logs_dir,
            debug=debug,
        )


def get_config() -> Config:
    """Return a singleton-like Config instance.

    This helper is convenient for importing configuration in other modules
    without repeatedly reading environment variables.
    """

    return Config.from_env()
