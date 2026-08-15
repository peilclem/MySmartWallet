from PySide6.QtWidgets import QFileDialog, QTableView, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
# from mysmartwallet.database.TransactionRepository import TransactionRepository

class TransactionWidget(QWidget):
    import_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction Widget")
        self.setMinimumSize(600, 300)

        self._setup_ui()
        self._connect_signals()


    def _setup_ui(self):
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
        self.import_button.clicked.connect(self._on_import_clicked)

    def _on_import_clicked(self):
        file_path = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")

        if file_path:
            self.import_clicked.emit(file_path[0])

    def set_transactions(self, transactions):
        """
        Remplit la table avec une liste de Transaction
        """
        self.model.setRowCount(0)

        for t in transactions:
            print(f"Ajout de la transaction: {t.date}, {t.label}, {t.amount}")
            row = [
                QStandardItem(str(t.date)),
                QStandardItem(str(t.account)),
                QStandardItem(t.label),
                QStandardItem(f"{t.amount:.2f}"),
                QStandardItem(getattr(t, "category", ""))
            ]

            self.model.appendRow(row)

    def refresh(self, transactions):
        self.set_transactions(transactions=transactions)

