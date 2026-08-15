# Holds the services like checking if transaction is valid, do categorization, etc.

class TransactionService:
    def __init__(self, transaction_repository):
        self.transaction_repository = transaction_repository

    def import_transactions(self, transactions):
        cleaned_transactions = []
        for t in transactions:
            if not self._is_valid_transaction(t):
                continue
            t = self._normalize_transaction(t)
            t.category = self._categorize_transaction(t)
            cleaned_transactions.append(t)

        self.transaction_repository.add_many(cleaned_transactions)

    def _is_valid_transaction(self, transaction):
        return transaction.amount != 0

    def _normalize_transaction(self, transaction):
        transaction.label = transaction.label.strip()
        text_to_remove = ["CARTE 1685", "CARTE 7581"]
        for text in text_to_remove:
            if text in transaction.label.upper():
                transaction.label = transaction.label.upper().replace(text, "").strip()
        return transaction

    def _categorize_transaction(self, transaction):
        if transaction.amount < 0:
            return "Expense"
        elif transaction.amount > 0:
            return "Income"
        else:
            return "Unknown"

