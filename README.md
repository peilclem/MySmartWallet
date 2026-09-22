# MySmartWallet

> **Status:** early-stage desktop app prototype for importing bank transactions from PDF statements (currently CIC) and storing/displaying them in a local SQLite database.

## Table of Contents

- [Overview](#overview)
- [What the app does today](#what-the-app-does-today)
- [Architecture](#architecture)
  - [UI (View)](#ui-view)
  - [Controller](#controller)
  - [Services (business logic)](#services-business-logic)
  - [Repositories (persistence)](#repositories-persistence)
  - [PDF parsing](#pdf-parsing)
- [Data model & database](#data-model--database)
- [Supported PDF format](#supported-pdf-format)
- [Configuration](#configuration)
- [Logging](#logging)
- [Development setup](#development-setup)
- [Running locally](#running-locally)
- [Building a Windows executable](#building-a-windows-executable)
- [CI pipeline](#ci-pipeline)
- [Project structure](#project-structure)
- [Known limitations / TODOs](#known-limitations--todos)
- [Extending the project](#extending-the-project)
- [License](#license)

## Overview

**MySmartWallet** is a Python desktop app built with **PySide6** (Qt) that:

1. Lets you select a **PDF** file containing bank transactions.
2. Extracts transactions using a **PDF parser** (currently tailored to CIC statements).
3. Normalizes and categorizes transactions.
4. Persists them in an on-disk **SQLite** database.
5. Displays the stored transactions in a table.

## What the app does today

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

## Known limitations / TODOs

Based on current implementation:

- **Parser specificity:** `CICParser` relies on CIC-specific PDF layouts and heuristics.
- **Category pipeline mismatch:** `CICParser` sets `category` to `"-"`, but `TransactionService` later overwrites it. (This is okay but redundant.)
- **Date assumptions:** CIC parsing uses `default_date` with fallbacks; incorrect PDF formats can lead to wrong dates.
- **No UI editing/filtering:** the UI is display-only besides importing.
- **No duplicate handling:** transactions are simply inserted; there is no explicit deduplication logic in `TransactionRepository`.
- **Potential type mismatch risk:** `Database TransactionRepository.get_all()` constructs `Transaction` with `date=row[1]` (SQLite stores DATE as text/whatever was inserted). If the DB stores strings in a format not covered by `Transaction.__post_init__`, date conversion may fail.

## Extending the project

Ideas for the next iterations:

1. **Add parsers for other banks/formats**
   - Create a new parser class inheriting `PdfParser` (e.g., `SocieteGeneraleParser`).
   - Plug it into `main.py` (or make parser selection configurable).

2. **Improve categorization**
   - Replace the sign-based categorization with rule-based categories keyed on label/merchant.

3. **Add transaction deduplication**
   - Add a `UNIQUE` constraint (e.g., `(Account_ID, Date, Label, Amount)`) or check before insert.

4. **Expand the UI**
   - Filters (by account/category/date)
   - Search
   - Edit/correct transactions

## License

MIT (see `src/mysmartwallet/__init__.py`).