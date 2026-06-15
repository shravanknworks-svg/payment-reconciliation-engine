# Payment Reconciliation Engine

## Overview

A FinTech reconciliation platform built using Python, FastAPI, and MongoDB that compares payment records from multiple sources and identifies mismatches, missing transactions, and exceptions.

## Features

- Payment reconciliation
- Exception reporting
- CSV file processing
- REST APIs
- MongoDB integration
- Unit testing with PyTest

## Technology Stack

- Python 3.13
- FastAPI
- MongoDB
- Pandas
- Docker
- PyTest

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

## Run Tests

```bash
pytest
```
## Sample Use Case
This project simulates a FinTech payment reconciliation engine that validates and compares payment records from internal systems and external settlement providers. It automatically identifies mismatches, missing transactions, and exceptions while generating reconciliation reports for business users.

## Sample Request
```text
Internal Payments File (internal_payments.csv)
transaction_id,amount,status
TXN1001,100.00,SUCCESS
TXN1002,250.00,SUCCESS
TXN1003,500.00,SUCCESS
Settlement File (settlement_payments.csv)
transaction_id,amount,status
TXN1001,100.00,SUCCESS
TXN1002,300.00,SUCCESS
TXN1004,700.00,SUCCESS
```
## Sample Response
```json
Reconciliation Summary
{
  "total_internal_transactions": 3,
  "total_settlement_transactions": 3,
  "matched_transactions": 1,
  "amount_mismatches": 1,
  "missing_in_settlement": 1,
  "missing_in_internal": 1
}
Exception Report
[
  {
    "transaction_id": "TXN1002",
    "issue": "Amount Mismatch",
    "internal_amount": 250.00,
    "settlement_amount": 300.00
  },
  {
    "transaction_id": "TXN1003",
    "issue": "Missing in Settlement"
  },
  {
    "transaction_id": "TXN1004",
    "issue": "Missing in Internal System"
  }
]
```

## Author

Shravan K Nellutla