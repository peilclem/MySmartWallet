import logging
from abc import ABC, abstractmethod
from datetime import date, datetime

from mysmartwallet.models.transaction import Transaction

logger = logging.getLogger(__name__)


class PdfParser(ABC):
    """
    An abstract base class for parsing PDF files to extract financial transactions.
    """

    def __init__(self) -> None:
        """Initialize the PdfParser"""

    def strToDate(self, dateStr: str) -> date | None:
        """Convert string date to datetime

        Parameters
        ----------
        dateStr : str
            Date in string format

        Returns
        -------
        date
            Date in date format
        """
        if isinstance(dateStr, str):
            try:
                return datetime.strptime(dateStr, "%d/%m/%Y").date()
            except ValueError:
                logger.warning(
                    "Invalid date format",
                    extra={"dateStr": dateStr},
                )
                return None

    def parse(self, pdfFile: str) -> list[Transaction]:
        """Parse a bank report

        Parameters
        ----------
        pdfFile : str
            Pdf bank report to parse

        Returns
        -------
        list[Transaction]
            List of all transactions
        """
        logger.info("Parsing PDF", extra={"pdfFile": pdfFile})

        accountNames = self.extractAccountNames(pdfFile)
        transactionsId = self.extractTransactionFromTables(pdfFile)

        transactions = self.groupTransactionsByAccount(transactionsId, accountNames)

        return transactions

    def groupTransactionsByAccount(
        self, transactions: list[Transaction], accountNames: dict
    ) -> list[Transaction]:
        """Group transactions by account

        Parameters
        ----------
        transactions : list[Transaction]
            All transactions
        accountNames : dict
            Dictionnary of account names associated with table number

        Returns
        -------
        list[Transaction]
            All transactions with an associated account name
        """
        logger.debug("Grouping transactions by account")

        for transaction in transactions:
            account_id = int(transaction.account)
            transaction.account = accountNames.get(account_id, "Unknown Account")

        return transactions

    @abstractmethod
    def extractTransactionFromTables(self, file: str) -> list[Transaction]:
        """Abstract method to extract transaction data from tables in a PDF file.
        This method should be implemented by subclasses to handle the specific logic for extracting transaction data from the provided PDF file.

        Parameters
        ----------
        file : str
            Pdf file to parse

        Returns
        -------
        list[Transaction]
            All extracted transactions
        """

    @abstractmethod
    def extractAccountNames(self, file: str):
        """Extracts account names from the provided PDF file.

        This method should be implemented by subclasses to handle the specific logic for extracting account names from the provided PDF file.


        Parameters
        ----------
        file : str
            Pdf file to parse
        """
