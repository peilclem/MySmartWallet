import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor

    def fetch_all(self, query):
        cursor = self.execute(query)
        print(cursor.description)
        return cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()