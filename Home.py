# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

# Load Firebase credentials from Streamlit secrets
if not firebase_admin._apps:
    firebase_creds = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


def run():
    st.set_page_config(
        page_title="Bites & Bytes",
        page_icon="🍰",
    )

    st.markdown("""
    <h1 style='text-align: center; color: #ff4b4b;'>Bites & Bytes 🍰</h1>
    <hr style='border:1px solid #ff4b4b;'>
    """, unsafe_allow_html=True)

    with st.container():
        st.subheader("Add Income/Expense Record")
        col1, col2 = st.columns([2, 1])
        with col1:
            dateOfCategory = st.date_input("Date Of Income/Expense", value=None)
            Amount = st.number_input("Amount", min_value=0, help="Enter the amount for income or expense.")
            category = st.radio(
                "Category",
                ["Income", "Expense"],
                index=0,
                help="Select whether this is an income or expense."
            )
            Description = st.text_area("Description", help="Add details about this entry.")
        with col2:
            st.image("images/Sticker_Banana_walnut_cake.png", width=120)
            st.markdown("<div style='text-align:center;'>🍌🍰</div>", unsafe_allow_html=True)

    st.write(f"**Date:** {dateOfCategory}")
    st.write(f"**Amount:** {Amount}")
    st.write(f"**Category:** {category}")
    st.write(f"**Description:** {Description}")

    if st.button("Add Expense/Income"):
        st.success(f"{category} Successfully Added")
        date_str = dateOfCategory.isoformat() if isinstance(dateOfCategory, datetime.date) else ""
        record = {
            "Date": date_str,
            "Amount": Amount,
            "Category": category,
            "Description": Description
        }
        doc_ref = db.collection("BitsNBytes").document()
        doc_ref.set(record)

    st.markdown("---")
    st.info("Use the sidebar to view your income and expense records.")

if __name__ == "__main__":
    run()
