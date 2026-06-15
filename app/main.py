from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from app.reconciliation_service import reconcile_payments
from app.models import ReconciliationResponse

app = FastAPI(
    title="Payment Reconciliation Engine",
    description="Compares internal payment records against bank/vendor settlement files.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "UP"}


@app.post("/reconcile", response_model=ReconciliationResponse)
async def reconcile(
    internal_file: UploadFile = File(...),
    bank_file: UploadFile = File(...),
):
    try:
        internal_df = pd.read_csv(internal_file.file)
        bank_df = pd.read_csv(bank_file.file)
        result = reconcile_payments(internal_df, bank_df)
        return result
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Reconciliation failed: {str(ex)}")
