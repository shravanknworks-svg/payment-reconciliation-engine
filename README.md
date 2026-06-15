# Payment Reconciliation Engine - Python FastAPI

A FinTech-style payment reconciliation service that compares an internal payment file against a bank/vendor settlement file and identifies:

- Matched payments
- Missing in bank file
- Missing in internal file
- Amount mismatches
- Duplicate transactions
- Date mismatches

## Tech Stack

- Python 3.10+
- FastAPI
- Pandas
- Uvicorn
- Pytest

## Project Structure

```text
payment-reconciliation-engine/
├── app/
│   ├── main.py
│   ├── reconciliation_service.py
│   └── models.py
├── sample_files/
│   ├── internal_payments.csv
│   └── bank_settlement.csv
├── tests/
│   └── test_reconciliation.py
├── requirements.txt
└── README.md
```

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

## API Endpoint

### POST /reconcile

Upload two CSV files:

- `internal_file`
- `bank_file`

The API returns reconciliation summary and detailed exception records.

## Expected CSV Columns

Both files should contain:

```text
transaction_id,customer_id,amount,currency,payment_date,status
```

## Example GitHub Resume Bullet

Developed a Python-based Payment Reconciliation Engine using FastAPI and Pandas to compare internal payment records against external bank settlement files, identify exceptions, generate reconciliation summaries, and support audit-ready financial operations.
