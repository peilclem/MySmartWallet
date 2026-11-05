import logging
import sys
from pathlib import Path

from mysmartwallet.config.config import CONFIG


class CenteredFormatter(logging.Formatter):
    """
    Formatter custom pour centrer levelname et logger name
    """

    def format(self, record):
        record.levelname = f"{record.levelname:^10}"
        record.name = f"{record.module:^25}"
        return super().format(record)


def initLogger(logFile: str = "logs/app.log", level=CONFIG.LOG_LEVEL):
    # Création dossier logs si nécessaire
    Path("logs").mkdir(exist_ok=True)

    formatter = CenteredFormatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(level)
    consoleHandler.setFormatter(formatter)

    # File handler
    fileHandler = logging.FileHandler(logFile, encoding="utf-8")
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(formatter)

    # Root logger
    rootLogger = logging.getLogger()
    rootLogger.setLevel(level)
    rootLogger.handlers.clear()

    rootLogger.addHandler(consoleHandler)
    rootLogger.addHandler(fileHandler)

    # Remove DEBUG logs from libraries
    NOISY_LIBS = ["pdfplumber", "tabula", "pdfinterp", "pdfinterp", "pdfminer", "pdfminer.six"]

    for lib in NOISY_LIBS:
        logging.getLogger(lib).setLevel(logging.WARNING)

    # Optionnel: éviter doublons si reload
    rootLogger.propagate = False
