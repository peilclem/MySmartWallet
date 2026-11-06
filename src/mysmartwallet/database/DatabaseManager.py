import sqlite3
from pathlib import Path


class DatabaseManager:
    """Manage connection with the database"""

    def __init__(self, dbPath: Path):
        """Initialize DatabaseManager

        Parameters
        ----------
        dbPath : str
            Path to the database file
        """
        if not Path.exists(dbPath):
            from mysmartwallet.database.createDatabase import createDatabase

            createDatabase()

        self.conn = sqlite3.connect(str(dbPath))

    def execute(self, query: str, params: tuple = ()):
        """Execute a query

        Parameters
        ----------
        query : str
            SQL query to execute
        params : tuple, optional
            Parameters for the SQL query, by default ()

        Returns
        -------
        sqlite3.Cursor
            Cursor object for the executed query
        """
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor

    def executeMany(self, query: str, data: list):
        """Execute many identical queries

        Parameters
        ----------
        query : str
            SQL query to execute
        data : list
            List of parameter tuples for the SQL query
        """
        cursor = self.conn.cursor()
        cursor.executemany(query, data)
        return cursor

    def fetchAll(self, query: str):
        """Get all results from a query

        Parameters
        ----------
        query : str
            SQL query to execute

        Returns
        -------
        list
            List of all results from the query
        """
        cursor = self.execute(query)
        return cursor.fetchall()

    def commit(self):
        """Commit query"""
        self.conn.commit()

    def close(self):
        """Close connection with the database"""
        self.conn.close()
