from mysmartwallet.database import TransactionRepository
from mysmartwallet.models.transaction import Transaction


class TransactionService:
    """Holds the services like checking if transaction is valid, do categorization, etc.
    """
    def __init__(self, transaction_repository:TransactionRepository):
        """Initialize TransactionService

        Parameters
        ----------
        transaction_repository : TransactionRepository
            TransactionRepository that manages connection with transaction tanle
        """
        self.transaction_repository = transaction_repository

    def import_transactions(self, transactions:list[Transaction]):
        """Clean transaction labels

        Parameters
        ----------
        transactions : list[Transaction]
            List of all transactions that just got parsed
        """
        cleaned_transactions = []
        for t in transactions:
            if not self._is_valid_transaction(t):
                continue
            t = self._normalize_transaction(t)
            t.category = self._categorize_transaction(t)
            cleaned_transactions.append(t)

        self.transaction_repository.add_many(cleaned_transactions)

    def _is_valid_transaction(self, transaction:Transaction):
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

    def _normalize_transaction(self, transaction:Transaction) -> Transaction:
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
        text_to_remove = ["CARTE 1685", "CARTE 7581"]
        for text in text_to_remove:
            if text in transaction.label.upper():
                transaction.label = transaction.label.upper().replace(text, "").strip()
        return transaction

    def _categorize_transaction(self, transaction:Transaction):
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

