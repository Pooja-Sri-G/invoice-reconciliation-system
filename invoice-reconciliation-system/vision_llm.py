import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
FALLBACK_MODEL_NAME = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.1-flash-lite")
LAST_RESORT_MODEL_NAME = os.getenv("GEMINI_LAST_RESORT_MODEL", "gemini-flash-latest")
MAX_RETRIES = 2


def analyze_documents(
    po_filename: str,
    po_bytes: bytes,
    gr_filename: str,
    gr_bytes: bytes,
    invoice_filename: str,
    invoice_bytes: bytes,
) -> str:
    """Analyze PDFs in the caller's process; this function never contacts our API."""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from environment variables.")

    client = genai.Client(api_key=api_key)

    prompt = """
You are an expert invoice reconciliation assistant.

You are given three PDF documents:
1. Purchase Order (PO)
2. Goods Received Note (GRN)
3. Commercial Invoice

Perform a strict 3-way match across these three documents.

Compare:
- PO Number, GRN Number, and Invoice Number
- Vendor / Supplier Name
- Line-item details (Quantities ordered vs received vs billed)
- Unit Prices and Totals

Format your final response clearly using this exact structure:

STATUS: [MATCHED or NEEDS REVIEW]

SUMMARY OF DOCUMENTS:
- Purchase Order: [PO Number]
- Goods Received Note: [GRN Number]
- Invoice: [Invoice Number]
- Supplier Name: [Supplier]

DISCREPANCIES FOUND:
- [List each discrepancy clearly, e.g., line item quantity mismatches or price differences]
- [If no discrepancies exist, state "None"]

RECOMMENDED ACTION:
[Provide a 1-2 sentence recommendation for the finance team]
"""

    # Convert PDF byte buffers into official Gemini Parts
    po_part = types.Part.from_bytes(data=po_bytes, mime_type="application/pdf")
    gr_part = types.Part.from_bytes(data=gr_bytes, mime_type="application/pdf")
    invoice_part = types.Part.from_bytes(data=invoice_bytes, mime_type="application/pdf")

    contents = [
        prompt,
        f"\n--- DOCUMENT 1: Purchase Order ({po_filename}) ---",
        po_part,
        f"\n--- DOCUMENT 2: Goods Received Note ({gr_filename}) ---",
        gr_part,
        f"\n--- DOCUMENT 3: Commercial Invoice ({invoice_filename}) ---",
        invoice_part,
    ]

    last_error = None
    models_to_try = [MODEL_NAME]
    if FALLBACK_MODEL_NAME != MODEL_NAME:
        models_to_try.append(FALLBACK_MODEL_NAME)
    if LAST_RESORT_MODEL_NAME not in models_to_try:
        models_to_try.append(LAST_RESORT_MODEL_NAME)

    for model_name in models_to_try:
        for attempt in range(MAX_RETRIES + 1):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                )
                if not response.text:
                    raise RuntimeError(f"Gemini returned no text using {model_name}.")
                return response.text
            except Exception as error:
                last_error = error
                error_text = str(error).upper()
                is_transient = (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                    or "404" in error_text
                    or "NOT_FOUND" in error_text
                )
                if not is_transient or attempt == MAX_RETRIES:
                    break
                time.sleep(2**attempt)

    return (
        "STATUS: NEEDS REVIEW\n\n"
        "SUMMARY OF DOCUMENTS:\n"
        "- Local analysis could not contact the Gemini service.\n\n"
        "DISCREPANCIES FOUND:\n"
        "- Automatic document comparison was not completed.\n\n"
        "RECOMMENDED ACTION:\n"
        "Retry the reconciliation when the AI service is available. "
        "No document data was sent to the server."
    )