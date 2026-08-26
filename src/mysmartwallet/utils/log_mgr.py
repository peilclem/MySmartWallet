import logging
import sys
from pathlib import Path


class CenteredFormatter(logging.Formatter):
    """
    Formatter custom pour centrer levelname et logger name
    """

    def format(self, record):
        record.levelname = f"{record.levelname:^10}"
        record.name = f"{record.module:^25}"
        return super().format(record)


def init_logger(log_file: str = "logs/app.log", level=logging.DEBUG):
    # Création dossier logs si nécessaire
    Path("logs").mkdir(exist_ok=True)

    formatter = CenteredFormatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Remove DEBUG logs from libraries
    NOISY_LIBS = [
        "pdfplumber",
        "tabula",
        "pdfinterp",
        "pdfinterp"
    ]

    for lib in NOISY_LIBS:
        logging.getLogger(lib).setLevel(logging.WARNING)

    # Optionnel: éviter doublons si reload
    root_logger.propagate = False