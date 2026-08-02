import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path):
        if not os.path.exists(db_path):
            from mysmartwallet.database.create_database import create_database
            create_database()

        self.conn = sqlite3.connect(db_path)

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor

    def executemany(self, query, data):
        cursor = self.conn.cursor()
        cursor.executemany(query, data)
        return cursor

    def fetch_all(self, query):
        cursor = self.execute(query)
        print(cursor.description)
        return cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()