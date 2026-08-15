from mysmartwallet.database.DatabaseManager import DatabaseManager
from mysmartwallet.models.transaction import Transaction


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

    def add_many(self, transactions: list[Transaction]):
        query = """
        INSERT INTO Transactions
        (Date, Account_ID, Label, Amount, Category)
        VALUES (?, ?, ?, ?, ?)
        """

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
    DB_PATH = CONFIG.DATA_DIR + "MySmartWallet.db"
    parser = CICParser(file_test)
    transactions = parser.parse()
    repo = TransactionRepository(DatabaseManager(DB_PATH))
    repo.add_many(transactions)

    print(repo.get_all())