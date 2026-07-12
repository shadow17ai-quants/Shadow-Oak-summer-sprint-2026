"""
Streamlit dashboard for OakLedger.
Provides an interactive web interface for visualising and analysing trades.
"""

import streamlit as st
import plotly.express as px
from .analytics import load_trades, compute_metrics, behavioral_metrics

st.set_page_config(page_title="OakLedger", page_icon="📒", layout="wide")
st.sidebar.title("📒 OakLedger")
st.sidebar.caption("Shadow Oak Capitals – S1-P3")

page = st.sidebar.radio("Go to", ["Dashboard", "All Trades", "Analytics"])
df = load_trades()

if df.empty:
    st.warning("No trades found. Use the CLI to add trades, or run seed-data.py")
    st.stop()

if page == "Dashboard":
    st.title("📊 Trade Dashboard")
    m = compute_metrics(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Trades", m["total_trades"])
    c2.metric("Win Rate", f"{m['win_rate']:.1%}")
    c3.metric("Total P&L", f"₹{m['total_pnl']:,.2f}")
    c4.metric("Sharpe", f"{m['sharpe_trades']:.2f}")
    if 'result' in df.columns:
        df_sorted = df.sort_values('trade_date')
        df_sorted['cum'] = df_sorted['result'].sum()
        fig = px.line(df_sorted, x='trade_date', y='cum', title="Equity Curve")
        st.plotly_chart(fig, use_container_width=True)

elif page == "All Trades":
    st.title("📋 All Trades")
    st.dataframe(df)

elif page == "Analytics":
    st.title("🧠 Behavioral Analytics")
    b = behavioral_metrics(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Overconfidence", f"{b['overconfidence_rate']:.1%}")
    c2.metric("Recency Bias", f"{b['recency_bias']:.1%}")
    c3.metric("Loss Aversion", f"{b['loss_aversion_ratio']:.2f}")