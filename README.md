# MySmartWallet

## Code style / naming conventions (Python)

This project follows these naming conventions to keep code consistent and avoid `snake_case` anywhere.

| Element type | Required casing | Example | Notes |
|---|---|---|---|
| Variables | `camelCase` | `userId`, `filePath`, `transactionRepository` | Applies to local variables and instance attributes (unless otherwise specified). |
| Methods / functions | `camelCase` | `loadConfig()`, `fetchAll()`, `importTransactions()` | Prefer verbs in `camelCase`. |
| Classes | `PascalCase` | `TransactionRepository`, `AccountRepository` | Class names are `PascalCase`. |
| Constants | `CAPITAL_LETTERS` | `MAX_RETRIES`, `DEFAULT_LOG_LEVEL` | Use `CAPITAL_LETTERS` with underscores. |
| Other identifiers | “best according to convention” (but **no `snake_case`**) | `__dunder__` is allowed | Python special `__dunder__` names are permitted. |
| File names (Python modules) | `lowerCamelCase` | `transactionController.py`, `createDatabase.py` | This project avoids underscores in file/module names as well. |