from abc import ABC, abstractmethod
from datetime import datetime

from mysmartwallet.models.transaction import Transaction

class PdfParser(ABC):   
    """
    An abstract base class for parsing PDF files to extract financial transactions.
    """

    def __init__(self, pdf_file):
        self.pdf_file = pdf_file


    def str_to_datetime(self, date_str) -> datetime:
        """
        Converts a date string in the format 'dd/mm/yyyy' to a datetime object.
        Args:
            date_str (str): The date string to convert.
        Returns:
            datetime: A datetime object representing the date, or None if the conversion fails. 
        """
        if isinstance(date_str, str):
            try:
                return datetime.strptime(date_str, '%d/%m/%Y')
            except ValueError:
                return None
        return None

    def parse(self) -> list[Transaction]:
        """
        Parses the PDF file and extracts transactions.

        Returns:
            List[Transaction]: A list of Transaction objects extracted from the PDF file.
        """
        transactions_id = self.extract_transaction_from_tables(self.pdf_file)
        account_names = self.extract_account_names(self.pdf_file)

        transactions = self.group_transactions_by_account(transactions_id, account_names)

        return transactions


    def group_transactions_by_account(self, transactions, account_names) -> list[Transaction]:
        """
        Associate an account to each transactions
        This method should be implemented by subclasses to handle the specific logic for grouping transactions by account.

        Args:
            table: The table containing transaction data.
            account_names: A list of account names to group transactions by.
        Returns:
            List[Transaction]: A list of Transaction objects grouped by account.
        """
        for transaction in transactions:
            account_id = int(transaction.account)
            transaction.account = account_names[account_id] if account_id in account_names else "Unknown Account"

        return transactions
    

    @abstractmethod
    def extract_transaction_from_tables(self, file) -> list[Transaction]:
        """
        Abstract method to extract transaction data from tables in a PDF file.
        This method should be implemented by subclasses to handle the specific logic for extracting transaction data from the provided PDF file.
        Args:
            file: The PDF file from which to extract transaction data."""
        pass


    @abstractmethod
    def extract_account_names(self, file):
        """
        Extracts account names from the provided PDF file.
        This method should be implemented by subclasses to handle the specific logic for extracting account names from the provided PDF file.
        Args:
            file: The PDF file from which to extract account names.
        Returns:
            dict[int, str]: A dictionary mapping table indices to account names extracted from the PDF file.
        """
        pass