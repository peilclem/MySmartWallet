import logging

from mysmartwallet.database.DatabaseManager import DatabaseManager
from mysmartwallet.models.transaction import Transaction


logger = logging.getLogger(__name__)

class TransactionRepository:
    """Object to manage connection with the transaction table in the database
    """
    def __init__(self, db: DatabaseManager):
        """Initialize TransactionRepository

        Parameters
        ----------
        db : DatabaseManager
            database
        """
        self.db = db

    def add(self, transaction: Transaction):
        """Add a new transaction to the database

        Parameters
        ----------
        transaction : Transaction
            Transaction to be added
        """
        query = """
        INSERT INTO Transactions
        (Date, Account_ID, Label, Amount, Category)
        VALUES (?, ?, ?, ?, ?)
        """
        logger.info(f"Adding {transaction.label} in the database")

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

    def add_many(self, transactions: list[Transaction]):
        """Add multiple transactions to the database

        Parameters
        ----------
        transactions : list[Transaction]
            List of transactions to be added
        """
        query = """
        INSERT INTO Transactions
        (Date, Account_ID, Label, Amount, Category)
        VALUES (?, ?, ?, ?, ?)
        """
        logger.info(f"Adding {len(transactions)} transactions in the database")

        data = [
            (
                transaction.date,
                transaction.account,
                transaction.label,
                transaction.amount,
                transaction.category
            )
            for transaction in transactions
        ]

        self.db.executemany(query, data)
        self.db.commit()

    def get_all(self):
        """Fetch all transactions from the database
        
        Returns
        -------
        list
            List of all transactions in the database
        """
        logger.debug("Get all transactions in the database")

        query = """SELECT * FROM Transactions ORDER BY Date DESC"""
        rows = self.db.fetch_all(query)

        return [
        Transaction(
            date=row[1],
            account=row[2],
            label=row[3],
            amount=row[4],
            category=row[5]
        )
        for row in rows
    ]


if __name__ == "__main__":
    file_test = r"C:\Users\peill\Documents\Python_Scripts\MySmartWallet\data\CIC\Extrait2407.pdf"
    from mysmartwallet.models.parsers.cic import CICParser
    from mysmartwallet.utils.app_config import CONFIG
    DB_PATH = CONFIG.DATA_DIR / "MySmartWallet.db"
    parser = CICParser()
    transactions = parser.parse(file_test)
    repo = TransactionRepository(DatabaseManager(DB_PATH))
    repo.add_many(transactions)

    print(repo.get_all())