import sqlite3
from .models.transaction import Transaction
from .models.database.DatabaseManager import DatabaseManager

class TransactionRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def add(self, transaction: Transaction):
        query = """
        INSERT INTO Transactions
        (Date, Account_ID, Label, Amount, Category)
        VALUES (?, ?, ?, ?, ?)
        """

        self.db.execute(
            query,
            (
                transaction.date,
                transaction.account,
                transaction.label,
                transaction.amount,
                transaction.category
            )
        )

        self.db.commit()