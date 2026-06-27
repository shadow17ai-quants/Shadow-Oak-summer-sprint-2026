# projects/sovereignfinance/dashboard.py
# SovereignFinance – Streamlit Web Dashboard with full CRUD

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="SovereignFinance", page_icon="🏛️", layout="wide")

DB_PATH = "finance.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

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

def delete_transaction(txn_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
    conn.commit()
    conn.close()

def update_transaction(txn_id, category, amount, date, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions
        SET category = ?, amount = ?, date = ?, description = ?
        WHERE id = ?
    """, (category, amount, date, description, txn_id))
    conn.commit()
    conn.close()

# Ensure table exists
create_table()
df = load_transactions()

# Sidebar
st.sidebar.title("🏛️ SovereignFinance")
st.sidebar.caption("Shadow Oak Capitals – S1-P1")
page = st.sidebar.radio("Navigate", ["Summary", "All Transactions", "Charts", "Add Transaction", "Manage"])

# ---- SUMMARY ----
if page == "Summary":
    st.title("📊 Dashboard Summary")
    total_income = df[df['amount'] > 0]['amount'].sum() if not df.empty else 0
    total_expense = abs(df[df['amount'] < 0]['amount'].sum()) if not df.empty else 0
    net_balance = total_income - total_expense
    count = len(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Income", f"₹{total_income:,.2f}")
    col2.metric("Total Expense", f"₹{total_expense:,.2f}")
    col3.metric("Net Balance", f"₹{net_balance:,.2f}", delta=net_balance)
    col4.metric("Transactions", count)

    st.subheader("Recent Transactions")
    st.dataframe(df.head(10), use_container_width=True)

# ---- ALL TRANSACTIONS ----
elif page == "All Transactions":
    st.title("📋 All Transactions")
    search = st.text_input("Search by category or description")
    if search:
        mask = df['category'].str.contains(search, case=False) | df['description'].str.contains(search, case=False)
        filtered = df[mask]
    else:
        filtered = df
    st.dataframe(filtered, use_container_width=True)

# ---- CHARTS ----
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

# ---- ADD TRANSACTION ----
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

# ---- MANAGE (DELETE / EDIT) ----
elif page == "Manage":
    st.title("🛠️ Manage Transactions")

    if df.empty:
        st.warning("No transactions to manage. Add some first.")
    else:
        # Select transaction to edit/delete
        txn_ids = df['id'].tolist()
        selected_id = st.selectbox("Select Transaction ID to Edit/Delete", txn_ids)

        # Get the row for that ID
        row = df[df['id'] == selected_id].iloc[0]

        # Display current values
        st.write("**Current Details:**")
        st.write(f"**Category:** {row['category']}")
        st.write(f"**Amount:** ₹{row['amount']:,.2f}")
        st.write(f"**Date:** {row['date']}")
        st.write(f"**Description:** {row['description']}")

        col1, col2 = st.columns(2)

        # ---- DELETE ----
        with col1:
            if st.button("🗑️ Delete this Transaction", use_container_width=True):
                delete_transaction(selected_id)
                st.success("✅ Transaction deleted!")
                st.rerun()

        # ---- EDIT ----
        with col2:
            with st.expander("✏️ Edit this Transaction"):
                with st.form("edit_form"):
                    new_category = st.text_input("Category", value=row['category'])
                    new_amount = st.number_input("Amount (₹)", value=abs(row['amount']), min_value=0.01, step=100.0)
                    new_type = st.radio("Type", ["Income", "Expense"], index=0 if row['amount'] > 0 else 1)
                    new_date = st.date_input("Date", value=datetime.strptime(row['date'], "%Y-%m-%d"))
                    new_description = st.text_area("Description", value=row['description'] if row['description'] else "")
                    edit_submitted = st.form_submit_button("Update Transaction")
                    if edit_submitted:
                        if not new_category:
                            st.error("Category is required.")
                        else:
                            final_amount = new_amount if new_type == "Income" else -new_amount
                            update_transaction(selected_id, new_category, final_amount, new_date.strftime("%Y-%m-%d"), new_description)
                            st.success("✅ Transaction updated!")
                            st.rerun()