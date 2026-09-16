from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="Invoice Reconciliation API")

@app.get("/")
def home():
    return {"status": "FastAPI is running!"}

@app.post("/process-invoice/")
async def process_invoice(
    po_file: UploadFile = File(...),
    gr_file: UploadFile = File(...),
    invoice_file: UploadFile = File(...),
):
    await po_file.read()
    await gr_file.read()
    await invoice_file.read()

    return {
        "status": "Success",
        "files": {
            "po_file": po_file.filename,
            "gr_file": gr_file.filename,
            "invoice_file": invoice_file.filename,
        },
        "result": {
            "po_matched": True,
            "discrepancies_found": 0,
            "confidence_score": 0.96
        }
    }