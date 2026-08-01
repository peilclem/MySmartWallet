from mysmartwallet.database.DatabaseManager import DatabaseManager

class HistoryRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def add(self, account_id, date, balance):
        query = """
        INSERT INTO History
        (Account_ID, Date, Balance)
        VALUES (?, ?, ?)
        """

        self.db.execute(
            query,
            (
                account_id,
                date,
                balance
            )
        )

        self.db.commit()

    def check_history_existence(self, account_id, date):
        query = """
        SELECT * FROM History
        WHERE Account_ID = ? AND Date = ?
        """

        cursor = self.db.execute(query, (account_id, date))
        result = cursor.fetchone()

        return result is not None

    def fetch_all(self):
        query = """SELECT * FROM History"""
        rows = self.db.fetch_all(query)
        return rows