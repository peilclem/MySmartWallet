from abc import ABC, abstractmethod
from datetime import datetime

from mysmartwallet.models.transaction import Transaction


class PdfParser(ABC):   
    """
    An abstract base class for parsing PDF files to extract financial transactions.
    """

    def __init__(self):
        pass


    def str_to_datetime(self, date_str:str) -> datetime:
        """Convert string date to datetime

        Parameters
        ----------
        date_str : str
            Date in string format

        Returns
        -------
        datetime
            Date in datetime format
        """
        if isinstance(date_str, str):
            try:
                return datetime.strptime(date_str, '%d/%m/%Y')
            except ValueError:
                return None
        return None

    def parse(self, pdf_file: str) -> list[Transaction]:
        """Parse a bank report

        Parameters
        ----------
        pdf_file : str
            Pdf bank report to parse

        Returns
        -------
        list[Transaction]
            List of all transactions
        """
        transactions_id = self.extract_transaction_from_tables(pdf_file)
        account_names = self.extract_account_names(pdf_file)

        transactions = self.group_transactions_by_account(transactions_id, account_names)

        return transactions


    def group_transactions_by_account(self, transactions:list[Transaction], account_names:dict) -> list[Transaction]:
        """Group transactions by account

        Parameters
        ----------
        transactions : list[Transaction]
            All transactions
        account_names : dict
            Dictionnary of account names associated with table number

        Returns
        -------
        list[Transaction]
            All transactions with an associated account name
        """
        for transaction in transactions:
            account_id = int(transaction.account)
            transaction.account = account_names.get(account_id, "Unknown Account")

        return transactions
    

    @abstractmethod
    def extract_transaction_from_tables(self, file:str) -> list[Transaction]:
        """Abstract method to extract transaction data from tables in a PDF file.
        This method should be implemented by subclasses to handle the specific logic for extracting transaction data from the provided PDF file.

        Parameters
        ----------
        file : str
            Pdf file to parse

        Returns
        -------
        list[Transaction]
            All extracted transactions
        """

    @abstractmethod
    def extract_account_names(self, file:str):
        """Extracts account names from the provided PDF file.
        This method should be implemented by subclasses to handle the specific logic for extracting account names from the provided PDF file.


        Parameters
        ----------
        file : str
            Pdf file to parse
        """