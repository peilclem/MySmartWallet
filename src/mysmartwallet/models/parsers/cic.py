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
        self.defaultDate = None

    def extractTables(self, file: str) -> List[pd.DataFrame]:
        """
        Extract tables from PDF using pdfplumber.
        """
        logger.debug("Extracting tables with pdfplumber", extra={"file": file})

        tables = []

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extractedTables = page.extract_tables()

                for table in extractedTables:
                    if table:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        tables.append(df)

        return tables

    def extractTransactionFromTables(self, file: str) -> List[Transaction]:
        """
        Extract transactions from PDF.
        """
        logger.debug("Extracting transactions from PDF", extra={"file": file})

        tables = self.extractTables(file)
        transactions: List[Transaction] = []

        for k, table in enumerate(tables[:-2]):
            table = table.fillna("0")

            for i in range(len(table)):
                row = table.iloc[i]
                transactionDict = {}

                try:
                    if row.iloc[0] != "0":

                        if "SOLDE CREDITEUR" in row["Date"] or "SOLDE DEBITEUR" in row["Opération"]:
                            continue

                        income = self._toFloat(row.iloc[-1])
                        expense = self._toFloat(row.iloc[-2])

                        transactionDict["amount"] = income - expense

                        try:
                            next_row = table.iloc[i + 1]
                            if next_row.iloc[0] == "0":
                                transactionDict["label"] = next_row.iloc[2]
                            else:
                                transactionDict["label"] = row.iloc[2]
                        except IndexError:
                            transactionDict["label"] = row.iloc[2]

                        transactionDict["date"] = self.strToDate(row.iloc[0])

                        if not transactionDict["date"]:
                            transactionDict["date"] = self.defaultDate

                        transactionDict["category"] = "-" #FIXME: Assign default category ?

                        transactions.append(
                            Transaction(**transactionDict, account=str(k))
                        )

                except Exception as e:
                    logger.warning(
                        "Skipping row due to parsing error",
                        extra={"error": str(e)},
                    )
                    continue

        return transactions

    def extractAccountNames(self, file: str) -> Dict[int, str]:
        """
        Extract account names from PDF text.
        """
        logger.debug("Extracting account names", extra={"file": file})

        text = ""

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                pageText = page.extract_text()
                if pageText:
                    text += pageText + "\n"

        lines = text.split("\n")

        linesOfInterest = []
        isOfInterest = False
        try:
            monthDict = {
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
            dateStr = lines[12].split(" ")  # Assuming the date is always on line 13
            dateStr[1] = monthDict.get(dateStr[1].lower(), "01")  # Default to January if not found
            self.defaultDate = self.strToDate(f"{dateStr[0]}/{dateStr[1]}/{dateStr[2]}")
        except IndexError:
            self.defaultDate = self.strToDate("01/01/1900")

        for line in lines:
            if isOfInterest:
                linesOfInterest.append(line)
                isOfInterest = False

            if "€" in line:
                isOfInterest = True

        return self.cleanAccountNames(linesOfInterest)

    def groupTransactionsByAccount(
        self,
        transactions: List[Transaction],
        accountNames: Dict[int, str]
    ) -> List[Transaction]:

        logger.debug("Grouping transactions")

        nbUnknownAccount = 0

        for transaction in transactions:
            transaction.account = accountNames.get(
                int(transaction.account),
                "Unknown Account"
            )

            if transaction.account == "Unknown Account":
                nbUnknownAccount += 1

        if nbUnknownAccount > 0:
            logger.warning(
                "Found transactions with unknown account names",
                extra={"unknown_account_transactions": nbUnknownAccount},
            )

        return transactions

    def cleanAccountNames(self, linesOfInterest: List[str]) -> Dict[int, str]:

        logger.debug("Cleaning account names")

        accountNames: Dict[int, str] = {}
        k = 0

        for line in linesOfInterest:
            lineUpper = line.upper()

            if "C/C" in lineUpper:
                accountNames[k] = "Compte Courant"
                k += 1

            elif "LIVRET A" in lineUpper:
                accountNames[k] = "Livret A"
                k += 1

            elif "DURABLE SOLIDAIRE" in lineUpper:
                accountNames[k] = "LDDS"
                k += 1

            elif "LIVRET JEUNE" in lineUpper:
                accountNames[k] = "Livret JEUNE"
                k += 1

            #FIXME: Replace with Enum ?

        return accountNames

    def _toFloat(self, value: str) -> float:
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
    fileTest = r"C:\Users\peill\Documents\Python_Scripts\MySmartWallet\data\Extrait2311.pdf"

    parser = CICParser()
    transactions = parser.extractTransactionFromTables(fileTest)

    for t in transactions:
        print(t)