class TransactionController:
    def __init__(self, view, parser, transaction_service, transaction_repository):
        self.view = view
        self.parser = parser
        self.transaction_service = transaction_service
        self.transaction_repository = transaction_repository

        self.view.import_clicked.connect(self.import_transactions)

    def import_transactions(self, file_path):
        transactions = self.parser.parse(file_path)
        self.transaction_service.import_transactions(transactions)
        self.load_transactions_into_view()

    def load_transactions_into_view(self):
        transactions = self.transaction_repository.get_all()
        self.view.refresh(transactions)