from PySide6.QtWidgets import QApplication

from mysmartwallet.utils.app_config import CONFIG
from mysmartwallet.views.transaction_widget import TransactionWidget
from mysmartwallet.controllers.transaction_controller import TransactionController
from mysmartwallet.services.transaction_service import TransactionService
from mysmartwallet.database.TransactionRepository import TransactionRepository
from mysmartwallet.database.DatabaseManager import DatabaseManager
from mysmartwallet.models.parsers.cic import CICParser


def main():
    app = QApplication([])

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
    controller = TransactionController(
        view=view,
        parser=parser,
        transaction_service=transaction_service,
        transaction_repository=transaction_repository
    )

    view.show()

    app.exec()


if __name__ == "__main__":
    main()