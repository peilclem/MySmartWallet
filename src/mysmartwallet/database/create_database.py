import logging
import sqlite3

from mysmartwallet.config.config import CONFIG

logger = logging.getLogger(__name__)


def create_database():
    """
    Create tables of the database
    """
    logger.debug("Creating database")
    CONFIG.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(CONFIG.DB_PATH))
    cursor = con.cursor()

    # Tables de dimension
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Banks
            (Bank_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Bank_name TEXT NOT NULL
            )
    """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Users
            (User_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Login TEXT NOT NULL UNIQUE,
            Name TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE
            )
    """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Accounts
            (Account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            User_id INTEGER NOT NULL,
            Bank_id INTEGER NOT NULL,
            Type TEXT NOT NULL, --Savings, C/C, crypto ...
            FOREIGN KEY (User_id) REFERENCES Users(User_id),
            FOREIGN KEY (Bank_id) REFERENCES Banks(Bank_id)

            )
    """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS AccountBalances
            (Account_id INTEGER NOT NULL,
            Date DATE NOT NULL,
            Balance REAL NOT NULL,
            FOREIGN KEY (Account_id) REFERENCES Accounts(Account_id),
            UNIQUE (Account_id, Date)
            )
        """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Categories
            (Category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Category_name TEXT NOT NULL,
            Parent_id INTEGER,
            Type TEXT NOT NULL, --Income, Expense, Transfer
            User_id INTEGER NOT NULL,
            FOREIGN KEY (User_id) REFERENCES Users(User_id),
            FOREIGN KEY (Parent_id) REFERENCES Categories(Category_id),
            UNIQUE (Category_name, User_id)
            )
    """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Transactions
            (Transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date DATE NOT NULL,
            Account_id INTEGER NOT NULL,
            Label TEXT NOT NULL,
            Amount REAL NOT NULL,
            Category_id INTEGER,
            FOREIGN KEY (Account_id) REFERENCES Accounts(Account_id),
            FOREIGN KEY (Category_id) REFERENCES Categories(Category_id)
            )
    """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS LabelCategoryMapping
            (Mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Label TEXT NOT NULL,
            Category_id INTEGER NOT NULL,
            User_id INTEGER NOT NULL,
            FOREIGN KEY (Category_id) REFERENCES Categories(Category_id),
            FOREIGN KEY (User_id) REFERENCES Users(User_id),
            UNIQUE (Label, Category_id, User_id)
            )
    """
    )

    # Commit the changes
    con.commit()

    return con


if __name__ == "__main__":
    create_database()
