from mysmartwallet.database.DatabaseManager import DatabaseManager


class HistoryRepository:
    """Manage connection with the history table in the database
    """
    def __init__(self, db: DatabaseManager):
        """Initialize HistoryRepository

        Parameters
        ----------
        db : DatabaseManager
            database
        """
        self.db = db

    def add(self, account_id: int, date: str, balance: float):
        """Add a new history entry to the database

        Parameters
        ----------
        account_id : int
            ID of the account
        date : str
            Date of the history entry
        balance : float
            Balance of the account at the given date
        """
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

    def check_history_existence(self, account_id: int, date: str):
        """Check if a history entry exists in the database

        Parameters
        ----------
        account_id : int
            ID of the account
        date : str
            Date of the history entry

        Returns
        -------
        bool
            True if the history entry exists, False otherwise
        """
        query = """
        SELECT * FROM History
        WHERE Account_ID = ? AND Date = ?
        """

        cursor = self.db.execute(query, (account_id, date))
        result = cursor.fetchone()

        return result is not None

    def fetch_all(self):
        """Fetch all history entries from the database
        
        Returns
        -------
        list
            List of all history entries
        """
        query = """SELECT * FROM History"""
        rows = self.db.fetch_all(query)
        return rows