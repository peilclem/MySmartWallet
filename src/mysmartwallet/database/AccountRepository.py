from mysmartwallet.database.DatabaseManager import DatabaseManager


class AccountRepository:
    """Object to manage connection with the account table in the database
    """
    def __init__(self, db: DatabaseManager):
        """Initialize AccountRepository

        Parameters
        ----------
        db : DatabaseManager
            database
        """
        self.db = db

    def add(self, user_id: int, bank_id: int, account_type: str):     
        """Add a new account to the database

        Parameters
        ----------
        user_id : int
            ID of the user to whom the account belongs
        bank_id : int
            ID of the bank to which the account belongs
        account_type : str
            Type of the account
        """
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

    def check_account_existence(self, user_id: int, bank_id: int, account_type: str):
        """Check if an account exists in the database

        Parameters
        ----------
        user_id : int
            ID of the user to whom the account belongs
        bank_id : int
            ID of the bank to which the account belongs
        account_type : str
            Type of the account

        Returns
        -------
        bool
            True if the account exists, False otherwise
        """
        query = """
        SELECT * FROM Accounts
        WHERE User_id = ? AND Bank_ID = ? AND Type = ?
        """

        cursor = self.db.execute(query, (user_id, bank_id, account_type))
        result = cursor.fetchone()

        return result is not None

    def fetch_all(self):
        """Fetch all accounts from the database
        
        Returns
        -------
        list
            List of all accounts in the database
        """
        query = """SELECT * FROM Accounts"""
        rows = self.db.fetch_all(query)
        return rows