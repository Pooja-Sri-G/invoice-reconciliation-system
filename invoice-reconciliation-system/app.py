import os

import streamlit as st

import requests

from federated_learning import build_local_update
from vision_llm import analyze_documents

FEDERATED_API_URL = "http://127.0.0.1:8001"
CLIENT_ID = os.getenv("FEDERATED_CLIENT_ID", "streamlit-client")

st.set_page_config(page_title="Invoice Reconciliation")

st.title("Invoice Reconciliation System")
st.write("Upload the PO, Goods Received Note, and Invoice as PDF files.")

purchase_order = st.file_uploader("Upload Purchase Order", type=["pdf"])

goods_receipt = st.file_uploader("Upload Goods Received Note", type=["pdf"])

invoice = st.file_uploader("Upload Invoice", type=["pdf"])


if st.button("Submit"):
    if not purchase_order or not goods_receipt or not invoice:
        st.warning("Please upload all three PDF files.")

    else:
        try:
            with st.spinner("Reading the documents..."):
                result = analyze_documents(
                    purchase_order.name,
                    purchase_order.getvalue(),
                    goods_receipt.name,
                    goods_receipt.getvalue(),
                    invoice.name,
                    invoice.getvalue(),
                )

            st.success("Reconciliation completed.")
            st.subheader("Result")
            st.write(result)

            update = build_local_update(result, client_id=CLIENT_ID)
            response = requests.post(
                f"{FEDERATED_API_URL}/federated/update",
                json=update.model_dump(),
                timeout=15,
            )
            response.raise_for_status()
            st.caption("A privacy-safe numeric update was submitted to the coordinator.")

        except requests.RequestException as error:
            st.error(f"Could not connect to FastAPI: {error}")
        except RuntimeError as error:
            st.warning(str(error))
        except Exception as error:
            st.error(f"Could not process the documents locally: {error}")