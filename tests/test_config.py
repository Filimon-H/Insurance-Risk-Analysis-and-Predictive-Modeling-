"""Unit tests for the configuration module.

These tests are intentionally simple to validate that the Config
class can be constructed and that default paths are sensible.
"""

from pathlib import Path

from src.config import Config, get_config, PROJECT_ROOT


def test_config_from_env_uses_defaults_when_env_not_set(monkeypatch):
    """Config.from_env should fall back to default paths when env vars are absent."""

    # Ensure related environment variables are unset for this test
    for key in ["DATA_DIR", "MODELS_DIR", "LOGS_DIR", "DEBUG"]:
        monkeypatch.delenv(key, raising=False)

    cfg = Config.from_env()

    assert cfg.data_dir == PROJECT_ROOT / "data"
    assert cfg.models_dir == PROJECT_ROOT / "models"
    assert cfg.logs_dir == PROJECT_ROOT / "logs"
    assert cfg.debug is False


def test_get_config_returns_config_instance(monkeypatch):
    """get_config should return a Config instance with valid paths."""

    monkeypatch.setenv("DATA_DIR", str(PROJECT_ROOT / "custom_data"))

    cfg = get_config()

    assert isinstance(cfg, Config)
    assert cfg.data_dir == PROJECT_ROOT / "custom_data"
    assert isinstance(cfg.models_dir, Path)
    assert isinstance(cfg.logs_dir, Path)
