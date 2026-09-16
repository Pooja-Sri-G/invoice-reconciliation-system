import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000/process-invoice/"

st.set_page_config(page_title="Invoice Reconciliation")
st.title("Invoice Reconciliation System")

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown(
    """
    <style>
    .main{
        padding-top: 1rem;
    }
    
    .title-header{
    font-weight: bold;
    color: #4CAF50;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid #4CAF50;
    }

    .upload-card{
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        text-align: center;
        padding: 1rem;
    }

    .stButton > button{
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
def show_history():
    st.sidebar.header("History")

    if not st.session_state.history:
        st.sidebar.caption("No previous results yet.")
        return

    for item in reversed(st.session_state.history):
        with st.sidebar.expander(item["time"]):
            st.write(f"PO: {item['po_file']}")
            st.write(f"Goods receipt: {item['gr_file']}")
            st.write(f"Invoice: {item['invoice_file']}")
            st.json(item["result"])

    if st.sidebar.button("Clear history"):
        st.session_state.history = []
        st.rerun()


def submit_files(po_file, gr_file, invoice_file):
    files = {
        "po_file": (po_file.name, po_file.getvalue(), "application/pdf"),
        "gr_file": (gr_file.name, gr_file.getvalue(), "application/pdf"),
        "invoice_file": (invoice_file.name, invoice_file.getvalue(), "application/pdf"),
    }

    try:
        response = requests.post(API_URL, files=files, timeout=60)
        response.raise_for_status()
    except requests.RequestException as error:
        st.error(f"Could not connect to the FastAPI server: {error}")
        return

    result = response.json()
    st.session_state.history.append(
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "po_file": po_file.name,
            "gr_file": gr_file.name,
            "invoice_file": invoice_file.name,
            "result": result,
        }
    )
    st.success("Files submitted successfully.")
    st.json(result)


show_history()

purchase_order = st.file_uploader("Upload Purchase Order", type="pdf")
goods_receipt = st.file_uploader("Upload Goods Receipt", type="pdf")
invoice = st.file_uploader("Upload Invoice", type="pdf")

submitted = st.button("Submit")
if submitted:
    if purchase_order and goods_receipt and invoice:
        submit_files(purchase_order, goods_receipt, invoice)
    else:
        st.warning("Please upload all three PDF files.")
    