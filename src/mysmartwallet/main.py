from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from mysmartwallet.controllers.transaction_controller import TransactionController
from mysmartwallet.database.DatabaseManager import DatabaseManager
from mysmartwallet.database.TransactionRepository import TransactionRepository
from mysmartwallet.models.parsers.cic import CICParser
from mysmartwallet.services.transaction_service import TransactionService
from mysmartwallet.utils.app_config import CONFIG
from mysmartwallet.views.transaction_widget import TransactionWidget

from mysmartwallet.utils.log_mgr import init_logger

import logging
from json import load


def main():
    app = QApplication([])
    app.setWindowIcon(QIcon("resources/icons/msw_logo.png"))

    # -------------------
    # Infrastructure
    # -------------------
    db = DatabaseManager(CONFIG.DB_PATH)
    transaction_repository = TransactionRepository(db)

    # -------------------
    # Services
    # -------------------
    transaction_service = TransactionService(transaction_repository)

    # -------------------
    # Parser
    # -------------------
    parser = CICParser()

    # -------------------
    # View
    # -------------------
    view = TransactionWidget()

    # -------------------
    # Controller
    # -------------------
    TransactionController(
        view=view,
        parser=parser,
        transaction_service=transaction_service,
        transaction_repository=transaction_repository
    )

    view.show()

    init_logger(level=logging.INFO)

    logging.info("App started")
    logging.debug("DEBUG mode")

    app.exec()


if __name__ == "__main__":
    main()