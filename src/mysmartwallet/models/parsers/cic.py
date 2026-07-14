import tabula

from mysmartwallet.models.parsers.base import PdfParser
from mysmartwallet.models.transaction import Transaction

class CICParser(PdfParser):
    def __init__(self, pdf_file):
        super().__init__(pdf_file)

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
                    t_dict["date"] = row.iloc[0]
                    income = float(row.iloc[-2].replace('.','').replace(',', '.'))
                    expense = float(row.iloc[-1].replace('.','').replace(',', '.'))
                    t_dict["amount"] = income - expense # either expense or income, so we subtract the two to get the correct amount

                    try:
                        next_row = table.iloc[i+1]
                        if next_row.iloc[0] == '0':
                            t_dict["label"] = next_row.iloc[2]
                        else:
                            t_dict["label"] = row.iloc[2]
                    except IndexError:
                        t_dict["label"] = row.iloc[2]


                    if not 'SOLDE CREDITEUR' in t_dict['label']:
                        transactions.append(Transaction(**t_dict, account=f"{k}"))

                else:
                    continue

        return transactions 
    
    def extract_account_names(self, file):
        # Implement the logic to extract account names from the CIC PDF file
        # This is a placeholder implementation; you should replace it with actual account name extraction logic.
        return {}
    
    def group_transactions_by_account(self, transactions, account_names):
        # Implement the logic to group transactions by account for the CIC PDF file
        # This is a placeholder implementation; you should replace it with actual grouping logic.
        return []
    
