"""
Streamlit dashboard for OakLedger — dark trading-journal style matching reference layout.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from oakledger.analytics import load_trades, compute_metrics, behavioral_metrics, monthly_returns

st.set_page_config(page_title="OakLedger", page_icon=":notebook:", layout="wide")

BG = "#000000"
CARD = "#0a0a0a"
GREEN = "#4ade80"
RED = "#f87171"
BLUE = "#60a5fa"
ORANGE = "#fb923c"
TEXT = "#e5e5e5"
MUTED = "#8a8a8a"

st.markdown(f"""
<style>
.stApp {{ background-color: {BG}; color: {TEXT}; }}
[data-testid="stMetricValue"] {{ color: {TEXT}; font-size: 1.4rem; }}
[data-testid="stMetricLabel"] {{ color: {MUTED}; font-size: 0.75rem; letter-spacing: 1px; }}
div[data-testid="stMetric"] {{ background-color: {CARD}; border: 1px solid #262626; border-radius: 4px; padding: 10px 14px; }}
section[data-testid="stSidebar"] {{ background-color: {CARD}; }}
h1, h2, h3 {{ letter-spacing: 1px; }}
</style>
""", unsafe_allow_html=True)

st.sidebar.title(":notebook: OakLedger")
st.sidebar.caption("Shadow Oak Capitals - S1-P3")
page = st.sidebar.radio("Go to", ["Dashboard", "All Trades", "Analytics"])

df = load_trades()
if df.empty:
    st.warning("No trades found. Run seed-data.py first.")
    st.stop()

m = compute_metrics(df)

if page == "Dashboard":
    st.markdown("### TRADING JOURNAL")

    beg_balance = 2_000_000.0
    net_profit = m["total_pnl"]
    end_balance = beg_balance + net_profit

    c1, c2, c3 = st.columns(3)
    c1.metric("BEG. BALANCE", f"₹{beg_balance:,.2f}")
    c2.metric("NET PROFIT", f"₹{net_profit:,.2f}")
    c3.metric("END BALANCE", f"₹{end_balance:,.2f}")

    st.markdown("---")

    col_perf, col_wl, col_stats = st.columns([1.1, 1, 1.3])

    with col_perf:
        st.markdown("**OVERALL PERFORMANCE**")
        total_gain = m["max_profit"] * m["win_trades"] if m["win_trades"] else m["total_pnl"] * 0.6
        wins_sum = df.copy()
        wins_sum['result'] = pd.to_numeric(wins_sum['result'], errors='coerce')
        gain_sum = wins_sum.loc[wins_sum['result'] > 0, 'result'].sum()
        loss_sum = wins_sum.loc[wins_sum['result'] < 0, 'result'].sum()
        st.write(f"Total Gain: **:green[₹{gain_sum:,.2f}]**")
        st.write(f"Total Loss: **:red[₹{loss_sum:,.2f}]**")
        st.write(f"Gain/Loss: **₹{net_profit:,.2f}**")
        pct = m['win_rate']
        st.progress(min(max(pct, 0.0), 1.0))

    with col_wl:
        st.markdown("**WIN / LOSS**")
        fig = go.Figure(data=[go.Pie(
            labels=["Win", "Loss"], values=[m["win_trades"], m["loss_trades"]],
            hole=0.6, marker=dict(colors=[GREEN, RED]), textinfo="none",
        )])
        fig.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color=TEXT, height=220,
                           margin=dict(t=10, b=10, l=10, r=10), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_stats:
        st.markdown("**TRADE STATISTICS**")
        s1, s2 = st.columns(2)
        s1.metric("Win Trades", m["win_trades"])
        s2.metric("Loss Trades", m["loss_trades"])
        s1.metric("Win Rate", f"{m['win_rate']:.1%}")
        s2.metric("R:R", f"{m['rr_ratio']:.2f}")

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**MONTHLY RETURN**")
        mr = monthly_returns(df)
        if not mr.empty:
            colors = [GREEN if v >= 0 else RED for v in mr['pnl']]
            fig = go.Figure(data=[go.Bar(x=mr['month'], y=mr['pnl'], marker_color=colors)])
            fig.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color=TEXT, height=300,
                               margin=dict(t=10, b=10, l=10, r=10),
                               xaxis=dict(gridcolor="#1f1f1f"), yaxis=dict(gridcolor="#1f1f1f"))
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("**CUMULATIVE PROFIT**")
        d = df.copy()
        d['result'] = pd.to_numeric(d['result'], errors='coerce')
        d['trade_date'] = pd.to_datetime(d['trade_date'], errors='coerce')
        d = d.dropna(subset=['result', 'trade_date']).sort_values('trade_date')
        d['cum'] = d['result'].cumsum()
        fig = go.Figure(data=[go.Scatter(x=d['trade_date'], y=d['cum'], mode='lines',
                                          line=dict(color=GREEN, width=2), fill='tozeroy',
                                          fillcolor="rgba(74,222,128,0.08)")])
        fig.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color=TEXT, height=300,
                           margin=dict(t=10, b=10, l=10, r=10),
                           xaxis=dict(gridcolor="#1f1f1f"), yaxis=dict(gridcolor="#1f1f1f"))
        st.plotly_chart(fig, use_container_width=True)

elif page == "All Trades":
    st.title("All Trades")
    st.dataframe(df, use_container_width=True)

elif page == "Analytics":
    st.title("Behavioral Analytics")
    b = behavioral_metrics(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Overconfidence", f"{b['overconfidence_rate']:.1%}")
    c2.metric("Recency Bias", f"{b['recency_bias']:.1%}")
    c3.metric("Loss Aversion", f"{b['loss_aversion_ratio']:.2f}")