import logging
from typing import List, Dict

import pdfplumber
import pandas as pd

from mysmartwallet.models.parsers.base import PdfParser
from mysmartwallet.models.transaction import Transaction

logger = logging.getLogger(__name__)


class CICParser(PdfParser):
    """Parser for CIC bank reports (PDF only, no Java dependency)."""

    def __init__(self):
        super().__init__()

    def extract_tables(self, file: str) -> List[pd.DataFrame]:
        """
        Extract tables from PDF using pdfplumber.
        """
        logger.info(f"Extracting tables with pdfplumber from {file}")

        tables = []

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted_tables = page.extract_tables()

                for table in extracted_tables:
                    if table:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        tables.append(df)

        return tables

    def extract_transaction_from_tables(self, file: str) -> List[Transaction]:
        """
        Extract transactions from PDF.
        """
        logger.info(f"Extracting transactions from {file}")

        tables = self.extract_tables(file)
        transactions: List[Transaction] = []

        for k, table in enumerate(tables[:-2]):
            table = table.fillna("0")

            for i in range(len(table)):
                row = table.iloc[i]
                t_dict = {}

                try:
                    if row.iloc[0] != "0":

                        if "SOLDE CREDITEUR" in row["Date"] or "SOLDE DEBITEUR" in row["Opération"]:
                            continue

                        income = self._to_float(row.iloc[-1])
                        expense = self._to_float(row.iloc[-2])

                        t_dict["amount"] = income - expense

                        try:
                            next_row = table.iloc[i + 1]
                            if next_row.iloc[0] == "0":
                                t_dict["label"] = next_row.iloc[2]
                            else:
                                t_dict["label"] = row.iloc[2]
                        except IndexError:
                            t_dict["label"] = row.iloc[2]

                        t_dict["date"] = self.str_to_date(row.iloc[0])

                        if not t_dict["date"]:
                            t_dict["date"] = self.default_date

                        t_dict["category"] = "-" #FIXME: Assign default category ?

                        transactions.append(
                            Transaction(**t_dict, account=str(k))
                        )

                except Exception as e:
                    logger.warning(f"Skipping row due to error: {e}")
                    continue

        return transactions

    def extract_account_names(self, file: str) -> Dict[int, str]:
        """
        Extract account names from PDF text.
        """
        logger.info(f"Extracting account names from {file}")

        text = ""

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        lines = text.split("\n")

        lines_of_interest = []
        is_of_interest = False
        try:
            month_dict = {
                "janvier": "01",
                "février": "02",
                "mars": "03",
                "avril": "04",
                "mai": "05",
                "juin": "06",
                "juillet": "07",
                "août": "08",
                "septembre": "09",
                "octobre": "10",
                "novembre": "11",
                "décembre": "12"
            }
            date_str = lines[12].split(" ")  # Assuming the date is always on line 13
            date_str[1] = month_dict.get(date_str[1].lower(), "01")  # Default to January if not found
            self.default_date = self.str_to_date(f"{date_str[0]}/{date_str[1]}/{date_str[2]}")
        except IndexError:
            self.default_date = self.str_to_date("01/01/1900")

        for line in lines:
            if is_of_interest:
                lines_of_interest.append(line)
                is_of_interest = False

            if "€" in line:
                is_of_interest = True

        return self.clean_account_names(lines_of_interest)

    def group_transactions_by_account(
        self,
        transactions: List[Transaction],
        account_names: Dict[int, str]
    ) -> List[Transaction]:

        logger.info("Grouping transactions")

        unknown_account_nb = 0

        for transaction in transactions:
            transaction.account = account_names.get(
                int(transaction.account),
                "Unknown Account"
            )

            if transaction.account == "Unknown Account":
                unknown_account_nb += 1

        if unknown_account_nb > 0:
            logger.warning(
                f"Found {unknown_account_nb} transactions with unknown account names."
            )

        return transactions

    def clean_account_names(self, lines_of_interest: List[str]) -> Dict[int, str]:

        logger.info("Cleaning account names")

        account_names: Dict[int, str] = {}
        k = 0

        for line in lines_of_interest:
            line_upper = line.upper()

            if "C/C" in line_upper:
                account_names[k] = "Compte Courant"
                k += 1

            elif "LIVRET A" in line_upper:
                account_names[k] = "Livret A"
                k += 1

            elif "DURABLE SOLIDAIRE" in line_upper:
                account_names[k] = "LDDS"
                k += 1

            elif "LIVRET JEUNE" in line_upper:
                account_names[k] = "Livret JEUNE"
                k += 1

        return account_names

    def _to_float(self, value: str) -> float:
        """
        Convert CIC formatted string to float.
        Example: '1.234,56' → 1234.56
        """
        try:
            return float(
                value.replace(".", "").replace(",", ".")
            )
        except Exception:
            return 0.0


if __name__ == "__main__":
    file_test = r"C:\Users\peill\Documents\Python_Scripts\MySmartWallet\data\Extrait2311.pdf"

    parser = CICParser()
    transactions = parser.extract_transaction_from_tables(file_test)

    for t in transactions:
        print(t)