"""
Streamlit dashboard for SovereignFinance.
Violet fintech-SaaS styled interface for managing personal finances.
"""

import logging
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from sovfin.config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    CHART_COLORS,
    DISPLAY_DATE_FORMAT,
    LOG_FORMAT,
    LOG_LEVEL,
    MAX_AMOUNT_LIMIT,
    MAX_CATEGORY_LENGTH,
    MAX_DESCRIPTION_LENGTH,
)
from sovfin.database import db

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)
logger.info(f"{APP_NAME} dashboard v{APP_VERSION} starting up")

st.set_page_config(
    page_title=f"{APP_NAME}",
    page_icon=":gem:",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    db.initialize_schema()
    logger.info("Database initialized successfully for dashboard")
except Exception as e:
    logger.critical(f"Failed to initialize database: {e}")
    st.error(f"Database initialization failed: {e}")
    st.stop()

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(circle at 15% 0%, #241f3d 0%, #15121f 45%, #0f0d18 100%);
    color: #f1eefc;
}

[data-testid="stSidebar"] {
    background: #17142a;
    border-right: 1px solid #2a2645;
}
[data-testid="stSidebar"] * { color: #cfc9ea !important; }

div[role="radiogroup"] label {
    background: #1f1b36;
    border: 1px solid #2a2645;
    border-radius: 10px;
    padding: 8px 14px;
    margin-bottom: 6px;
    width: 100%;
}
div[role="radiogroup"] label:hover { border-color: #8b5cf6; }

h1, h2, h3 { font-weight: 800; letter-spacing: -0.02em; color: #ffffff; }

.term-caption {
    color: #8b87a8;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
    margin-bottom: 1.2rem;
}

.metric-card {
    background: linear-gradient(160deg, #241f3d 0%, #181530 100%);
    border: 1px solid #2a2645;
    border-radius: 18px;
    padding: 20px 22px;
    height: 100%;
    box-shadow: 0 8px 24px rgba(139,92,246,0.08);
}

.metric-label {
    color: #8b87a8;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
}
.metric-value.positive { color: #34d399; }
.metric-value.negative { color: #fb7185; }
.metric-value.neutral  { color: #c4b5fd; }

.pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    padding: 3px 10px;
    border-radius: 999px;
    font-weight: 600;
}
.pill.income  { background: rgba(52,211,153,0.15); color: #34d399; }
.pill.expense { background: rgba(251,113,133,0.15); color: #fb7185; }

.row-card {
    background: #1c1832;
    border: 1px solid #2a2645;
    border-radius: 14px;
    padding: 12px 16px;
    margin-bottom: 8px;
}

hr.term-divider { border: none; border-top: 1px solid #2a2645; margin: 1.5rem 0; }

[data-testid="stDataFrame"] { border: 1px solid #2a2645; border-radius: 12px; }

.stButton>button {
    background: linear-gradient(135deg, #8b5cf6, #c084fc);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}
.stButton>button:hover { opacity: 0.9; }

[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; }
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)

PLOTLY_DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cfc9ea", family="Inter"),
    xaxis=dict(gridcolor="#2a2645", zerolinecolor="#2a2645"),
    yaxis=dict(gridcolor="#2a2645", zerolinecolor="#2a2645"),
)

VIOLET_SCALE = ["#fb7185", "#8b5cf6", "#34d399"]


def metric_card(label: str, value: str, tone: str = "neutral") -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {tone}">{value}</div>
    </div>
    """


def main() -> None:
    with st.sidebar:
        st.markdown(f"### {APP_NAME}")
        st.markdown(f'<div class="term-caption">{APP_DESCRIPTION} · v{APP_VERSION}</div>', unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio(
            "Navigate",
            ["Summary", "Transactions", "Charts", "Add Transaction", "Manage"],
            label_visibility="collapsed",
        )

    if page == "Summary":
        show_summary_page()
    elif page == "Transactions":
        show_transactions_page()
    elif page == "Charts":
        show_charts_page()
    elif page == "Add Transaction":
        show_add_transaction_page()
    elif page == "Manage":
        show_manage_page()


def show_summary_page() -> None:
    st.title("Dashboard")
    st.markdown('<div class="term-caption">Manage your transactions and financial goals</div>', unsafe_allow_html=True)

    transactions = db.get_all_transactions()
    if not transactions:
        st.info("No transactions recorded yet. Add a transaction to see your summary.")
        return

    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"])
    df["date_dt"] = pd.to_datetime(df["date"])

    total_income = df[df["amount"] > 0]["amount"].sum()
    total_expense = abs(df[df["amount"] < 0]["amount"].sum())
    net_balance = total_income - total_expense
    transaction_count = len(df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card("Total Balance", f"₹{net_balance:,.2f}", "positive" if net_balance >= 0 else "negative"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Total Income", f"₹{total_income:,.2f}", "positive"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Total Expense", f"₹{total_expense:,.2f}", "negative"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("Transactions", f"{transaction_count}", "neutral"), unsafe_allow_html=True)

    st.markdown('<hr class="term-divider">', unsafe_allow_html=True)

    left, right = st.columns([2, 1])

    with left:
        st.markdown("##### Transactions Overview")
        df_sorted = df.sort_values("date_dt")
        df_sorted["cumulative_balance"] = df_sorted["amount"].cumsum()
        fig = px.area(df_sorted, x="date_dt", y="cumulative_balance")
        fig.update_traces(line=dict(color="#8b5cf6", width=2), fillcolor="rgba(139,92,246,0.15)")
        fig.update_layout(**PLOTLY_DARK_LAYOUT, height=340, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("##### All Expenses")
        expense_df = df[df["amount"] < 0].copy()
        if not expense_df.empty:
            expense_df["amount"] = expense_df["amount"].abs()
            cat_totals = expense_df.groupby("category")["amount"].sum().reset_index()
            fig2 = px.pie(cat_totals, names="category", values="amount", hole=0.65,
                          color_discrete_sequence=["#8b5cf6", "#c084fc", "#fb7185", "#34d399", "#60a5fa"])
            fig2.update_layout(**PLOTLY_DARK_LAYOUT, height=340, showlegend=True,
                                legend=dict(orientation="h", y=-0.15))
            fig2.update_traces(textinfo="none")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No expenses yet.")

    st.markdown('<hr class="term-divider">', unsafe_allow_html=True)
    st.markdown("##### Recent Activity")
    recent = df.sort_values("date_dt", ascending=False).head(5)
    for _, row in recent.iterrows():
        pill_class = "income" if row["amount"] > 0 else "expense"
        pill_label = "INCOME" if row["amount"] > 0 else "EXPENSE"
        st.markdown(
            f'<div class="row-card"><span class="pill {pill_class}">{pill_label}</span>&nbsp;&nbsp;'
            f'<b>{row["category"]}</b> — ₹{abs(row["amount"]):,.2f} · '
            f'{row["date_dt"].strftime(DISPLAY_DATE_FORMAT)}</div>',
            unsafe_allow_html=True,
        )


def show_transactions_page() -> None:
    st.title("All Transactions")
    st.markdown('<div class="term-caption">Browse, search, and filter your transaction history</div>', unsafe_allow_html=True)

    transactions = db.get_all_transactions()
    if not transactions:
        st.info("No transactions recorded yet.")
        return

    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"])
    df["date_dt"] = pd.to_datetime(df["date"])

    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("Search by category or description", placeholder="Enter search term...")
    with col2:
        transaction_type = st.selectbox("Filter by type", ["All", "Income Only", "Expense Only"], index=0)

    filtered_df = df.copy()
    if search_term:
        mask = (
            filtered_df["category"].str.contains(search_term, case=False, na=False)
            | filtered_df["description"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    if transaction_type == "Income Only":
        filtered_df = filtered_df[filtered_df["amount"] > 0]
    elif transaction_type == "Expense Only":
        filtered_df = filtered_df[filtered_df["amount"] < 0]

    filtered_df = filtered_df.sort_values("date_dt", ascending=False)

    if filtered_df.empty:
        st.warning("No transactions match your search criteria.")
        return

    st.markdown(f'<div class="term-caption">Showing {len(filtered_df)} of {len(df)} transactions</div>', unsafe_allow_html=True)

    display_df = filtered_df.copy()
    display_df["amount_formatted"] = display_df["amount"].apply(lambda x: f"₹{x:,.2f}")
    display_df["date_formatted"] = display_df["date_dt"].dt.strftime(DISPLAY_DATE_FORMAT)
    display_df["type"] = display_df["amount"].apply(lambda x: "Income" if x > 0 else "Expense")
    display_df = display_df[["id", "category", "type", "amount_formatted", "date_formatted", "description"]]
    display_df.columns = ["ID", "Category", "Type", "Amount", "Date", "Description"]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown('<hr class="term-divider">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(metric_card("Filtered Income", f"₹{filtered_df[filtered_df['amount'] > 0]['amount'].sum():,.2f}", "positive"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Filtered Expense", f"₹{abs(filtered_df[filtered_df['amount'] < 0]['amount'].sum()):,.2f}", "negative"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Filtered Count", f"{len(filtered_df)}", "neutral"), unsafe_allow_html=True)


def show_charts_page() -> None:
    st.title("Financial Charts")
    st.markdown('<div class="term-caption">Visualize income, expenses, and trends</div>', unsafe_allow_html=True)

    transactions = db.get_all_transactions()
    if not transactions:
        st.info("No data available for charts. Add some transactions first.")
        return

    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"])
    df["date_dt"] = pd.to_datetime(df["date"])

    tab1, tab2, tab3 = st.tabs(["By Category", "Cumulative Balance", "Monthly Trends"])
    with tab1:
        show_category_chart(df)
    with tab2:
        show_cumulative_chart(df)
    with tab3:
        show_monthly_trends_chart(df)


def show_category_chart(df: pd.DataFrame) -> None:
    st.subheader("Income / Expense by Category")
    category_totals = df.groupby("category")["amount"].sum().reset_index()
    category_totals = category_totals.sort_values("amount", key=abs, ascending=False)

    fig = px.bar(
        category_totals, x="category", y="amount",
        labels={"amount": "Amount (₹)", "category": "Category"},
        color="amount",
        color_continuous_scale=[[0, "#fb7185"], [0.5, "#2a2645"], [1, "#8b5cf6"]],
        text="amount",
    )
    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    fig.update_layout(**PLOTLY_DARK_LAYOUT, xaxis_tickangle=-45, showlegend=False, height=500)
    fig.add_hline(y=0, line_dash="dash", line_color="#3a3660")
    st.plotly_chart(fig, use_container_width=True)


def show_cumulative_chart(df: pd.DataFrame) -> None:
    st.subheader("Cumulative Balance Over Time")
    df_sorted = df.sort_values("date_dt")
    df_sorted["cumulative_balance"] = df_sorted["amount"].cumsum()

    fig = px.area(df_sorted, x="date_dt", y="cumulative_balance",
                  labels={"cumulative_balance": "Balance (₹)", "date_dt": "Date"})
    fig.update_traces(line=dict(color="#8b5cf6", width=2), fillcolor="rgba(139,92,246,0.15)")
    fig.update_layout(**PLOTLY_DARK_LAYOUT, xaxis_tickangle=-45, hovermode="x unified")
    fig.add_hline(y=0, line_dash="dash", line_color="#3a3660")
    st.plotly_chart(fig, use_container_width=True)


def show_monthly_trends_chart(df: pd.DataFrame) -> None:
    st.subheader("Monthly Income vs Expense")
    df_temp = df.copy()
    df_temp["date_dt"] = pd.to_datetime(df_temp["date"])
    df_temp = df_temp.set_index("date_dt")

    monthly_data = df_temp.resample("ME").agg({"amount": "sum"}).reset_index()
    monthly_data["income"] = monthly_data["amount"].clip(lower=0)
    monthly_data["expense"] = monthly_data["amount"].clip(upper=0).abs()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly_data["date_dt"], y=monthly_data["income"], name="Income", marker_color="#34d399"))
    fig.add_trace(go.Bar(x=monthly_data["date_dt"], y=monthly_data["expense"], name="Expense", marker_color="#fb7185"))
    fig.update_layout(**PLOTLY_DARK_LAYOUT, xaxis_title="Month", yaxis_title="Amount (₹)", barmode="group", xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


def show_add_transaction_page() -> None:
    st.title("Add New Transaction")
    st.markdown('<div class="term-caption">Record a new income or expense</div>', unsafe_allow_html=True)

    with st.form("add_transaction_form"):
        category = st.text_input("Category (e.g., Salary, Rent, Food)")
        amount = st.number_input("Amount (₹)", min_value=0.01, step=100.0)
        txn_type = st.radio("Transaction Type", ["Income", "Expense"], horizontal=True)
        date = st.date_input("Date", value=datetime.today())
        description = st.text_area("Description (optional)")

        submitted = st.form_submit_button("Add Transaction", use_container_width=True)
        if submitted:
            errors = []
            if not category:
                errors.append("Category is required.")
            elif len(category) > MAX_CATEGORY_LENGTH:
                errors.append(f"Category must be under {MAX_CATEGORY_LENGTH} characters.")
            if amount <= 0 or amount > MAX_AMOUNT_LIMIT:
                errors.append(f"Amount must be between 0 and {MAX_AMOUNT_LIMIT:,.0f}.")
            if description and len(description) > MAX_DESCRIPTION_LENGTH:
                errors.append(f"Description must be under {MAX_DESCRIPTION_LENGTH} characters.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                signed_amount = amount if txn_type == "Income" else -amount
                try:
                    db.add_transaction(category=category, amount=signed_amount,
                                        date=date.strftime("%Y-%m-%d"), description=description)
                    st.success("Transaction added successfully.")
                    logger.info(f"Transaction added: {category} ₹{signed_amount}")
                    st.rerun()
                except Exception as e:
                    logger.error(f"Failed to add transaction: {e}")
                    st.error(f"Failed to add transaction: {e}")


def show_manage_page() -> None:
    st.title("Manage Transactions")
    st.markdown('<div class="term-caption">Edit or delete existing transactions</div>', unsafe_allow_html=True)

    transactions = db.get_all_transactions()
    if not transactions:
        st.info("No transactions to manage. Add a transaction first.")
        return

    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"])
    df["date_dt"] = pd.to_datetime(df["date"])

    txn_ids = df["id"].tolist()
    selected_id = st.selectbox(
        "Select Transaction ID to Edit or Delete", txn_ids,
        format_func=lambda x: (
            f"ID {x} — {df[df['id']==x]['category'].iloc[0]}: "
            f"₹{df[df['id']==x]['amount'].iloc[0]:,.2f} on {df[df['id']==x]['date'].iloc[0]}"
        ),
    )

    row = df[df["id"] == selected_id].iloc[0]

    st.markdown("**Current Details**")
    st.write(f"Category: {row['category']}")
    st.write(f"Amount: ₹{row['amount']:,.2f}")
    st.write(f"Date: {row['date']}")
    st.write(f"Description: {row['description'] or 'No description'}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete this Transaction", use_container_width=True, type="secondary"):
            try:
                success = db.delete_transaction(selected_id)
                if success:
                    st.success("Transaction deleted.")
                    logger.info(f"Transaction {selected_id} deleted")
                    st.rerun()
                else:
                    st.warning("Transaction not found or already deleted.")
            except Exception as e:
                logger.error(f"Failed to delete transaction: {e}")
                st.error(f"Failed to delete transaction: {e}")

    with col2:
        with st.expander("Edit this Transaction", expanded=False):
            with st.form("edit_transaction_form"):
                edit_category = st.text_input("Category", value=row["category"])
                edit_amount = st.number_input("Amount (₹)", value=abs(row["amount"]), min_value=0.01, step=100.0)
                edit_type = st.radio("Transaction Type", ["Income", "Expense"],
                                      index=0 if row["amount"] > 0 else 1, horizontal=True)
                edit_date = st.date_input("Date", value=pd.to_datetime(row["date"]))
                edit_description = st.text_area("Description (optional)",
                                                 value=row["description"] if row["description"] else "")

                edit_submitted = st.form_submit_button("Update Transaction", use_container_width=True)
                if edit_submitted:
                    errors = []
                    if not edit_category:
                        errors.append("Category is required.")
                    elif len(edit_category) > MAX_CATEGORY_LENGTH:
                        errors.append(f"Category must be under {MAX_CATEGORY_LENGTH} characters.")
                    if edit_amount <= 0 or edit_amount > MAX_AMOUNT_LIMIT:
                        errors.append(f"Amount must be between 0 and {MAX_AMOUNT_LIMIT:,.0f}.")

                    if errors:
                        for err in errors:
                            st.error(err)
                    else:
                        signed_amount = edit_amount if edit_type == "Income" else -edit_amount
                        try:
                            success = db.update_transaction(
                                transaction_id=selected_id, category=edit_category,
                                amount=signed_amount, date=edit_date.strftime("%Y-%m-%d"),
                                description=edit_description,
                            )
                            if success:
                                st.success("Transaction updated.")
                                logger.info(f"Transaction {selected_id} updated")
                                st.rerun()
                            else:
                                st.error("Transaction not found or update failed.")
                        except Exception as e:
                            logger.error(f"Failed to update transaction: {e}")
                            st.error(f"Failed to update transaction: {e}")


if __name__ == "__main__":
    main()
else:
    main()