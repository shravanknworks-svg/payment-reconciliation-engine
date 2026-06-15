from pydantic import BaseModel
from typing import List, Dict, Any


class ReconciliationSummary(BaseModel):
    total_internal_records: int
    total_bank_records: int
    matched_records: int
    missing_in_bank: int
    missing_in_internal: int
    amount_mismatches: int
    date_mismatches: int
    duplicate_internal_transactions: int
    duplicate_bank_transactions: int


class ReconciliationResponse(BaseModel):
    summary: ReconciliationSummary
    exceptions: List[Dict[str, Any]]
