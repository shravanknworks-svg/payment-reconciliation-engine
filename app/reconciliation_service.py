import pandas as pd
from typing import Dict, Any, List

REQUIRED_COLUMNS = {
    "transaction_id",
    "customer_id",
    "amount",
    "currency",
    "payment_date",
    "status",
}


def validate_columns(df: pd.DataFrame, file_name: str) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"{file_name} is missing required columns: {sorted(missing)}")


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["transaction_id"] = df["transaction_id"].astype(str).str.strip()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["currency"] = df["currency"].astype(str).str.upper().str.strip()
    df["status"] = df["status"].astype(str).str.upper().str.strip()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").round(2)
    df["payment_date"] = pd.to_datetime(df["payment_date"], errors="coerce").dt.date
    return df


def find_duplicates(df: pd.DataFrame, source: str) -> List[Dict[str, Any]]:
    duplicate_rows = df[df.duplicated(subset=["transaction_id"], keep=False)]
    exceptions = []
    for _, row in duplicate_rows.iterrows():
        exceptions.append(
            {
                "exception_type": f"DUPLICATE_{source.upper()}_TRANSACTION",
                "transaction_id": row["transaction_id"],
                "customer_id": row["customer_id"],
                "amount": row["amount"],
                "payment_date": str(row["payment_date"]),
                "source": source,
            }
        )
    return exceptions


def reconcile_payments(internal_df: pd.DataFrame, bank_df: pd.DataFrame) -> Dict[str, Any]:
    validate_columns(internal_df, "internal_file")
    validate_columns(bank_df, "bank_file")

    internal_df = normalize_dataframe(internal_df)
    bank_df = normalize_dataframe(bank_df)

    duplicate_internal = find_duplicates(internal_df, "internal")
    duplicate_bank = find_duplicates(bank_df, "bank")

    # Keep first record for reconciliation comparison after capturing duplicates.
    internal_unique = internal_df.drop_duplicates(subset=["transaction_id"], keep="first")
    bank_unique = bank_df.drop_duplicates(subset=["transaction_id"], keep="first")

    merged = internal_unique.merge(
        bank_unique,
        on="transaction_id",
        how="outer",
        suffixes=("_internal", "_bank"),
        indicator=True,
    )

    exceptions: List[Dict[str, Any]] = []
    exceptions.extend(duplicate_internal)
    exceptions.extend(duplicate_bank)

    matched_records = 0
    amount_mismatches = 0
    date_mismatches = 0
    missing_in_bank = 0
    missing_in_internal = 0

    for _, row in merged.iterrows():
        transaction_id = row["transaction_id"]

        if row["_merge"] == "left_only":
            missing_in_bank += 1
            exceptions.append(
                {
                    "exception_type": "MISSING_IN_BANK",
                    "transaction_id": transaction_id,
                    "customer_id": row.get("customer_id_internal"),
                    "amount_internal": row.get("amount_internal"),
                    "payment_date_internal": str(row.get("payment_date_internal")),
                }
            )
            continue

        if row["_merge"] == "right_only":
            missing_in_internal += 1
            exceptions.append(
                {
                    "exception_type": "MISSING_IN_INTERNAL",
                    "transaction_id": transaction_id,
                    "customer_id": row.get("customer_id_bank"),
                    "amount_bank": row.get("amount_bank"),
                    "payment_date_bank": str(row.get("payment_date_bank")),
                }
            )
            continue

        amount_internal = row.get("amount_internal")
        amount_bank = row.get("amount_bank")
        date_internal = row.get("payment_date_internal")
        date_bank = row.get("payment_date_bank")

        has_exception = False

        if amount_internal != amount_bank:
            amount_mismatches += 1
            has_exception = True
            exceptions.append(
                {
                    "exception_type": "AMOUNT_MISMATCH",
                    "transaction_id": transaction_id,
                    "amount_internal": amount_internal,
                    "amount_bank": amount_bank,
                }
            )

        if date_internal != date_bank:
            date_mismatches += 1
            has_exception = True
            exceptions.append(
                {
                    "exception_type": "DATE_MISMATCH",
                    "transaction_id": transaction_id,
                    "payment_date_internal": str(date_internal),
                    "payment_date_bank": str(date_bank),
                }
            )

        if not has_exception:
            matched_records += 1

    summary = {
        "total_internal_records": len(internal_df),
        "total_bank_records": len(bank_df),
        "matched_records": matched_records,
        "missing_in_bank": missing_in_bank,
        "missing_in_internal": missing_in_internal,
        "amount_mismatches": amount_mismatches,
        "date_mismatches": date_mismatches,
        "duplicate_internal_transactions": len(duplicate_internal),
        "duplicate_bank_transactions": len(duplicate_bank),
    }

    return {"summary": summary, "exceptions": exceptions}
