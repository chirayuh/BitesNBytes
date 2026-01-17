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
import inspect
import textwrap
import time
import numpy as np
import re
from utils import show_code
# Firestore fetch logic
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase if not already
if not firebase_admin._apps:
    cred = credentials.Certificate("bitesbytes-f2302-e345b2788029.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.header("Income Records")
# Query BitsNBytes collection for Income records
docs = db.collection("BitsNBytes").where("Category", "==", "Income").stream()
income_records = []
for doc in docs:
    data = doc.to_dict()
    income_records.append(data)

if income_records:
    st.dataframe(income_records)
    # Calculate total income
    total_income = sum(float(rec.get("Amount", 0)) for rec in income_records)
    
    # Count total PCs sold from description
    pcs_sold = 0
    for rec in income_records:
        description = rec.get("Description", "").lower()
        if "pc" in description:
            pcs_sold += 1
    
    # Count Wheat and Mix quantities from description
    wheat_count = 0
    mix_count = 0
    for rec in income_records:
        description = rec.get("Description", "").lower()
        
        # Extract wheat quantity (e.g., "wheat - 6pc" → 6)
        wheat_match = re.search(r'wheat\s*-?\s*(\d+)\s*pc', description)
        if wheat_match:
            wheat_count += int(wheat_match.group(1))
        
        # Extract mix quantity (e.g., "mix - 6pc" → 6)
        mix_match = re.search(r'mix\s*-?\s*(\d+)\s*pc', description)
        if mix_match:
            mix_count += int(mix_match.group(1))
    
    total_wheat_mix = wheat_count + mix_count
    
    st.markdown("---")
    st.markdown(f"<h4 style='text-align:right;'>Total Income:₹ <span style='color:#27ae60;'>{total_income}</span></h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align:right;'>Total Wheat: <span style='color:#e67e22;'>{wheat_count}</span></h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align:right;'>Total Mix: <span style='color:#9b59b6;'>{mix_count}</span></h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align:right;'>Total PCs Sold: <span style='color:#1abc9c;'>{total_wheat_mix}</span></h4>", unsafe_allow_html=True)
else:
    st.info("No income records found.")

