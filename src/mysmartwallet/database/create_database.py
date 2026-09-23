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
            (Bank_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Bank_name TEXT NOT NULL
            )
    """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Users
            (User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Login TEXT NOT NULL UNIQUE,
            Name TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE
            )
    """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Accounts
            (Account_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_ID INTEGER NOT NULL,
            Bank_ID INTEGER NOT NULL,
            Type TEXT NOT NULL, --Savings, C/C, crypto ...
            FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
            FOREIGN KEY (Bank_ID) REFERENCES Banks(Bank_ID)

            )
    """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS AccountBalances
            (Account_ID INTEGER NOT NULL,
            Date DATE NOT NULL,
            Balance REAL NOT NULL,
            FOREIGN KEY (Account_ID) REFERENCES Accounts(Account_ID)
            UNIQUE (Account_ID, Date)
            )
        """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Transactions
            (Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date DATE NOT NULL,
            Account_ID INTEGER NOT NULL,
            Label TEXT NOT NULL,
            Amount REAL NOT NULL,
            Category_ID INTEGER,
            FOREIGN KEY (Account_ID) REFERENCES Accounts(Account_ID),
            FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID)
            )
    """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Categories
            (Category_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Category_name TEXT NOT NULL,
            Parent_ID INTEGER,
            Type TEXT NOT NULL, --Income, Expense, Transfer
            User_ID INTEGER NOT NULL,
            FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
            FOREIGN KEY (Parent_ID) REFERENCES Categories(Category_ID),
            UNIQUE (Category_name, User_ID)
            )
    """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS LabelCategoryMapping
            (Mapping_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Label TEXT NOT NULL,
            Category_ID INTEGER NOT NULL,
            User_ID INTEGER NOT NULL,
            FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID),
            FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
            UNIQUE (Label, Category_ID, User_ID)
            )
    """
    )

    # Commit the changes
    con.commit()

    return con


if __name__ == "__main__":
    create_database()
