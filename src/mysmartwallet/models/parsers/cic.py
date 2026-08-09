import tabula
import pdfplumber
from datetime import datetime

from mysmartwallet.models.parsers.base import PdfParser
from mysmartwallet.models.transaction import Transaction

class CICParser(PdfParser):
    def __init__(self):
        super().__init__()

    def extract_transaction_from_tables(self, file) -> list[Transaction]:
        """Extracts transaction data from tables in a CIC PDF file.
        Args:
            file: The CIC PDF file from which to extract transaction data.
        Returns:
            List[Transaction]: A list of Transaction objects containing the extracted transaction data.
        """
        tables = tabula.read_pdf(file, pages='all', encoding='latin-1', multiple_tables=True)
        transactions = []
        
        for k, table in enumerate(tables[:-2]):
            table = table.fillna('0')   
            
            for i in range(len(table)):
                row = table.iloc[i]
                t_dict = {}

                if row.iloc[0] != '0':
                    
                    income = float(row.iloc[-2].replace('.','').replace(',', '.'))
                    expense = float(row.iloc[-1].replace('.','').replace(',', '.'))
                    t_dict["amount"] = income - expense 
                    
                    try:
                        next_row = table.iloc[i+1]
                        if next_row.iloc[0] == '0':
                            t_dict["label"] = next_row.iloc[2]
                        else:
                            t_dict["label"] = row.iloc[2]
                    except IndexError:
                        t_dict["label"] = row.iloc[2]

                    # To be implemented in TransactionService
                    t_dict["category"] = None

                    if not 'SOLDE CREDITEUR' in t_dict['label']:
                        date = row.iloc[0]
                        t_dict["date"] = self.str_to_datetime(date).date()
                        transactions.append(Transaction(**t_dict, account=f"{k}"))

                else:
                    continue

        return transactions 
    
    def extract_account_names(self, file):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        text = text.split("\n")

        lines_of_interest, is_of_interest = [], False
        for i, line in enumerate(text):
            if is_of_interest:
                lines_of_interest.append(line)
                is_of_interest = False
            if '€' in line:
                is_of_interest = True

        account_names = self.clean_account_names(lines_of_interest)
        return account_names
    
    def group_transactions_by_account(self, transactions, account_names):
        unknown_account = 0
        for transaction in transactions:
            transaction.account = account_names.get(int(transaction.account), "Unknown Account")
            if transaction.account == "Unknown Account":
                unknown_account += 1
        print(f"Found {unknown_account} transactions with unknown account names.")
        return transactions
    
    def clean_account_names(self, lines_of_interest):
        account_names = {}
        k = 0
        for line in lines_of_interest:

            if 'C/C' in line.upper():
                account_names[k] = 'Compte Courant'
                k += 1
            elif 'LIVRET A' in line.upper():
                account_names[k] = 'Livret A'
                k += 1
            elif 'DURABLE SOLIDAIRE' in line.upper():
                account_names[k] = 'LDDS'
                k += 1
            elif 'LIVRET JEUNE' in line.upper():
                account_names[k] = 'Livret JEUNE'
                k += 1
            else:
                continue

        return account_names
    
if __name__ == "__main__":
    file_test = r"C:\Users\peill\Documents\Python_Scripts\MySmartWallet\data\CIC\Extrait2407.pdf"
    parser = CICParser(file_test)
    transactions = parser.parse()
    for transaction in transactions:
        print(transaction)