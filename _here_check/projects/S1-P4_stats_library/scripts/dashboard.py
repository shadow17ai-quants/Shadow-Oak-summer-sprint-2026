"""
Streamlit dashboard for quant_stats Ã¢â‚¬â€ purple fintech-app style, live market data via yfinance.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import yfinance as yf
from quant_stats import full_report

st.set_page_config(page_title="Quant Stats", page_icon=":bar_chart:", layout="wide")

BG = "#f2e8d5"
CARD = "#e8d7b8"
PURPLE = "#7a2e2e"
TEAL = "#a0522d"
PINK = "#c97064"
GREEN = "#4d7c4d"
RED = "#8b2f2f"
TEXT = "#3a2a1e"
MUTED = "#8a7358"

st.markdown(
    f"""
<style>
.stApp {{ background-color: {BG}; color: {TEXT}; }}
[data-testid="stMetricValue"] {{ color: {TEXT}; }}
[data-testid="stMetricLabel"] {{ color: {MUTED}; }}
div[data-testid="stMetric"] {{ background-color: {CARD}; border-radius: 14px; padding: 14px 16px; }}
section[data-testid="stSidebar"] {{ background-color: {CARD}; }}
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.title(":bar_chart: Quant Stats")
st.sidebar.caption("Shadow Oak Capitals - S1-P4")

TICKERS = {
    "Nifty 50": "^NSEI",
    "Sensex": "^BSESN",
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Custom": None,
}
choice = st.sidebar.selectbox("Instrument", list(TICKERS.keys()))
if choice == "Custom":
    ticker = st.sidebar.text_input("Enter ticker (Yahoo Finance format)", "^NSEI")
else:
    ticker = TICKERS[choice]

period = st.sidebar.selectbox("Period", ["6mo", "1y", "2y", "5y", "max"], index=2)
refresh = st.sidebar.button("Refresh data")


@st.cache_data(ttl=300, show_spinner="Fetching live market data...")
def fetch_data(ticker: str, period: str):
    data = yf.download(ticker, period=period, progress=False, auto_adjust=True)
    if data.empty:
        return None
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data


if refresh:
    fetch_data.clear()

data = fetch_data(ticker, period)

if data is None or data.empty:
    st.error(f"No data returned for ticker '{ticker}'. Check the symbol and try again.")
    st.stop()

price_col = "Close"
prices = data[price_col].dropna()
log_returns = np.log(prices / prices.shift(1)).dropna()

if len(log_returns) < 10:
    st.warning("Not enough data points for reliable statistics. Try a longer period.")
    st.stop()

report = full_report(log_returns.values)

last_price = float(prices.iloc[-1])
last_date = prices.index[-1].strftime("%d %b %Y")
day_chg = float(prices.iloc[-1] / prices.iloc[-2] - 1) if len(prices) > 1 else 0.0

tabs = st.tabs(["Overview", "Ratios", "Hypothesis Tests"])

