from mysmartwallet.database.DatabaseManager import DatabaseManager

class BankRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def add(self, bank_name):
        bank_exists = self.check_bank_existence(bank_name)

        if bank_exists:
            return
        
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
        query = """
        SELECT * FROM Banks
        WHERE Bank_name = ?
        """

        cursor = self.db.execute(query, (bank_name,))
        result = cursor.fetchone()

        return result is not None

    def fetch_all(self):
        query = """SELECT * FROM Banks"""
        rows = self.db.fetch_all(query)
        return rows