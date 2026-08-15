from mysmartwallet.database.DatabaseManager import DatabaseManager


class AccountRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def add(self, user_id, bank_id, account_type):        
        query = """
        INSERT INTO Accounts
        (User_id, Bank_ID, Type)
        VALUES (?, ?, ?)
        """

        self.db.execute(
            query,
            (
                user_id,
                bank_id,
                account_type
            )
        )

        self.db.commit()

    def check_account_existence(self, user_id, bank_id, account_type):
        query = """
        SELECT * FROM Accounts
        WHERE User_id = ? AND Bank_ID = ? AND Type = ?
        """

        cursor = self.db.execute(query, (user_id, bank_id, account_type))
        result = cursor.fetchone()

        return result is not None

    def fetch_all(self):
        query = """SELECT * FROM Accounts"""
        rows = self.db.fetch_all(query)
        return rows