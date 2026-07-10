"""
Streamlit dashboard for SovereignFinance.
Provides an interactive web interface for managing personal finances.
"""

import logging
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from .config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    CHART_COLORS,
    DISPLAY_DATE_FORMAT,
    LOG_FORMAT,
    LOG_LEVEL,
)
from .database import db
from .validation import ValidationError, validate_transaction_data

# Configure logging
logging.basicConfig(
    level=getattr(__import__("logging"), LOG_LEVEL) if isinstance(LOG_LEVEL, str) else LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

logger.info(f"{APP_NAME} dashboard v{APP_VERSION} starting up")

# Page configuration
st.set_page_config(
    page_title=f"{APP_NAME} - Personal Finance Tracker",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database schema on app startup
try:
    db.initialize_schema()
    logger.info("Database initialized successfully for dashboard")
except Exception as e:
    logger.critical(f"Failed to initialize database: {e}")
    st.error("❌ Failed to initialize database. Please check the logs.")
    st.stop()


def main() -> None:
    """Main dashboard application."""
    # Sidebar
    with st.sidebar:
        st.title(f"🏛️ {APP_NAME}")
        st.caption(f"{APP_DESCRIPTION} v{APP_VERSION}")
        st.divider()

        page = st.radio(
            "Navigate",
            ["📊 Summary", "📋 All Transactions", "📈 Charts", "✏️ Add Transaction", "🛠️ Manage"],
            label_visibility="collapsed"
        )

    # Main content area
    if page == "📊 Summary":
        show_summary_page()
    elif page == "📋 All Transactions":
        show_transactions_page()
    elif page == "📈 Charts":
        show_charts_page()
    elif page == "✏️ Add Transaction":
        show_add_transaction_page()
    elif page == "🛠️ Manage":
        show_manage_page()


def show_summary_page() -> None:
    """Display the summary dashboard page."""
    st.title("📊 Financial Summary")
    st.caption("Overview of your financial situation")

    transactions = db.get_all_transactions()

    if not transactions:
        st.info("📭 No transactions recorded yet. Add some transactions to see your financial summary.")
        return

    # Convert to DataFrame for easier calculations
    df = pd.DataFrame(transactions)
    df['amount'] = pd.to_numeric(df['amount'])

    # Calculate metrics
    total_income = df[df['amount'] > 0]['amount'].sum()
    total_expense = abs(df[df['amount'] < 0]['amount'].sum())
    net_balance = total_income - total_expense
    transaction_count = len(df)

    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Total Income",
            value=f"₹{total_income:,.2f}",
            delta=None
        )

    with col2:
        st.metric(
            label="💸 Total Expense",
            value=f"₹{total_expense:,.2f}",
            delta=None
        )

    with col3:
        delta_color = "normal" if net_balance >= 0 else "inverse"
        st.metric(
            label="💳 Net Balance",
            value=f"₹{net_balance:,.2f}",
            delta=f"₹{net_balance:,.2f}",
            delta_color=delta_color
        )

    with col4:
        st.metric(
            label="📝 Transactions",
            value=f"{transaction_count}",
            delta=None
        )

    st.divider()

    # Recent transactions
    st.subheader("🕒 Recent Transactions")
    recent_df = df.head(10).copy()
    recent_df['amount'] = recent_df['amount'].apply(lambda x: f"₹{x:,.2f}")
    recent_df['date'] = pd.to_datetime(recent_df['date']).dt.strftime(DISPLAY_DATE_FORMAT)
    recent_df = recent_df[['id', 'category', 'amount', 'date', 'description']]
    recent_df.columns = ['ID', 'Category', 'Amount', 'Date', 'Description']

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Category": st.column_config.TextColumn("Category", width="medium"),
            "Amount": st.column_config.TextColumn("Amount", width="medium"),
            "Date": st.column_config.TextColumn("Date", width="small"),
            "Description": st.column_config.TextColumn("Description", width="large"),
        }
    )


