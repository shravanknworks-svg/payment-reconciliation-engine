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

## Author

Shravan Kumar Nellutla