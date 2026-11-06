import logging

from mysmartwallet.database.TransactionRepository import TransactionRepository
from mysmartwallet.models.transaction import Transaction

logger = logging.getLogger(__name__)


class TransactionService:
    """Holds the services like checking if transaction is valid, do categorization, etc."""

    def __init__(self, transactionRepository: TransactionRepository) -> None:
        """Initialize TransactionService

        Parameters
        ----------
        transactionRepository : TransactionRepository
            TransactionRepository that manages connection with transaction table
        """
        self.transactionRepository = transactionRepository

    def importTransactions(self, transactions: list[Transaction]) -> None:
        """Clean transaction labels

        Parameters
        ----------
        transactions : list[Transaction]
            List of all transactions that just got parsed
        """
        logger.info("Importing transactions", extra={"count": len(transactions)})

        cleanedTransactions = []
        for t in transactions:
            if not self.isValidTransaction(t):
                continue
            t = self._normalizeTransaction(t)
            t.category = self._categorizeTransaction(t)
            cleanedTransactions.append(t)

        self.transactionRepository.addMany(cleanedTransactions)

    def isValidTransaction(self, transaction: Transaction) -> bool:
        """Check if amount is not null

        Parameters
        ----------
        transaction : Transaction
            Transaction to check

        Returns
        -------
        bool
            if transaction is not null
        """
        return transaction.amount != 0

    def _normalizeTransaction(self, transaction: Transaction) -> Transaction:
        """Clean transaction labels

        Parameters
        ----------
        transaction : Transaction
            transaction to clean

        Returns
        -------
        Transaction
            Cleaned transaction
        """
        transaction.label = transaction.label.strip()
        textToRemove = ["CARTE 1685", "CARTE 7581"]
        for text in textToRemove:
            if text in transaction.label.upper():
                transaction.label = transaction.label.upper().replace(text, "").strip()
        return transaction

    def _categorizeTransaction(self, transaction: Transaction) -> str:
        """Dumb categorization

        Parameters
        ----------
        transaction : Transaction
            transaction to categorize

        Returns
        -------
        _type_
            _description_
        """
        if transaction.amount < 0:
            return "Expense"
        elif transaction.amount > 0:
            return "Income"
        else:
            return "Unknown"
