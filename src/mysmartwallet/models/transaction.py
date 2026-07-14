from dataclasses import dataclass
import datetime

@dataclass
class Transaction:
    """
    A class representing a financial transaction.

    Attributes: 
    date (datetime): The date of the transaction.
    amount (float): The amount of the transaction.
    label (str): A label for the transaction.
    account (str): The account associated with the transaction.
    """
    date: datetime
    amount: float
    label: str
    account: str
