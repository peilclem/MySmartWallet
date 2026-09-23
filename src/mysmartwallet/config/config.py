import logging
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """
    Configuration class for the application.
    """

    ROOT_DIR: Path
    DATA_DIR: Path
    DB_PATH: Path

    LOG_FILE: Path
    LOG_LEVEL: int


def load_config() -> AppConfig:
    """
    Load the application configuration.

    Returns
    -------
    AppConfig
        An instance of the AppConfig class containing the application configuration.
    """
    return AppConfig(
        ROOT_DIR=Path(__file__).parents[2],
        DATA_DIR=Path(__file__).parents[2] / "data",
        DB_PATH=Path(__file__).parents[2] / "data" / "MySmartWallet.db",
        LOG_FILE=Path(__file__).parents[2] / "logs" / "app.log",
        LOG_LEVEL=logging.DEBUG,
    )


CONFIG = load_config()
