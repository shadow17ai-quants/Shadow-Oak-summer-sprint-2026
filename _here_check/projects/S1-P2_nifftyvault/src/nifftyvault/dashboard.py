"""
Streamlit dashboard for NiftyVault — dark navy vault style.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="NiftyVault", page_icon=":bar_chart:", layout="wide")

BG = "#0f1424"
CARD = "#161c33"
BLUE = "#4f8cff"
GREEN = "#4ade80"
RED = "#f87171"
TEXT = "#e8ebf7"
MUTED = "#7d86ab"

st.markdown(
    f"""
<style>
.stApp {{ background-color: {BG}; color: {TEXT}; }}
[data-testid="stMetricValue"] {{ color: {TEXT}; font-size: 1.3rem; }}
[data-testid="stMetricLabel"] {{ color: {MUTED}; }}
div[data-testid="stMetric"] {{ background-color: {CARD}; border-radius: 8px; padding: 12px 14px; }}
section[data-testid="stSidebar"] {{ background-color: {CARD}; }}
</style>
""",
    unsafe_allow_html=True,
)

CSV_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "nifty_50_data.csv"
df = pd.read_csv(CSV_PATH, index_col=0, parse_dates=True)
price_col = "Adj Close" if "Adj Close" in df.columns else "Close"
df = df[[price_col]].rename(columns={price_col: "price"}).dropna()
df["return"] = df["price"].pct_change()

st.sidebar.title(":bar_chart: NiftyVault")
st.sidebar.caption("Shadow Oak Capitals - S1-P2")

st.markdown("### DASHBOARD")

last = df.iloc[-1]
week_chg = (df["price"].iloc[-1] / df["price"].iloc[-6] - 1) if len(df) > 6 else 0
month_chg = (df["price"].iloc[-1] / df["price"].iloc[-22] - 1) if len(df) > 22 else 0
year_chg = df["price"].iloc[-1] / df["price"].iloc[0] - 1

c1, c2, c3, c4 = st.columns(4)
c1.metric("This Week", f"{week_chg:+.2%}")
c2.metric("This Month", f"{month_chg:+.2%}")
c3.metric("This Year", f"{year_chg:+.2%}")
c4.metric("Current Price", f"₹{last['price']:,.2f}")

st.markdown("---")
col_price, col_right = st.columns([2, 1])

with col_price:
    st.markdown("**ACCOUNT BALANCE — NIFTY 50 PRICE**")
    fig = go.Figure(
        data=[
            go.Scatter(
                x=df.index,
                y=df["price"],
                mode="lines",
                line=dict(color=BLUE, width=2),
                fill="tozeroy",
                fillcolor="rgba(79,140,255,0.12)",
            )
        ]
    )
    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font_color=TEXT,
        height=320,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(gridcolor="#232a45"),
        yaxis=dict(gridcolor="#232a45"),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**DAILY RETURNS**")
    recent = df.tail(60)
    colors = [GREEN if v >= 0 else RED for v in recent["return"].fillna(0)]
    fig2 = go.Figure(
        data=[go.Bar(x=recent.index, y=recent["return"], marker_color=colors)]
    )
    fig2.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font_color=TEXT,
        height=220,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(gridcolor="#232a45"),
        yaxis=dict(gridcolor="#232a45", tickformat=".1%"),
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    st.markdown("**TOP MOVERS (LAST 10 DAYS)**")
    last10 = df.tail(10).copy()
    last10 = last10.sort_values("return", ascending=False)
    for date, row in last10.iterrows():
        color = GREEN if row["return"] >= 0 else RED
        sign = "+" if row["return"] >= 0 else ""
        st.markdown(
            f"<div style='background-color:{CARD}; border-radius:6px; padding:8px 10px; margin-bottom:6px;'>"
            f"<b>{date.strftime('%d %b %Y')}</b><br>"
            f"<span style='color:{MUTED}'>₹{row['price']:,.2f}</span> "
            f"<span style='color:{color}; float:right;'>{sign}{row['return']:.2%}</span></div>",
            unsafe_allow_html=True,
        )

st.markdown("---")
st.markdown("**MONTHLY RETURNS HEATMAP**")
d = df.copy()
d["year"] = d.index.year
d["month"] = d.index.month
monthly = d.groupby(["year", "month"])["price"].agg(["first", "last"])
monthly["ret"] = monthly["last"] / monthly["first"] - 1
pivot = monthly["ret"].unstack("month")
fig3 = go.Figure(
    data=go.Heatmap(
        z=pivot.values,
        x=[f"M{m}" for m in pivot.columns],
        y=[str(y) for y in pivot.index],
        colorscale=[[0, RED], [0.5, "#1a2040"], [1, GREEN]],
        zmid=0,
        text=[[f"{v:.1%}" if pd.notna(v) else "" for v in row] for row in pivot.values],
        texttemplate="%{text}",
        showscale=False,
    )
)
fig3.update_layout(
    paper_bgcolor=BG,
    plot_bgcolor=BG,
    font_color=TEXT,
    height=280,
    margin=dict(t=10, b=10, l=10, r=10),
)
st.plotly_chart(fig3, use_container_width=True)
