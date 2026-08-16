from mysmartwallet.database.DatabaseManager import DatabaseManager


class BankRepository:
    """Object to manage connection with the bank table in the database
    """
    def __init__(self, db: DatabaseManager):
        """Initialize BankRepository

        Parameters
        ----------
        db : DatabaseManager
            database
        """
        self.db = db

    def add(self, bank_name):
        """Add a new bank to the database

        Parameters
        ----------
        bank_name : str
            Name of the bank to be added
        """
        query = """
        INSERT INTO Banks
        (Bank_name)
        VALUES (?)
        """

        self.db.execute(
            query,
            (
                bank_name
            )
        )

        self.db.commit()

    def check_bank_existence(self, bank_name):
        """Check if a bank exists in the database

        Parameters
        ----------
        bank_name : str
            Name of the bank to check

        Returns
        -------
        bool
            True if the bank exists, False otherwise
        """
        query = """
        SELECT * FROM Banks
        WHERE Bank_name = ?
        """

        cursor = self.db.execute(query, (bank_name,))
        result = cursor.fetchone()

        return result is not None

    def fetch_all(self):
        """Fetch all banks from the database

        Returns
        -------
        list
            List of all banks in the database
        """
        query = """SELECT * FROM Banks"""
        rows = self.db.fetch_all(query)
        return rows