def show_transactions_page() -> None:
    """Display all transactions with search and filter capabilities."""
    st.title("📋 All Transactions")
    st.caption("Complete transaction history with search and filtering")

    transactions = db.get_all_transactions()

    if not transactions:
        st.info("📭 No transactions recorded yet. Add some transactions to see them here.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    df['amount'] = pd.to_numeric(df['amount'])
    df['date_dt'] = pd.to_datetime(df['date'])

    # Search and filter controls
    col1, col2 = st.columns([2, 1])

    with col1:
        search_term = st.text_input(
            "🔍 Search by category or description",
            placeholder="Enter search term..."
        )

    with col2:
        # Filter by transaction type
        transaction_type = st.selectbox(
            "Filter by type",
            ["All", "Income Only", "Expense Only"],
            index=0
        )

    # Apply filters
    filtered_df = df.copy()

    if search_term:
        mask = (
            filtered_df['category'].str.contains(search_term, case=False, na=False) |
            filtered_df['description'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    if transaction_type == "Income Only":
        filtered_df = filtered_df[filtered_df['amount'] > 0]
    elif transaction_type == "Expense Only":
        filtered_df = filtered_df[filtered_df['amount'] < 0]

    # Sort by date (newest first)
    filtered_df = filtered_df.sort_values('date_dt', ascending=False)

    if filtered_df.empty:
        st.warning("🔍 No transactions match your search criteria.")
        return

    # Display count
    st.caption(f"Showing {len(filtered_df)} of {len(df)} transactions")

    # Prepare data for display
    display_df = filtered_df.copy()
    display_df['amount_formatted'] = display_df['amount'].apply(lambda x: f"₹{x:,.2f}")
    display_df['date_formatted'] = display_df['date_dt'].dt.strftime(DISPLAY_DATE_FORMAT)
    display_df['type'] = display_df['amount'].apply(lambda x: "Income" if x > 0 else "Expense")
    display_df = display_df[['id', 'category', 'type', 'amount_formatted', 'date_formatted', 'description']]
    display_df.columns = ['ID', 'Category', 'Type', 'Amount', 'Date', 'Description']

    # Configure column display
    column_config = {
        "ID": st.column_config.NumberColumn("ID", width="small"),
        "Category": st.column_config.TextColumn("Category", width="medium"),
        "Type": st.column_config.TextColumn("Type", width="small"),
        "Amount": st.column_config.TextColumn("Amount", width="medium"),
        "Date": st.column_config.TextColumn("Date", width="small"),
        "Description": st.column_config.TextColumn("Description", width="large"),
    }

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config
    )

    # Summary statistics for filtered data
    if len(filtered_df) > 0:
        st.divider()
        col1, col2, col3 = st.columns(3)

        with col1:
            filtered_income = filtered_df[filtered_df['amount'] > 0]['amount'].sum()
            st.metric("Filtered Income", f"₹{filtered_income:,.2f}")

        with col2:
            filtered_expense = abs(filtered_df[filtered_df['amount'] < 0]['amount'].sum())
            st.metric("Filtered Expense", f"₹{filtered_expense:,.2f}")

        with col3:
            filtered_count = len(filtered_df)
            st.metric("Filtered Transactions", f"{filtered_count}")


def show_charts_page() -> None:
    """Display charts and visualizations."""
    st.title("📈 Financial Charts")
    st.caption("Visualize your income, expenses, and trends")

    transactions = db.get_all_transactions()

    if not transactions:
        st.info("📭 No data available for charts. Add some transactions to see visualizations.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    df['amount'] = pd.to_numeric(df['amount'])
    df['date_dt'] = pd.to_datetime(df['date'])

    if len(df) == 0:
        st.warning("⚠️ No valid data to display.")
        return

    # Create tabs for different chart types
    tab1, tab2, tab3 = st.tabs(["📊 Income/Expense by Category", "📈 Cumulative Balance", "📅 Monthly Trends"])

    with tab1:
        show_category_chart(df)

    with tab2:
        show_cumulative_chart(df)

    with tab3:
        show_monthly_trends_chart(df)


def show_category_chart(df: pd.DataFrame) -> None:
    """Show income/expense by category bar chart."""
    st.subheader("Income/Expense by Category")

    # Group by category and sum amounts
    category_totals = df.groupby('category')['amount'].sum().reset_index()
    category_totals = category_totals.sort_values('amount', key=abs, ascending=False)


    fig = px.bar(
        category_totals,
        x='category',
        y='amount',
        title='Income/Expense by Category',
        labels={'amount': 'Amount (₹)', 'category': 'Category'},
        color='amount',
        color_continuous_scale=[[0, CHART_COLORS["negative"]], [0.5, "#FFFFFF"], [1, CHART_COLORS["positive"]]],
        text='amount'
    )

    fig.update_traces(
        texttemplate='₹%{text:,.0f}',
        textposition='outside'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=500
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    st.plotly_chart(fig, use_container_width=True)


def show_cumulative_chart(df: pd.DataFrame) -> None:
    """Show cumulative balance over time."""
    st.subheader("Cumulative Balance Over Time")

    # Sort by date and calculate cumulative sum
    df_sorted = df.sort_values('date_dt')
    df_sorted['cumulative_balance'] = df_sorted['amount'].cumsum()

    fig = px.line(
        df_sorted,
        x='date_dt',
        y='cumulative_balance',
        title='Cumulative Balance Over Time',
        labels={'cumulative_balance': 'Balance (₹)', 'date_dt': 'Date'},
        line_shape='linear'
    )

    fig.update_traces(
        line=dict(color=CHART_COLORS["neutral"], width=2)
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        hovermode='x unified'
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    st.plotly_chart(fig, use_container_width=True)


def show_monthly_trends_chart(df: pd.DataFrame) -> None:
    """Show monthly income/expense trends."""
    st.subheader("Monthly Trends")

    # Ensure datetime index for resampling
    df_temp = df.copy()
    df_temp['date_dt'] = pd.to_datetime(df_temp['date'])
    df_temp = df_temp.set_index('date_dt')

    # Resample to monthly frequency
    monthly_data = df_temp.resample('M').agg({
        'amount': 'sum'
    }).reset_index()

    # Separate income and expenses
    monthly_data['income'] = monthly_data['amount'].clip(lower=0)
    monthly_data['expense'] = monthly_data['amount'].clip(upper=0).abs()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=monthly_data['date_dt'],
        y=monthly_data['income'],
        name='Income',
        marker_color=CHART_COLORS["positive"]
    ))

    fig.add_trace(go.Bar(
        x=monthly_data['date_dt'],
        y=monthly_data['expense'],
        name='Expense',
        marker_color=CHART_COLORS["negative"]
    ))

    fig.update_layout(
        title='Monthly Income vs Expense',
        xaxis_title='Month',
        yaxis_title='Amount (₹)',
        barmode='group',
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)


def show_add_transaction_page() -> None:
    """Display the add transaction form."""
    st.title("✏️ Add New Transaction")
    st.caption("Record a new income or expense transaction")

    with st.form("add_transaction_form"):
        category = st.text_input(
            "Category (e.g., Salary, Rent, Food)",
            help="Enter the category for this transaction"
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            step=100.0,
            help="Enter the transaction amount"
        )

        txn_type = st.radio(
            "Transaction Type",
            ["Income", "Expense"],
            horizontal=True,
            help="Select whether this is income or expense"
        )

        date = st.date_input(
            "Date",
            value=datetime.today(),
            help="Select the transaction date"
        )

        description = st.text_area(
            "Description (optional)",
            help="Add any additional notes about this transaction"
        )

        submitted = st.form_submit_button("Add Transaction", use_container_width=True)

        if submitted:
            if not category:
                st.error("❌ Category is required.")
            else:
                try:
                    # Validate inputs
                    validated_category, validated_amount, validated_date, validated_description = validate_transaction_data(
                        category, str(amount), date.strftime("%Y-%m-%d"), description
                    )

                    # Adjust amount sign based on transaction type
                    final_amount = validated_amount if txn_type == "Income" else -validated_amount

                    # Add transaction to database
                    transaction_id = db.add_transaction(
                        validated_category,
                        final_amount,
                        validated_date,
                        validated_description
                    )

                    st.success(f"✅ {txn_type} added successfully! (ID: {transaction_id})")
                    logger.info(f"{txn_type} added: {validated_category} | ₹{final_amount:,.2f} | {validated_date}")

                    # Clear form by rerunning
                    st.rerun()

                except ValidationError as e:
                    st.error(f"❌ Validation error: {e}")
                except Exception as e:
                    logger.error(f"Failed to add transaction: {e}")
                    st.error("❌ Failed to add transaction. Please check the logs.")


def show_manage_page() -> None:
    """Display the manage transactions page (edit/delete)."""
    st.title("🛠️ Manage Transactions")
    st.caption("Edit or delete existing transactions")

    transactions = db.get_all_transactions()

    if not transactions:
        st.info("📭 No transactions to manage. Add some transactions first.")
        return

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(transactions)
    df['amount'] = pd.to_numeric(df['amount'])
    df['date_dt'] = pd.to_datetime(df['date'])

    # Select transaction to edit/delete
    txn_ids = df['id'].tolist()
    selected_id = st.selectbox(
        "Select Transaction ID to Edit/Delete",
        txn_ids,
        format_func=lambda x: f"ID {x} - {df[df['id']==x]['category'].iloc[0]}: ₹{df[df['id']==x]['amount'].iloc[0]:,.2f} on {df[df['id']==x]['date'].iloc[0]}"
    )

    # Get the row for that ID
    row = df[df['id'] == selected_id].iloc[0]

    # Display current values
    st.write("**Current Details:**")
    st.write(f"**Category:** {row['category']}")
    st.write(f"**Amount:** ₹{row['amount']:,.2f}")
    st.write(f"**Date:** {row['date']}")
    st.write(f"**Description:** {row['description'] or 'No description'}")

    col1, col2 = st.columns(2)

    # ---- DELETE SECTION ----
    with col1:
        if st.button("🗑️ Delete this Transaction", use_container_width=True, type="secondary"):
            try:
                success = db.delete_transaction(selected_id)
                if success:
                    st.success("✅ Transaction deleted successfully!")
                    logger.info(f"Transaction {selected_id} deleted")
                    st.rerun()
                else:
                    st.warning("⚠️ Transaction not found or already deleted.")
            except Exception as e:
                logger.error(f"Failed to delete transaction: {e}")
                st.error("❌ Failed to delete transaction. Please check the logs.")

    # ---- EDIT SECTION ----
    with col2:
        with st.expander("✏️ Edit this Transaction", expanded=True):
            with st.form("edit_transaction_form"):
                # Pre-fill form with current values
                edit_category = st.text_input(
                    "Category",
                    value=row['category'],
                    help="Edit the category for this transaction"
                )

                edit_amount = st.number_input(
                    "Amount (₹)",
                    value=abs(row['amount']),
                    min_value=0.01,
                    step=100.0,
                    help="Edit the transaction amount"
                )

                edit_type = st.radio(
                    "Transaction Type",
                    ["Income", "Expense"],
                    index=0 if row['amount'] > 0 else 1,
                    horizontal=True,
                    help="Select whether this is income or expense"
                )

                edit_date = st.date_input(
                    "Date",
                    value=pd.to_datetime(row['date']),
                    help="Edit the transaction date"
                )

                edit_description = st.text_area(
                    "Description (optional)",
                    value=row['description'] if row['description'] else "",
                    help="Edit any additional notes about this transaction"
                )

                edit_submitted = st.form_submit_button("Update Transaction", use_container_width=True)

                if edit_submitted:
                    if not edit_category:
                        st.error("❌ Category is required.")
                    else:
                        try:
                            # Validate inputs
                            validated_category, validated_amount, validated_date, validated_description = validate_transaction_data(
                                edit_category, str(edit_amount), edit_date.strftime("%Y-%m-%d"), edit_description
                            )

                            # Adjust amount sign based on transaction type
                            final_amount = validated_amount if edit_type == "Income" else -validated_amount

                            # Update transaction in database
                            success = db.update_transaction(
                                selected_id,
                                validated_category,
                                final_amount,
                                validated_date,
                                validated_description
                            )

                            if success:
                                st.success("✅ Transaction updated successfully!")
                                logger.info(f"Transaction {selected_id} updated")
                                st.rerun()
                            else:
                                st.warning("⚠️ Transaction not found or update failed.")

                        except ValidationError as e:
                            st.error(f"❌ Validation error: {e}")
                        except Exception as e:
                            logger.error(f"Failed to update transaction: {e}")
                            st.error("❌ Failed to update transaction. Please check the logs.")


if __name__ == "__main__":
    main()
