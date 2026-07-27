from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    """
    A class representing a financial transaction.

    Attributes: 
    date (datetime): The date of the transaction. YYYY/MM/DD format.
    amount (float): The amount of the transaction.
    label (str): A label for the transaction.
    account (str): The account associated with the transaction.
    category (str): The category of the transsaction
    """
    date: datetime
    amount: float
    label: str
    account: str
    category: str

    def __post_init__(self):
        # Ensure the amount is a float
        if not isinstance(self.amount, float):
            raise ValueError(f"Amount must be a float, got {type(self.amount).__name__}")
        # Ensure the date is in the correct format (YYYY/MM/DD)
        if isinstance(self.date, str):
            try:
                self.date = datetime.strptime(self.date, '%Y/%m/%d').date()
            except ValueError:
                raise ValueError(f"Date must be in YYYY/MM/DD format, got {self.date}")
