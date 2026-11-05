import logging

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from mysmartwallet.controllers.transactionController import TransactionController
from mysmartwallet.database.DatabaseManager import DatabaseManager
from mysmartwallet.database.TransactionRepository import TransactionRepository
from mysmartwallet.models.parsers.cic import CICParser
from mysmartwallet.services.transactionService import TransactionService
from mysmartwallet.utils.logMgr import initLogger
from mysmartwallet.views.transactionWidget import TransactionWidget

from mysmartwallet.config.config import CONFIG

def main():
    
    # Configure logging after CONFIG is loaded and before anything else logs.
    initLogger(level=CONFIG.LOG_LEVEL)

    logger = logging.getLogger(__name__)
    logger.info("App started")
    logger.debug("DEBUG mode")
    
    app = QApplication([])
    app.setWindowIcon(QIcon("resources/icons/msw_logo.png"))

    db = DatabaseManager(CONFIG.DB_PATH)
    transactionRepository = TransactionRepository(db)
    transactionService = TransactionService(transactionRepository)
    parser = CICParser()

    view = TransactionWidget()

    controller = TransactionController(
        view=view,
        parser=parser,
        transactionService=transactionService,
        transactionRepository=transactionRepository,
    )

    view.show()

    app.exec()


if __name__ == "__main__":
    main()
