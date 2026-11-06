import logging

from mysmartwallet.database.DatabaseManager import DatabaseManager

logger = logging.getLogger(__name__)


class AccountRepository:
    """Object to manage connection with the account table in the database"""

    def __init__(self, db: DatabaseManager):
        """Initialize AccountRepository

        Parameters
        ----------
        db : DatabaseManager
            database
        """
        self.db = db

    def add(self, userId: int, bankId: int, accountType: str):
        """Add a new account to the database

        Parameters
        ----------
        userId : int
            ID of the user to whom the account belongs
        bankId : int
            ID of the bank to which the account belongs
        accountType : str
            Type of the account
        """
        logger.info(
            "Adding account",
            extra={"userId": userId, "bankId": bankId, "accountType": accountType},
        )
        query = """
        INSERT INTO Accounts
        (User_id, Bank_id, Type)
        VALUES (?, ?, ?)
        """

        self.db.execute(query, (userId, bankId, accountType))

        self.db.commit()

    def checkAccountExistence(self, userId: int, bankId: int, accountType: str):
        """Check if an account exists in the database

        Parameters
        ----------
        userId : int
            ID of the user to whom the account belongs
        bankId : int
            ID of the bank to which the account belongs
        accountType : str
            Type of the account

        Returns
        -------
        bool
            True if the account exists, False otherwise
        """
        logger.debug(
            "Checking account existence",
            extra={"userId": userId, "bankId": bankId, "accountType": accountType},
        )
        query = """
        SELECT * FROM Accounts
        WHERE User_id = ? AND Bank_id = ? AND Type = ?
        """

        cursor = self.db.execute(query, (userId, bankId, accountType))
        result = cursor.fetchone()

        return result is not None

    def fetchAll(self):
        """Fetch all accounts from the database

        Returns
        -------
        list
            List of all accounts in the database
        """
        logger.debug("Fetching all accounts")
        query = """SELECT * FROM Accounts"""
        rows = self.db.fetchAll(query)
        return rows
