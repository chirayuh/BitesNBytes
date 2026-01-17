import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase only if not already initialized
try:
    app = firebase_admin.get_app()
except ValueError:
    firebase_creds = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.set_page_config(page_title="Expense Records", page_icon="💸")
st.header("Expense Records")

# Query BitsNBytes collection for Expense records
expense_docs = db.collection("BitsNBytes").where("Category", "==", "Expense").stream()
expense_records = []
for doc in expense_docs:
    data = doc.to_dict()
    expense_records.append(data)

if expense_records:
    st.dataframe(expense_records)
    # Calculate total expense
    total_expense = sum(float(rec.get("Amount", 0)) for rec in expense_records)
    st.markdown("---")
    st.markdown(f"<h4 style='text-align:right;'>Total Expense:₹ <span style='color:#c0392b;'>{total_expense}</span></h4>", unsafe_allow_html=True)
else:
    st.info("No expense records found.")
