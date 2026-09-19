import logging

from mysmartwallet.database.TransactionRepository import TransactionRepository
from mysmartwallet.models.parsers.base import PdfParser
from mysmartwallet.services.transaction_service import TransactionService
from mysmartwallet.views.transaction_widget import TransactionWidget

logger = logging.getLogger(__name__)


class TransactionController:
    """Controller for managing transactions in the application.
    Handles the interaction between the view, parser, service, and repository.
    """

    def __init__(
        self,
        view: TransactionWidget,
        parser: PdfParser,
        transaction_service: TransactionService,
        transaction_repository: TransactionRepository,
    ):
        """Instanciate the transaction controller widget

        Parameters
        ----------
        view : TransviewactionWidget
            View for displaying and interacting with transactions.
        parser : PdfParser
            Parser for extracting transaction data from PDF files.
        transaction_service : TransactionService
            Service for handling transaction-related business logic.
        transaction_repository : TransactionRepository
            Repository for managing transaction data persistence.
        """
        self.view = view
        self.parser = parser
        self.transaction_service = transaction_service
        self.transaction_repository = transaction_repository

        self.load_transactions_into_view()

        self.view.import_clicked.connect(self.import_transactions)

    def import_transactions(self, file_path: str):
        """Get transactions from a pdf imported by the user

        Parameters
        ----------
        file_path : str
            Path to the PDF file containing transaction data.
        """
        logger.debug(f"ENTER import_transactions: {file_path}")

        try:
            transactions = self.parser.parse(file_path)
            logger.debug(f"Parsed transactions: {len(transactions)}")

            self.transaction_service.import_transactions(transactions)
            logger.debug("Import done")

            self.load_transactions_into_view()
            logger.debug("View refreshed")

        except Exception as e:
            import traceback

            logger.error(f"ERROR in import_transactions: {e}")
            logger.error(traceback.format_exc())

    def load_transactions_into_view(self):
        """Send transactions to transaction view"""
        transactions = self.transaction_repository.get_all()
        logger.info("Loading transactions into view")
        self.view.refresh(transactions)
