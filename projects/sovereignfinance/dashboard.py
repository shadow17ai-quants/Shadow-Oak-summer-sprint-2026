# projects/sovereignfinance/dashboard.py
# SovereignFinance – Streamlit Web Dashboard

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page config – brand it with the name
st.set_page_config(
    page_title="SovereignFinance",
    page_icon="🏛️",
    layout="wide"
)

# Database path – relative to the repo root
DB_PATH = "projects/sovereignfinance/finance.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def load_transactions():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM transactions ORDER BY date DESC", conn)
    conn.close()
    return df

def add_transaction(category, amount, date, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (category, amount, date, description)
        VALUES (?, ?, ?, ?)
    """, (category, amount, date, description))
    conn.commit()
    conn.close()

# Sidebar navigation
st.sidebar.title("🏛️ SovereignFinance")
st.sidebar.caption("Shadow Oak Capitals – S1-P1")
page = st.sidebar.radio("Navigate", ["Summary", "All Transactions", "Charts", "Add Transaction"])

# Load data
df = load_transactions()

if page == "Summary":
    st.title("📊 Dashboard Summary")
    col1, col2, col3, col4 = st.columns(4)
    total_income = df[df['amount'] > 0]['amount'].sum() if not df.empty else 0
    total_expense = abs(df[df['amount'] < 0]['amount'].sum()) if not df.empty else 0
    net_balance = total_income - total_expense
    count = len(df)

    col1.metric("Total Income", f"₹{total_income:,.2f}")
    col2.metric("Total Expense", f"₹{total_expense:,.2f}")
    col3.metric("Net Balance", f"₹{net_balance:,.2f}", delta=net_balance)
    col4.metric("Transactions", count)

    st.subheader("Recent Transactions")
    st.dataframe(df.head(10), use_container_width=True)

elif page == "All Transactions":
    st.title("📋 All Transactions")
    search = st.text_input("Search by category or description")
    if search:
        mask = df['category'].str.contains(search, case=False) | df['description'].str.contains(search, case=False)
        filtered = df[mask]
    else:
        filtered = df
    st.dataframe(filtered, use_container_width=True)

elif page == "Charts":
    st.title("📈 Visualizations")
    if df.empty:
        st.warning("No data to display. Add some transactions first.")
    else:
        cat_agg = df.groupby('category')['amount'].sum().reset_index()
        fig1 = px.bar(cat_agg, x='category', y='amount', color='amount',
                      title='Income/Expense by Category',
                      labels={'amount': 'Amount (₹)'},
                      color_continuous_scale=['red', 'green'])
        st.plotly_chart(fig1, use_container_width=True)

        df_sorted = df.sort_values('date')
        df_sorted['cumulative'] = df_sorted['amount'].cumsum()
        fig2 = px.line(df_sorted, x='date', y='cumulative',
                       title='Cumulative Balance Over Time',
                       labels={'cumulative': 'Balance (₹)', 'date': 'Date'})
        st.plotly_chart(fig2, use_container_width=True)

elif page == "Add Transaction":
    st.title("✏️ Add New Transaction")
    with st.form("add_form"):
        category = st.text_input("Category (e.g., Salary, Rent, Food)")
        amount = st.number_input("Amount (₹)", min_value=0.01, step=100.0)
        txn_type = st.radio("Type", ["Income", "Expense"])
        date = st.date_input("Date", datetime.today())
        description = st.text_area("Description (optional)")

        submitted = st.form_submit_button("Add Transaction")
        if submitted:
            if not category:
                st.error("Category is required.")
            else:
                final_amount = amount if txn_type == "Income" else -amount
                add_transaction(category, final_amount, date.strftime("%Y-%m-%d"), description)
                st.success("✅ Transaction added successfully!")
                st.rerun()
                