import sqlite3
from mysmartwallet.utils.app_config import CONFIG

ROOT_DIR = CONFIG.ROOT_DIR
DB_PATH = CONFIG.DB_PATH

def create_database():
    """
    Create tables of the database
    """
        
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    
    # Tables de dimension
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Banks
                   (Bank_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Bank_name TEXT NOT NULL
                    )
    ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Users
                   (User_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Login TEXT NOT NULL UNIQUE,
                    Name TEXT NOT NULL,
                    Email TEXT NOT NULL UNIQUE
                    )
    ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Accounts
                   (Account_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    User_id INTEGER NOT NULL,
                    Bank_ID INTEGER NOT NULL,
                    Type TEXT NOT NULL, --Savings, C/C, crypto ...
                    FOREIGN KEY (User_id) REFERENCES Users(User_id),
                    FOREIGN KEY (Bank_ID) REFERENCES Users(Bank_ID)

                    )
    ''')

    cursor.execute('''
                       CREATE TABLE IF NOT EXISTS History
                       (Account_id INTEGER NOT NULL,
                        Date DATE NOT NULL,
                        Balance REAL NOT NULL,
                        FOREIGN KEY (Account_id) REFERENCES Account(Account_id)
                        UNIQUE (Account_id, Date)
                        )
        ''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Transactions
                   (Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Date DATE NOT NULL,
                    Account_ID INTEGER NOT NULL,
                    Label TEXT NOT NULL,
                    Amount REAL NOT NULL,
                    Category TEXT,
                    FOREIGN KEY (Account_ID) REFERENCES Accounts(Account_ID)
                    )
    ''')
    
    # Commit the changes
    con.commit()
    
    return con




if __name__ == '__main__':
    create_database()