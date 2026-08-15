from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    """A class representing a financial transaction

    Raises
    ------
    TypeError
        if amount is not a float
    ValueError
        if date is not the right foramt
    """
    date: datetime
    amount: float
    label: str
    account: str
    category: str

    def __post_init__(self):
        """Check value in the object
        """
        # Ensure the amount is a float
        if not isinstance(self.amount, float):
            raise TypeError(f"Amount must be a float, got {type(self.amount).__name__}")
        # Ensure the date is in the correct format (YYYY/MM/DD)
        if isinstance(self.date, str):
            try:
                if '/' in self.date:
                    self.date = datetime.strptime(self.date, '%Y/%m/%d').date()
                elif '-' in self.date:
                    self.date = datetime.strptime(self.date, '%Y-%m-%d').date()

            except ValueError:
                raise ValueError(f"Date must be in YYYY/MM/DD or YYYY-MM-DD format, got {self.date}")