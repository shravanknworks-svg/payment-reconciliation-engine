import pandas as pd
from app.reconciliation_service import reconcile_payments


def test_reconcile_payments():
    internal_df = pd.DataFrame(
        [
            {"transaction_id": "T1", "customer_id": "C1", "amount": 100, "currency": "USD", "payment_date": "2026-01-01", "status": "POSTED"},
            {"transaction_id": "T2", "customer_id": "C2", "amount": 200, "currency": "USD", "payment_date": "2026-01-02", "status": "POSTED"},
        ]
    )

    bank_df = pd.DataFrame(
        [
            {"transaction_id": "T1", "customer_id": "C1", "amount": 100, "currency": "USD", "payment_date": "2026-01-01", "status": "SETTLED"},
            {"transaction_id": "T3", "customer_id": "C3", "amount": 300, "currency": "USD", "payment_date": "2026-01-03", "status": "SETTLED"},
        ]
    )

    result = reconcile_payments(internal_df, bank_df)

    assert result["summary"]["matched_records"] == 1
    assert result["summary"]["missing_in_bank"] == 1
    assert result["summary"]["missing_in_internal"] == 1
