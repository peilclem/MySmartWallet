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


class TransactionWidget(QWidget):
    """Transaction widget to display a table of transactions
    """
    import_clicked = Signal(str)

    def __init__(self):
        """Initialize the widget
        """
        super().__init__()
        self.setWindowTitle("Transaction Widget")
        self.setMinimumSize(600, 300)

        self._setup_ui()
        self._connect_signals()


    def _setup_ui(self):
        """Create the ui of the widget
        """
        layout = QVBoxLayout(self)

        self.title = QLabel("Transactions")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.import_button = QPushButton("Import Transactions")

        self.table = QTableView()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Date", "Account", "Label", "Amount", "Category"])
        self.table.setModel(self.model)

        layout.addWidget(self.title)
        layout.addWidget(self.import_button)
        layout.addWidget(self.table)

    def _connect_signals(self):
        """Signal when button is clicked
        """
        self.import_button.clicked.connect(self._on_import_clicked)

    def _on_import_clicked(self):
        """Action when file button is clicked
        """
        file_path = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")

        if file_path:
            self.import_clicked.emit(file_path[0])

    def set_transactions(self, transactions:Transaction):
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
                QStandardItem(getattr(t, "category", ""))
            ]

            self.model.appendRow(row)

    def refresh(self, transactions:list[Transaction]):
        """Refresh the view

        Parameters
        ----------
        transactions : list[Transaction]
            Transactions to display
        """
        self.set_transactions(transactions=transactions)

