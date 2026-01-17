import pandas as pd
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import matplotlib.pyplot as plt

# Initialize Firebase only if not already initialized
try:
	app = firebase_admin.get_app()
except ValueError:
	firebase_creds = st.secrets["firebase"]
	cred = credentials.Certificate(firebase_creds)
	firebase_admin.initialize_app(cred)
db = firestore.client()

st.set_page_config(page_title="Stats", page_icon="📊")
st.header("Income & Expense Statistics")

# Fetch Income records
income_docs = db.collection("BitsNBytes").where("Category", "==", "Income").stream()
income_records = [doc.to_dict() for doc in income_docs]
total_income = sum(float(rec.get("Amount", 0)) for rec in income_records)

# Fetch Expense records
expense_docs = db.collection("BitsNBytes").where("Category", "==", "Expense").stream()
expense_records = [doc.to_dict() for doc in expense_docs]
total_expense = sum(float(rec.get("Amount", 0)) for rec in expense_records)

# Calculate net balance
net_balance = total_income - total_expense



# Conditional color for Net Balance
net_color = "#27ae60" if net_balance >= 0 else "#e67e22"
st.markdown(f"""
<div style='display: flex; justify-content: space-between;'>
    <div style='flex:1; text-align:center;'>
        <span style='color:#27ae60; font-size:1.2em; font-weight:bold;'>Total Income</span><br>
        <span style='color:#27ae60; font-size:1.5em;'>₹ {total_income}</span>
    </div>
    <div style='flex:1; text-align:center;'>
        <span style='color:#c0392b; font-size:1.2em; font-weight:bold;'>Total Expense</span><br>
        <span style='color:#c0392b; font-size:1.5em;'>₹ {total_expense}</span>
    </div>
    <div style='flex:1; text-align:center;'>
        <span style='color:{net_color}; font-size:1.2em; font-weight:bold;'>Net Balance</span><br>
        <span style='color:{net_color}; font-size:1.5em;'>₹ {net_balance}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.subheader("Income Records")

if income_records:
	st.dataframe(income_records)
else:
	st.info("No income records found.")

st.subheader("Expense Records")

if expense_records:
	st.dataframe(expense_records)
else:
	st.info("No expense records found.")

# --- Analytics Section ---
st.markdown("---")
st.subheader("Analytics")

# Combine income and expense records for analytics
all_records = []
for rec in income_records:
	rec_copy = rec.copy()
	rec_copy["Type"] = "Income"
	all_records.append(rec_copy)
for rec in expense_records:
	rec_copy = rec.copy()
	rec_copy["Type"] = "Expense"
	all_records.append(rec_copy)

if all_records:
    df = pd.DataFrame(all_records)
    # Segregated Expense Table by Description
    st.write("### Segregated Expense Table (by Description)")
    expense_df = df[df["Type"] == "Expense"].copy()
    def expense_type(desc):
        # handle None and normalize
        desc = (str(desc) if desc is not None else "").lower()
        # container detection (explicit)
        if "container" in desc or "containers" in desc or "box" in desc:
            return "Container"
        # OTG
        if "otg" in desc:
            return "OTG"
        # ingredient-specific categories (priority after container/otg)
        if "sugar" in desc:
            return "Sugar"
        if "atta" in desc or "aata" in desc:
            return "Atta"
        if "maida" in desc:
            return "Maida"
        if "oil" in desc:
            return "Oil"
        if "walnut" in desc or "walnuts" in desc:
            return "Walnut"
        if "banana" in desc or "bananas" in desc:
            return "Banana"
        # default to Material
        return "Material"
    expense_df["ExpenseType"] = expense_df["Description"].apply(expense_type)
    segregated = expense_df.groupby("ExpenseType")["Amount"].sum().reset_index()
    st.dataframe(segregated)
    # Pie chart for Segregated Expense Table (by Description)
    st.write("### Segregated Expense Pie Chart")
    if not segregated.empty:
        # sort for consistent ordering
        segregated = segregated.sort_values("Amount", ascending=False)
        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(
            segregated["Amount"],
            labels=None,  # use legend for labels to avoid overlap
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.75,
            textprops={"fontsize": 10},
        )
        ax.set_title("Segregated Expenses by Description")
        # external legend to avoid label overlap
        ax.legend(wedges, segregated["ExpenseType"], title="Expense Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        ax.axis("equal")
        plt.tight_layout()
        st.pyplot(fig)
    
    # Parse date and group by month
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Month"] = df["Date"].dt.strftime("%B %Y")
        monthly_summary = df.groupby(["Month", "Type"])["Amount"].sum().unstack(fill_value=0).reset_index()
        st.write("### Monthly Income/Expense Summary")
        st.dataframe(monthly_summary)
        st.write("### Monthly Income vs Expense Bar Chart")
        #st.bar_chart(monthly_summary.set_index("Month"))

        # Pie chart for category distribution
        st.write("### Category Distribution Pie Chart")
        if "Category" in df.columns:
            # Use both income and expense categories for pie chart
            cat_sum = df.groupby(["Category"])["Amount"].sum()
            if not cat_sum.empty:
                fig, ax = plt.subplots(figsize=(6, 6))
                wedges, texts, autotexts = ax.pie(
                    cat_sum,
                    labels=None,
                    autopct='%1.1f%%',
                    startangle=90,
                    pctdistance=0.75,
                    textprops={"fontsize": 10},
                )
                ax.set_title("Category Distribution (Income & Expense)")
                ax.legend(wedges, cat_sum.index, title="Category", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
                ax.axis("equal")
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("No category data available for pie chart.")

        # Cumulative balance over time
        st.write("### Cumulative Net Balance Over Time")
        df_sorted = df.sort_values("Date")
        df_sorted["Income"] = df_sorted.apply(lambda x: x["Amount"] if x["Type"] == "Income" else 0, axis=1)
        df_sorted["Expense"] = df_sorted.apply(lambda x: x["Amount"] if x["Type"] == "Expense" else 0, axis=1)
        df_sorted["Net"] = df_sorted["Income"] - df_sorted["Expense"]
        df_sorted["CumulativeNet"] = df_sorted["Net"].cumsum()
        # Ensure index is datetime or string
        df_sorted["Date_str"] = df_sorted["Date"].dt.strftime('%Y-%m-%d')
        st.line_chart(df_sorted.set_index("Date_str")["CumulativeNet"])

        # Top Segregated Expense Categories
        st.write("### Top Segregated Expense Categories (by Description)")
        if "ExpenseType" in expense_df.columns:
            segregated_cats = expense_df.groupby("ExpenseType")["Amount"].sum().sort_values(ascending=False)
            segregated_cats.index = segregated_cats.index.astype(str)
            st.bar_chart(segregated_cats)
        else:
            st.info("No valid segregated expense data for analytics.")
    else:
        st.info("No valid date data for analytics.")
