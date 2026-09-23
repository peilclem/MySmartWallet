import logging

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from mysmartwallet.config.config import CONFIG
from mysmartwallet.controllers.transaction_controller import TransactionController
from mysmartwallet.database.DatabaseManager import DatabaseManager
from mysmartwallet.database.TransactionRepository import TransactionRepository
from mysmartwallet.models.parsers.cic import CICParser
from mysmartwallet.services.transaction_service import TransactionService
from mysmartwallet.utils.log_mgr import init_logger
from mysmartwallet.views.transaction_widget import TransactionWidget


def main():

    # Configure logging after CONFIG is loaded and before anything else logs.
    init_logger(level=CONFIG.LOG_LEVEL)

    logger = logging.getLogger(__name__)
    logger.info("App started")
    logger.debug("DEBUG mode")

    app = QApplication([])
    app.setWindowIcon(QIcon("resources/icons/msw_logo.png"))

    db = DatabaseManager(CONFIG.DB_PATH)
    transaction_repository = TransactionRepository(db)
    transaction_service = TransactionService(transaction_repository)
    parser = CICParser()

    view = TransactionWidget()

    controller = TransactionController(  # noqa: F841
        view=view,
        parser=parser,
        transaction_service=transaction_service,
        transaction_repository=transaction_repository,
    )

    view.show()

    app.exec()


if __name__ == "__main__":
    main()
