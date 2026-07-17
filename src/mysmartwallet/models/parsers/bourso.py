import tabula
import math
import re
from datetime import datetime

from mysmartwallet.models.parsers.base import PdfParser
from mysmartwallet.models.transaction import Transaction

class BoursoParser(PdfParser):
    def __init__(self, pdf_file):
        super().__init__(pdf_file)

    def extract_transaction_from_tables(self, file) -> list[Transaction]:
        """Extracts transaction data from tables in a Bourso PDF file.
        Args:
            file: The Bourso PDF file from which to extract transaction data.
        Returns:
            List[Transaction]: A list of Transaction objects containing the extracted transaction data.
        """
        tables = tabula.read_pdf(file, encoding='latin-1', pages='all', multiple_tables=True)
        transactions = []
        
        for table in tables:
            t_dict = {}
            for row in table.itertuples():
                label = row[1]
                try:
                    date = datetime.strptime(label[:10], '%d/%m/%Y')
                except Exception:
                    date = None
                if isinstance(date, datetime):
                    t_dict["date"] = date.strftime('%Y/%m/%d')
                    t_dict["amount"] = get_amount(row[-2], row[-1])
                    t_dict["label"] = clean_labels(label[10:])
                    
                    transactions.append(Transaction(**t_dict, account="Compte Courant"))

        return transactions
    
    def extract_account_names(self, file):
        """Extracts account names from a Bourso PDF file.
        Args:
            file: The Bourso PDF file from which to extract account names.
        Returns:
            Dict[int, str]: A dictionary mapping account IDs to account names.
        """
        # Implement the logic to extract account names from Bourso PDF files
        pass

    def get_amount(income, expense):
        if isinstance(income, str) and income.strip() != '':
            income = float(income.replace('.','').replace(',', '.'))
        elif isinstance(income, (int, float)):
            income = float(income)
        else:
            income = 0.0

        
        if isinstance(expense, str) and expense.strip() != '':
            expense = float(expense.replace('.','').replace(',', '.'))
        elif isinstance(expense, (int, float)) and not math.isnan(expense):
            expense = float(expense)
        else:
            expense = 0.0

        return income - expense
    
    def clean_labels(label):
        if "CARTE" in label:
            label = label.split("CARTE")[1].strip()
        
        date_pattern = r"\b\d{2}/\d{2}/\d{2}\b"

        if re.search(date_pattern, label):
            label = re.sub(date_pattern, "", label).strip()

        if 'CB*' in label[-7:]:
            label = label[:-7].strip()
        return label
    

