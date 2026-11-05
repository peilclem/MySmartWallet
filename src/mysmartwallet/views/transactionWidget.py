import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from mysmartwallet.models.transaction import Transaction

logger = logging.getLogger(__name__)


class TransactionWidget(QWidget):
    """Transaction widget to display a table of transactions"""

    importClicked = Signal(str)

    def __init__(self):
        """Initialize the widget"""
        super().__init__()
        self.setWindowTitle("Transaction Widget")
        self.setMinimumSize(600, 300)

        self._setupUi()
        self._connectSignals()

    def _setupUi(self):
        """Create the ui of the widget"""
        layout = QVBoxLayout(self)

        self.title = QLabel("Transactions")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.importButton = QPushButton("Import Transactions")

        self.table = QTableView()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            ["Date", "Account", "Label", "Amount", "Category"]
        )
        self.table.setModel(self.model)

        layout.addWidget(self.title)
        layout.addWidget(self.importButton)
        layout.addWidget(self.table)

    def _connectSignals(self):
        """Signal when button is clicked"""
        self.importButton.clicked.connect(self._onImportClicked)

    def _onImportClicked(self):
        """Action when file button is clicked"""
        logger.info("User clicked import button")
        filePath = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )[0]

        if filePath:
            logger.info("Selected PDF file for import", extra={"filePath": filePath})
            self.importClicked.emit(filePath)

    def setTransactions(self, transactions: list[Transaction]):
        """Fill table with imported transactions

        Parameters
        ----------
        transactions : list[Transaction]
            Newly imported transactions
        """
        self.model.setRowCount(0)

        for t in transactions:
            row = [
                QStandardItem(str(t.date)),
                QStandardItem(str(t.account)),
                QStandardItem(t.label),
                QStandardItem(f"{t.amount:.2f}"),
                QStandardItem(getattr(t, "category", "")),
            ]

            self.model.appendRow(row)

    def refresh(self, transactions: list[Transaction]):
        """Refresh the view

        Parameters
        ----------
        transactions : list[Transaction]
            Transactions to display
        """
        self.setTransactions(transactions=transactions)
