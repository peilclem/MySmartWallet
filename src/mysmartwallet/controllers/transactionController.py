import logging

from mysmartwallet.database.TransactionRepository import TransactionRepository
from mysmartwallet.models.parsers.base import PdfParser
from mysmartwallet.services.transactionService import TransactionService
from mysmartwallet.views.transactionWidget import TransactionWidget

logger = logging.getLogger(__name__)


class TransactionController:
    """Controller for managing transactions in the application.
    Handles the interaction between the view, parser, service, and repository.
    """

    def __init__(
        self,
        view: TransactionWidget,
        parser: PdfParser,
        transactionService: TransactionService,
        transactionRepository: TransactionRepository,
    ):
        """Instanciate the transaction controller widget

        Parameters
        ----------
        view : TransviewactionWidget
            View for displaying and interacting with transactions.
        parser : PdfParser
            Parser for extracting transaction data from PDF files.
        transactionService : TransactionService
            Service for handling transaction-related business logic.
        transactionRepository : TransactionRepository
            Repository for managing transaction data persistence.
        """
        self.view = view
        self.parser = parser
        self.transactionService = transactionService
        self.transactionRepository = transactionRepository

        self.loadTransactionsIntoView()

        self.view.importClicked.connect(self.importTransactions)

    def importTransactions(self, filePath: str):
        """Get transactions from a pdf imported by the user

        Parameters
        ----------
        filePath : str
        """
        logger.info("Importing transactions from PDF", extra={"filePath": filePath})
        try:
            transactions = self.parser.parse(filePath)
            logger.info(
                "Parsed transactions",
                extra={"count": len(transactions)},
            )

            self.transactionService.importTransactions(transactions)
            logger.info("Transactions persisted and service completed")

            self.loadTransactionsIntoView()
        except Exception:
            import traceback

            logger.exception(
                "Failed to import transactions from PDF",
                extra={"filePath": filePath},
            )
            logger.error(traceback.format_exc())

    def loadTransactionsIntoView(self):
        """Send transactions to transaction view"""
        transactions = self.transactionRepository.getAll()
        logger.info(
            "Loaded transactions into view",
            extra={"count": len(transactions)},
        )
        self.view.refresh(transactions)