with tabs[0]:
    st.markdown(f"### {choice.upper()} - {ticker}")
    st.caption(
        f"Last close: Rs {last_price:,.2f} on {last_date} ({day_chg:+.2%} vs prior close)"
    )

    c1, c2, c3 = st.columns([1.3, 2, 1.3])

    with c1:
        try:
            st.markdown("**ANNUALIZED RETURN**")
            ann_ret = float(report["sharpe_ratio"]["annualized_return"])
            color = GREEN if ann_ret >= 0 else RED
            st.markdown(
                f"<h2 style='color:{color}'>{ann_ret:.2%}</h2>", unsafe_allow_html=True
            )
            st.metric("Sharpe", f"{float(report['sharpe_ratio']['sharpe_ratio']):.2f}")
            st.metric(
                "Max Drawdown", f"{float(report['max_drawdown']['max_drawdown']):.2%}"
            )
        except Exception as e:
            st.error(f"Annualized Return block failed: {e}")

    with c2:
        try:
            st.markdown("**PRICE HISTORY**")
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=prices.index,
                        y=[float(v) for v in prices.values],
                        mode="lines",
                        line=dict(color=PURPLE, width=2),
                        fill="tozeroy",
                        fillcolor="rgba(139,92,246,0.15)",
                    )
                ]
            )
            fig.update_layout(
                paper_bgcolor=BG,
                plot_bgcolor=BG,
                font_color=TEXT,
                height=260,
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(gridcolor="#2a2444"),
                yaxis=dict(gridcolor="#2a2444"),
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Price History chart failed: {e}")

    with c3:
        try:
            st.markdown("**RISK METRICS**")
            metrics = [
                ("Sortino", float(report["sortino_ratio"]["sortino_ratio"])),
                ("Calmar", float(report["calmar_ratio"]["calmar_ratio"])),
                ("Omega", float(report["omega_ratio"]["omega_ratio"])),
            ]
            for label, val in metrics:
                val_str = (
                    f"{val:.2f}" if val == val and abs(val) != float("inf") else "N/A"
                )
                st.markdown(
                    f"<div style='background-color:{CARD}; border-radius:10px; padding:8px 12px; margin-bottom:8px;'>"
                    f"<span style='color:{MUTED}'>{label}</span>"
                    f"<span style='float:right; color:{TEXT}'>{val_str}</span></div>",
                    unsafe_allow_html=True,
                )
        except Exception as e:
            st.error(f"Risk Metrics block failed: {e}")

    st.markdown("---")
    c4, c5 = st.columns(2)

    with c4:
        try:
            st.markdown("**CUMULATIVE RETURN**")
            cum = (1 + log_returns).cumprod() - 1
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=cum.index,
                        y=[float(v) for v in cum.values],
                        mode="lines",
                        line=dict(color=TEAL, width=2),
                        fill="tozeroy",
                        fillcolor="rgba(34,211,238,0.12)",
                    )
                ]
            )
            fig.update_layout(
                paper_bgcolor=BG,
                plot_bgcolor=BG,
                font_color=TEXT,
                height=260,
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(gridcolor="#2a2444"),
                yaxis=dict(gridcolor="#2a2444", tickformat=".0%"),
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Cumulative Return chart failed: {e}")

    with c5:
        try:
            st.markdown("**UP DAYS vs DOWN DAYS**")
            up = int((log_returns > 0).sum())
            down = int((log_returns <= 0).sum())
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=["Up Days", "Down Days"],
                        values=[up, down],
                        hole=0.6,
                        marker=dict(colors=[TEAL, PINK]),
                        textinfo="percent",
                    )
                ]
            )
            fig.update_layout(
                paper_bgcolor=BG,
                plot_bgcolor=BG,
                font_color=TEXT,
                height=260,
                margin=dict(t=10, b=10, l=10, r=10),
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Up/Down Days chart failed: {e}")

    st.markdown("---")
    try:
        st.markdown("**TEST RESULTS (PASS/FAIL)**")
        tests = [
            "jarque_bera_test",
            "shapiro_wilk_test",
            "ljung_box_test",
            "adf_test",
            "fit_student_t",
        ]
        labels = [t.replace("_test", "").replace("_", " ").title() for t in tests]
        p_values = [
            float(report[t]["p_value"]) if report[t]["p_value"] is not None else 0.0
            for t in tests
        ]
        colors = [GREEN if p >= 0.05 else RED for p in p_values]
        fig = go.Figure(
            data=[
                go.Bar(
                    x=labels,
                    y=p_values,
                    marker_color=colors,
                    text=[f"{p:.3g}" for p in p_values],
                    textposition="outside",
                )
            ]
        )
        fig.add_hline(
            y=0.05, line_dash="dash", line_color=MUTED, annotation_text="ÃŽÂ± = 0.05"
        )
        fig.update_layout(
            paper_bgcolor=BG,
            plot_bgcolor=BG,
            font_color=TEXT,
            height=300,
            margin=dict(t=30, b=10, l=10, r=10),
            xaxis=dict(gridcolor="#2a2444"),
            yaxis=dict(gridcolor="#2a2444", title="p-value"),
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Test Results chart failed: {e}")

with tabs[1]:
    st.markdown("### RATIO BREAKDOWN")
    st.caption("What each risk/return metric actually tells you")

    def ratio_card(
        title, value, good_if, fmt="{:.2f}", explain_good="", explain_bad=""
    ):
        try:
            v = float(value)
            is_good = good_if(v)
            color = GREEN if is_good else RED
            verdict = "GOOD" if is_good else "WEAK"
            explain = explain_good if is_good else explain_bad
            val_str = fmt.format(v) if v == v and abs(v) != float("inf") else "N/A"
            st.markdown(
                f"<div style='background-color:{CARD}; border-radius:14px; padding:16px 20px; margin-bottom:12px; border-left: 4px solid {color};'>"
                f"<div style='display:flex; justify-content:space-between; align-items:center;'>"
                f"<span style='color:{MUTED}; font-size:13px; text-transform:uppercase; letter-spacing:0.5px;'>{title}</span>"
                f"<span style='color:{color}; font-size:12px; font-weight:600; background-color:{BG}; padding:2px 8px; border-radius:6px;'>{verdict}</span>"
                f"</div>"
                f"<div style='color:{TEXT}; font-size:28px; font-weight:700; margin:4px 0;'>{val_str}</div>"
                f"<div style='color:{MUTED}; font-size:13px;'>{explain}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"{title} card failed: {e}")

    rc1, rc2 = st.columns(2)
    with rc1:
        ratio_card(
            "Sharpe Ratio",
            report["sharpe_ratio"]["sharpe_ratio"],
            lambda v: v > 1,
            explain_good="Returns are strong relative to volatility taken on.",
            explain_bad="Return isn't compensating you enough for the volatility - risk-adjusted performance is weak.",
        )
        ratio_card(
            "Calmar Ratio",
            report["calmar_ratio"]["calmar_ratio"],
            lambda v: v > 0.5,
            explain_good="Annual return holds up well against the worst drawdown seen.",
            explain_bad="Drawdowns are large relative to annual return - a rough ride for the payoff.",
        )
        ratio_card(
            "Max Drawdown",
            report["max_drawdown"]["max_drawdown"],
            lambda v: v > -0.15,
            fmt="{:.2%}",
            explain_good="Peak-to-trough loss stayed within a manageable range.",
            explain_bad="Peak-to-trough loss was steep - this is the worst-case pain an investor felt historically.",
        )
    with rc2:
        ratio_card(
            "Sortino Ratio",
            report["sortino_ratio"]["sortino_ratio"],
            lambda v: v > 1,
            explain_good="Good return per unit of *downside-only* risk (ignores upside swings).",
            explain_bad="Downside volatility is eating into returns more than it should.",
        )
        ratio_card(
            "Omega Ratio",
            report["omega_ratio"]["omega_ratio"],
            lambda v: v > 1,
            explain_good="Gains outweigh losses across the return distribution (>1 = net positive edge).",
            explain_bad="Losses outweigh gains across the distribution - no statistical edge yet (<1).",
        )
        try:
            ann_ret = float(report["sharpe_ratio"]["annualized_return"])
            color = GREEN if ann_ret >= 0 else RED
            st.markdown(
                f"<div style='background-color:{CARD}; border-radius:14px; padding:16px 20px; margin-bottom:12px; border-left: 4px solid {color};'>"
                f"<span style='color:{MUTED}; font-size:13px; text-transform:uppercase;'>Annualized Return</span>"
                f"<div style='color:{color}; font-size:28px; font-weight:700; margin:4px 0;'>{ann_ret:.2%}</div>"
                f"<div style='color:{MUTED}; font-size:13px;'>The yearly growth rate implied by this period's returns.</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"Annualized Return card failed: {e}")

with tabs[2]:
    st.markdown("### STATISTICAL PROPERTIES OF RETURNS")
    st.caption("Each test checks a real assumption used in trading/risk models")

    def test_card(title, stat, p, passed, meaning):
        color = GREEN if passed else RED
        verdict = "PASS" if passed else "FLAG"
        p_str = f"{float(p):.3g}" if p is not None else "N/A"
        stat_str = f"{float(stat):.3g}" if stat is not None else "N/A"
        st.markdown(
            f"<div style='background-color:{CARD}; border-radius:14px; padding:16px 20px; margin-bottom:12px; border-left: 4px solid {color};'>"
            f"<div style='display:flex; justify-content:space-between; align-items:center;'>"
            f"<span style='color:{TEXT}; font-size:16px; font-weight:600;'>{title}</span>"
            f"<span style='color:{color}; font-size:12px; font-weight:600; background-color:{BG}; padding:2px 8px; border-radius:6px;'>{verdict}</span>"
            f"</div>"
            f"<div style='color:{MUTED}; font-size:13px; margin:6px 0;'>statistic = {stat_str} &nbsp;|&nbsp; p-value = {p_str}</div>"
            f"<div style='color:{TEXT}; font-size:14px;'>{meaning}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    try:
        jb = report["jarque_bera_test"]
        test_card(
            "Normality (Jarque-Bera)",
            jb["statistic"],
            jb["p_value"],
            jb["p_value"] >= 0.05,
            "Returns are NOT normally distributed - expect more extreme days than a bell curve predicts. Standard VaR/normal-assumption models will understate risk.",
        )
    except Exception as e:
        st.error(f"Jarque-Bera card failed: {e}")

    try:
        sw = report["shapiro_wilk_test"]
        test_card(
            "Normality (Shapiro-Wilk)",
            sw["statistic"],
            sw["p_value"],
            sw["p_value"] >= 0.05,
            "Confirms the Jarque-Bera result independently - the return distribution deviates from normal, usually due to fat tails or skew.",
        )
    except Exception as e:
        st.error(f"Shapiro-Wilk card failed: {e}")

    try:
        lb = report["ljung_box_test"]
        passed = lb["p_value"] >= 0.05
        meaning = (
            "No significant autocorrelation - today's return doesn't meaningfully predict tomorrow's from own history alone (closer to a random walk)."
            if passed
            else "Significant autocorrelation detected - past returns carry some predictive signal for future returns. Worth exploring as a momentum/mean-reversion feature."
        )
        test_card(
            "Autocorrelation (Ljung-Box)",
            lb["statistic"],
            lb["p_value"],
            passed,
            meaning,
        )
    except Exception as e:
        st.error(f"Ljung-Box card failed: {e}")

    try:
        adf = report["adf_test"]
        test_card(
            "Stationarity (ADF)",
            adf["statistic"],
            adf["p_value"],
            adf["p_value"] < 0.05,
            "Series is stationary (mean/variance don't drift indefinitely) - safer to model directly without differencing.",
        )
    except Exception as e:
        st.error(f"ADF card failed: {e}")

    try:
        st_t = report["fit_student_t"]
        df = float(st_t["degrees_of_freedom"])
        passed = df >= 5
        meaning = (
            f"Degrees of freedom = {df:.2f}. Fat tails are extreme (df < 5) - large moves happen far more often than a normal distribution assumes. Size positions and stop-losses with this in mind."
            if not passed
            else f"Degrees of freedom = {df:.2f}. Tails are closer to normal - extreme moves are relatively less frequent."
        )
        test_card(
            "Tail Risk (Student-t fit)",
            st_t["statistic"],
            st_t["p_value"],
            passed,
            meaning,
        )
    except Exception as e:
        st.error(f"Student-t card failed: {e}")
