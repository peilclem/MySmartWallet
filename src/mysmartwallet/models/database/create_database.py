import os
import sqlite3

ROOT_DIR = r"C:/Users/peill/Documents/Python_Scripts/MySmartWallet"

def create_database():
    """
    Create tables of the database
    """
    con = sqlite3.connect(ROOT_DIR / "data/MySmartWallet.db")
    cursor = con.cursor()
    
    # Tables de dimension
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS D_Date
                   (Date_ID INTEGER PRIMARY KEY, --YYYYMM
                    Month TEXT NOT NULL,
                    Quarter TEXT NOT NULL,
                    Year INTEGER NOT NULL
                    )
    ''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS D_Bank
                   (Wallet_ID TEXT PRIMARY KEY,
                    Bank TEXT NOT NULL,
                    Enveloppe TEXT NOT NULL
                    )
    ''')
    
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS D_Balance
                    (Balance_ID TEXT PRIMARY KEY,
                    Username TEXT NOT NULL,
                    Date_ID INTEGER NOT NULL,
                    Wallet_ID TEXT NOT NULL,
                    Solde_IN REAL NOT NULL,
                    Solde_OUT REAL NOT NULL,
                    FOREIGN KEY (Date_ID) REFERENCES D_Date(Date_ID),
                    FOREIGN KEY (Wallet_ID) REFERENCES D_Bank(Wallet_ID),
                    UNIQUE (Username, Date_ID, Wallet_ID)
                    )
    ''')
    
    # Table de fait
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS F_Transactions
                   (Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Username TEXT NOT NULL,
                    Date_ID INTEGER NOT NULL,
                    Wallet_ID TEXT NOT NULL,
                    Libelle TEXT NOT NULL,
                    Montant REAL NOT NULL,
                    Categorie TEXT NOT NULL,
                    FOREIGN KEY (Date_ID) REFERENCES D_Date(Date_ID),
                    FOREIGN KEY (Wallet_ID) REFERENCES D_Bank(Wallet_ID)
                    )
    ''')
    
    # Commit the changes
    con.commit()
    
    return con

def connect_database():
    """ Connect to database (or creeate if not exists) """
    if "MySmartWallet.db" not in os.listdir(ROOT_DIR / "data"):
        con = create_database()
    else:
        con = sqlite3.connect(ROOT_DIR / "data/MySmartWallet.db")
    return con
