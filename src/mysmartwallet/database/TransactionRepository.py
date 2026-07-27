from mysmartwallet.models.transaction import Transaction
from mysmartwallet.database.DatabaseManager import DatabaseManager

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

if __name__ == "__main__":
    from datetime import datetime
    date = datetime(2025, 2, 15, tzinfo=None)
    transaction = Transaction(
        date=date, 
        amount=31.,
        label="operation",
        account="CIC_C/C",
        category="ven "
    )
    ROOT_DIR = r"C:/Users/peill/Documents/Python_Scripts/MySmartWallet/"
    DB_PATH = ROOT_DIR + "data/MySmartWallet.db"
    db = DatabaseManager(DB_PATH)
    repo = TransactionRepository(db)

    repo.add(transaction)