import os
import sqlite3


class DatabaseManager:
    """Manage connection with the database
    """
    def __init__(self, db_path:str):
        """Initialize DatabaseManager

        Parameters
        ----------
        db_path : str
            Path to the database file
        """
        if not os.path.exists(db_path):
            from mysmartwallet.database.create_database import create_database
            create_database()

        self.conn = sqlite3.connect(db_path)

    def execute(self, query:str, params:tuple=()):
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

    def executemany(self, query:str, data:list):
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

    def fetch_all(self, query:str):
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
        """Commit query
        """
        self.conn.commit()

    def close(self):
        """Close connection with the database
        """
        self.conn.close()