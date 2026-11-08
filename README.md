# MySmartWallet

> **Status:** early-stage desktop app prototype for importing bank transactions from PDF statements (currently CIC) and storing/displaying them in a local SQLite database.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Data model & database](#data-model--database)
- [Supported PDF format](#supported-pdf-format)
- [Configuration](#configuration)
- [Logging](#logging)
- [Development setup](#development-setup)
- [Running locally](#running-locally)
- [Building a Windows executable](#building-a-windows-executable)
- [CI pipeline](#ci-pipeline)
- [Project structure](#project-structure)
- [Development Roadmap](#app-roadmap)
- [License](#license)

## Overview

**MySmartWallet** is a Python desktop app built with **PySide6** (Qt) that:

1. Lets you select a **PDF** file containing bank transactions.
2. Extracts transactions using a **PDF parser** (currently tailored to CIC statements).
3. Normalizes and categorizes transactions.
4. Persists them in an on-disk **SQLite** database.
5. Displays the stored transactions in a table.

### What the app does today

- Opens a small GUI window titled **“Transaction Widget”**.
- Provides an **“Import Transactions”** button.
- When you select a PDF:
  - Parses it into a list of `Transaction` objects.
  - Cleans/normalizes labels.
  - Categorizes each transaction as `Income` or `Expense` based on the sign of the amount.
  - Saves transactions into SQLite table `Transactions`.
  - Reloads and refreshes the table view with all transactions sorted by most recent date.

## Repo architecture

The project is organized as a small MVC-ish stack:

### `views/` (Qt UI)

- `mysmartwallet.views.transaction_widget.TransactionWidget`
  - Import button + table display
  - Emits a signal with the selected PDF path

### `controllers/` (coordination)

- `mysmartwallet.controllers.transaction_controller.TransactionController`
  - Connects: view ↔ parser ↔ service ↔ repository
  - On import: parse → process → persist → reload UI

### `services/` (processing)

- `mysmartwallet.services.transaction_service.TransactionService`
  - Filters/normalizes parsed transactions
  - Assigns a basic category (`Income`/`Expense`)
  - Saves them through the repository

### `database/` (SQLite)

- `DatabaseManager`: SQLite connection + auto-create DB
- `TransactionRepository`: insert + list transactions
- Also present: repositories for `Banks`, `Accounts`, `History`

### `models/parsers/` (PDF extraction)

- `PdfParser`: shared parsing flow
- `CICParser`: CIC-specific extraction from PDF tables/text (uses `pdfplumber`/`pandas`)

## Data model & database

### Transaction object

- `mysmartwallet.models.transaction.Transaction`
  - `date`, `amount`, `label`, `account`, `category`

### SQLite schema

- DB schema is created by `mysmartwallet.database.create_database.create_database()`.
- Tables: `Banks`, `Users`, `Accounts`, `History`, `Transactions`.
- The current GUI flow mainly reads/writes `Transactions`.

## Supported PDF format

Today, parsing is implemented specifically for **CIC bank statement PDFs**.

The extraction logic relies on:
- `pdfplumber` table extraction
- assumptions about table structure / row/column positions
- heuristics for account naming and a “default date” fallback

If your PDF differs, parsing may fail or skip rows.

## Configuration

- `mysmartwallet.config.config.CONFIG` is loaded at import time.
- Config is defined by:
  - `ROOT_DIR`
  - `DATA_DIR`
  - `DB_PATH` (stored as `data/MySmartWallet.db`)
  - `LOG_FILE` (stored as `logs/app.log`)
  - `LOG_LEVEL` (currently `logging.DEBUG`)

Implication:
- the app writes the SQLite DB under the project `data/` directory.

## Logging

Logging is initialized in `mysmartwallet.utils.log_mgr.init_logger()`.

- Console logging to stdout
- File logging to `logs/app.log`
- It reduces verbosity of common PDF libraries by setting their logger level to `WARNING`.

## Development setup

Dependencies are managed via `uv` (see `uv.lock` and `pyproject.toml`).

Main dependencies:
- `pyside6` (GUI)
- `pdfplumber` + `pandas` (PDF parsing)
- `sqlite3` (built-in)
- `numpy`, `matplotlib` (present as dependencies though not used in the code paths shown so far)
- `ruff` (linting)
- `jpype1` (present as dependency; not obviously used in the shown code)

## Running locally

1. Ensure Python 3.14+ is available (project requires `>=3.14`).
2. Install dependencies:
   - `uv sync`
3. Run the app:
   - `uv run python src/mysmartwallet/main.py`

## Building a Windows executable

The repository includes both:
- `justfile` with a `build` recipe
- GitHub Actions workflow that runs PyInstaller on Windows

Local build (via `just`):

- `just build`

Expected outputs:
- `dist/MSW.exe`
- `dist/MSW.zip` (a zip of dist contents)

## CI pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`):

- **Quality** job (Ubuntu):
  - `uv sync`
  - `ruff check src/`
- **documentation** job (Ubuntu):
  - `sphinx-build -W -b html docs ...`
- **build** job (Windows, only on `master`):
  - build executable with `pyinstaller --onefile --windowed`
  - package into a zip and upload as an artifact

## Project structure

- `src/mysmartwallet/main.py`
  - application entry point
- `src/mysmartwallet/controllers/`
  - controller wiring
- `src/mysmartwallet/views/`
  - Qt widgets
- `src/mysmartwallet/services/`
  - cleaning/categorization logic
- `src/mysmartwallet/models/`
  - `transaction.py`
  - `parsers/`
    - `base.py`
    - `cic.py`
- `src/mysmartwallet/database/`
  - SQLite connection + repository classes
- `resources/icons/`
  - application icon(s)
- `data/`
  - SQLite DB file (created on first run)
- `logs/`
  - application log file


## App roadmap

Below is the chronological plan for the next app versions. (Focus: getting semi-automatic categorization → dashboard reports → richer UI → more banks → customization → new asset modules.)

### v0.2 (Semi-automatic categorization)
- Semi-automatic categorization driven by **history**:
  - Save a `Label → Category` mapping when the user confirms/corrects a category.
  - On new PDF import, reuse the saved mapping for matching labels.
  - If no mapping exists: prompt the user to select a category (Income/Expense/Transfer or sub-category).
- Add UI/UX hooks to confirm category decisions during import (minimum viable popup).

### v1.0 (Single dashboard + import flow)
- Create a **one-page dashboard** that includes:
  - An **Import Transactions** button.
  - A popup/modal flow to choose a PDF, parse it, and perform categorization (including the “ask user when unknown” step).
  - A table view (existing) plus basic summaries (totals by day/week/month, Income vs Expense, etc.).

### v1.x (More PDF parsers)
- Add more parsers so other banks/formats work:
  - Introduce new `PdfParser` subclasses (e.g., `SocieteGeneraleParser`).
  - Add parser selection (or auto-detection by PDF layout heuristics).

### v1.x (Category customization)
- Let the user customize categories:
  - Create/edit categories.
  - Manage parent/child categories.
  - Update mappings if the user changes their category definitions.

### v2.0 (Multi-page / multi-layout reports)
- Expand to a multi-page/multi-layout UI with dynamic reports:
  - Monthly reports
  - Yearly reports
  - Cashflow
- Use the structure/style inspiration from `resources/msw_layout.pptx`.

### v3.0+ (Investments / additional asset tracking)
- Add new modules beyond bank transactions:
  - Stock market investment performance tracking.
  - Real estate investment tracking.


## License

MIT (see `src/mysmartwallet/__init__.py`).

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