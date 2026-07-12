"""

MarketVault — live dashboard + strategy builder.

Theme: rich pistachio / sage with a maroon accent thread.

"""



import sys

from pathlib import Path



sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))



from datetime import datetime



import numpy as np

import pandas as pd

import plotly.graph_objects as go

from plotly.subplots import make_subplots

import streamlit as st

import yfinance as yf



st.set_page_config(page_title="MarketVault", page_icon=":bank:", layout="wide")



# ---------------------------------------------------------------------------

# THEME — pistachio/sage paper with a maroon accent thread. Richer and more

# saturated than a pastel: deep pistachio for headers, mid pistachio for

# chart lines, maroon reserved for accents/borders/sell-side signals so it

# reads as a deliberate thread rather than a second competing brand color.

# ---------------------------------------------------------------------------

PAPER = "#eef3e6"            # pistachio paper background

PANEL = "#ffffff"            # card background

INK = "#1f2e1a"              # deep sage-black ink (body text)

INK_MUTED = "#54634c"        # muted secondary text

LINE = "#c9d9bd"             # hairline rule / border

PISTACHIO_DEEP = "#2f5525"   # headers, primary brand text

PISTACHIO = "#4d7c3e"        # chart lines, primary accent

PISTACHIO_SOFT = "#dcead0"   # tint for chart fills

MAROON = "#7a2331"           # accent thread — borders, badges, sell markers

MAROON_SOFT = "#f3e3e0"      # tint for maroon badges

GREEN_UP = "#2f7d3a"

RED_DOWN = "#a3392f"



st.markdown(

    f"""

<style>

.stApp {{ background-color: {PAPER}; color: {INK}; }}

h1, h2, h3, h4 {{ color: {PISTACHIO_DEEP} !important; font-family: Georgia, 'Times New Roman', serif; }}

p, span, label, div {{ color: {INK}; }}

[data-testid="stMetricValue"] {{ color: {PISTACHIO_DEEP}; font-weight: 700; }}

[data-testid="stMetricLabel"] {{ color: {INK_MUTED}; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.06em; }}

div[data-testid="stMetric"] {{

    background-color: {PANEL};

    border: 1px solid {LINE};

    border-left: 3px solid {MAROON};

    border-radius: 4px;

    padding: 14px 16px;

}}

section[data-testid="stSidebar"] {{ background-color: {PANEL}; border-right: 1px solid {LINE}; }}

section[data-testid="stSidebar"] * {{ color: {INK} !important; }}
    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] [data-baseweb="select"] div[role="button"] {{
        background-color: {PANEL} !important;
        color: {INK} !important;
        border: 1px solid {MAROON} !important;
    }}
    section[data-testid="stSidebar"] [data-baseweb="select"] svg {{ fill: {MAROON} !important; }}
    [data-baseweb="popover"] [role="listbox"] {{ background-color: {PANEL} !important; }}
    [data-baseweb="popover"] [role="option"] {{ background-color: {PANEL} !important; color: {INK} !important; }}
    [data-baseweb="popover"] [role="option"]:hover {{ background-color: {PISTACHIO_SOFT} !important; }}
    section[data-testid="stSidebar"] [data-baseweb="tag"] {{ background-color: {MAROON} !important; color: {PANEL} !important; }}
    section[data-testid="stSidebar"] [data-baseweb="tag"] span {{ color: {PANEL} !important; }}

.stTabs [data-baseweb="tab"] {{ color: {INK_MUTED}; font-weight: 600; }}

.stTabs [aria-selected="true"] {{ color: {PISTACHIO_DEEP} !important; border-bottom-color: {MAROON} !important; }}

hr {{ border-color: {LINE}; }}

.vault-seal {{

    display: inline-block; width: 34px; height: 34px; border-radius: 50%;

    border: 2px solid {MAROON}; text-align: center; line-height: 30px;

    color: {MAROON}; font-weight: 700; font-family: Georgia, serif;

    margin-right: 8px;

}}

.ledger-row {{

    background-color: {PANEL}; border: 1px solid {LINE}; border-radius: 4px;

    padding: 8px 12px; margin-bottom: 6px;

}}

.alert-badge {{

    display: inline-block; background-color: {MAROON_SOFT}; color: {MAROON};

    border: 1px solid {MAROON}; border-radius: 999px; padding: 3px 12px;

    font-size: 0.78rem; font-weight: 700; margin: 2px 6px 2px 0;

}}

.ok-badge {{

    display: inline-block; background-color: {PISTACHIO_SOFT}; color: {PISTACHIO_DEEP};

    border: 1px solid {PISTACHIO}; border-radius: 999px; padding: 3px 12px;

    font-size: 0.78rem; font-weight: 700; margin: 2px 6px 2px 0;

}}

div.stButton > button {{

    background-color: {PISTACHIO_DEEP}; color: {PAPER}; border: none; font-weight: 600;

}}

div.stButton > button:hover {{ background-color: {MAROON}; color: {PAPER}; }}

""",

    unsafe_allow_html=True,

)



TICKERS = {
    "Nifty 50": "^NSEI",
    "Nasdaq Composite": "^IXIC",
    "Sensex": "^BSESN",
    "Bank Nifty": "^NSEBANK",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "ICICI Bank (ADR)": "IBN",
    "Larsen & Toubro": "LT.NS",
    "ITC": "ITC.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Axis Bank": "AXISBANK.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "BlackRock": "BLK",
    "Custom": None,
}





# ---------------------------------------------------------------------------

# LIVE DATA PIPELINE

# ---------------------------------------------------------------------------

@st.cache_data(ttl=300, show_spinner="Pulling live data from Yahoo Finance...")

def fetch_live(ticker: str, period: str, interval: str) -> pd.DataFrame | None:

    data = yf.download(

        ticker, period=period, interval=interval,

        auto_adjust=True, progress=False, threads=False, timeout=30,

    )

    if data is None or data.empty:

        return None

    if isinstance(data.columns, pd.MultiIndex):

        data.columns = data.columns.get_level_values(0)

    return data





def prep_frame(raw: pd.DataFrame) -> pd.DataFrame:

    d = raw[["Close"]].rename(columns={"Close": "price"}).dropna()

    d["return"] = d["price"].pct_change()

    d["log_return"] = np.log(d["price"] / d["price"].shift(1))

    d["rsi"] = compute_rsi(d["price"], 14)

    d["vol_20"] = d["return"].rolling(20).std() * np.sqrt(252)

    return d





def compute_rsi(price: pd.Series, window: int) -> pd.Series:

    delta = price.diff()

    gain = delta.clip(lower=0).rolling(window).mean()

    loss = (-delta.clip(upper=0)).rolling(window).mean()

    rs = gain / loss.replace(0, np.nan)

    return 100 - (100 / (1 + rs))





def run_signals(strat: pd.DataFrame, signal_choices, key_prefix: str, container):

    """Renders signal controls in `container`, returns (strat_with_signals, signal_cols)."""

    signal_cols = []

    cols = container.columns(3)



    if "Moving Average Crossover" in signal_choices:

        with cols[0]:

            st.markdown("*MA Crossover*")

            ma_type = st.selectbox("MA type", ["SMA", "EMA"], key=f"{key_prefix}_ma_type")

            fast_win = st.slider("Fast window", 5, 50, 20, key=f"{key_prefix}_fast_win")

            slow_win = st.slider("Slow window", 20, 200, 50, key=f"{key_prefix}_slow_win")

        if ma_type == "SMA":

            strat["ma_fast"] = strat["price"].rolling(fast_win).mean()

            strat["ma_slow"] = strat["price"].rolling(slow_win).mean()

        else:

            strat["ma_fast"] = strat["price"].ewm(span=fast_win, adjust=False).mean()

            strat["ma_slow"] = strat["price"].ewm(span=slow_win, adjust=False).mean()

        strat["sig_ma"] = (strat["ma_fast"] > strat["ma_slow"]).astype(int)

        signal_cols.append("sig_ma")



    if "RSI" in signal_choices:

        with cols[1]:

            st.markdown("*RSI*")

            rsi_win = st.slider("RSI window", 5, 30, 14, key=f"{key_prefix}_rsi_win")

            rsi_buy = st.slider("Buy below", 10, 50, 30, key=f"{key_prefix}_rsi_buy")

            rsi_sell = st.slider("Sell above", 50, 90, 70, key=f"{key_prefix}_rsi_sell")

        strat["rsi_sig_raw"] = compute_rsi(strat["price"], rsi_win)

        strat["sig_rsi"] = np.nan

        strat.loc[strat["rsi_sig_raw"] < rsi_buy, "sig_rsi"] = 1

        strat.loc[strat["rsi_sig_raw"] > rsi_sell, "sig_rsi"] = 0

        strat["sig_rsi"] = strat["sig_rsi"].ffill().fillna(0).astype(int)

        signal_cols.append("sig_rsi")



    if "Bollinger Bands" in signal_choices:

        with cols[2]:

            st.markdown("*Bollinger Bands*")

            bb_win = st.slider("BB window", 10, 50, 20, key=f"{key_prefix}_bb_win")

            bb_std = st.slider("Std devs", 1.0, 3.0, 2.0, step=0.5, key=f"{key_prefix}_bb_std")

        mid = strat["price"].rolling(bb_win).mean()

        std = strat["price"].rolling(bb_win).std()

        strat["bb_upper"] = mid + bb_std * std

        strat["bb_lower"] = mid - bb_std * std

        strat["sig_bb"] = np.nan

        strat.loc[strat["price"] < strat["bb_lower"], "sig_bb"] = 1

        strat.loc[strat["price"] > strat["bb_upper"], "sig_bb"] = 0

        strat["sig_bb"] = strat["sig_bb"].ffill().fillna(0).astype(int)

        signal_cols.append("sig_bb")



    return strat, signal_cols





def backtest(strat: pd.DataFrame, signal_cols, combine_logic: str) -> pd.DataFrame:

    if combine_logic.startswith("AND"):

        strat["position"] = (strat[signal_cols].sum(axis=1) == len(signal_cols)).astype(int)

    else:

        strat["position"] = (strat[signal_cols].sum(axis=1) > 0).astype(int)

    strat["position"] = strat["position"].shift(1).fillna(0)

    strat["strategy_return"] = strat["position"] * strat["price"].pct_change().fillna(0)

    strat["buyhold_return"] = strat["price"].pct_change().fillna(0)

    strat["strategy_equity"] = (1 + strat["strategy_return"]).cumprod()

    strat["buyhold_equity"] = (1 + strat["buyhold_return"]).cumprod()

    return strat





def strategy_stats(strat: pd.DataFrame) -> dict:

    trades = strat["position"].diff().fillna(0)

    n_trades = int((trades != 0).sum())

    strat_total_ret = strat["strategy_equity"].iloc[-1] - 1

    bh_total_ret = strat["buyhold_equity"].iloc[-1] - 1

    strat_vol = strat["strategy_return"].std() * np.sqrt(252)

    strat_sharpe = (strat["strategy_return"].mean() * 252) / strat_vol if strat_vol > 0 else 0

    strat_dd = (strat["strategy_equity"] - strat["strategy_equity"].cummax()) / strat["strategy_equity"].cummax()

    return {

        "trades": trades,

        "n_trades": n_trades,

        "strategy_return": strat_total_ret,

        "buyhold_return": bh_total_ret,

        "sharpe": strat_sharpe,

        "max_drawdown": strat_dd.min(),

    }





# ---------------------------------------------------------------------------

# SIDEBAR

# ---------------------------------------------------------------------------

st.sidebar.markdown(

    f"<span class='vault-seal'>N</span>"

    f"<b style='font-size:1.3rem; color:{PISTACHIO_DEEP}'>MarketVault</b>",

    unsafe_allow_html=True,

)

st.sidebar.caption("Shadow Oak Capitals — S1-P2 · live pipeline")

st.sidebar.markdown("---")



mode = st.sidebar.radio("Mode", ["Single Instrument", "Portfolio"], horizontal=True)



if mode == "Single Instrument":

    choice = st.sidebar.selectbox("Instrument", list(TICKERS.keys()))

    ticker = st.sidebar.text_input("Ticker (Yahoo Finance format)", "^NSEI") if choice == "Custom" else TICKERS[choice]

    watchlist = [(choice if choice != "Custom" else ticker, ticker)]

else:

    default_syms = ["Nifty 50", "Bank Nifty", "Reliance", "TCS"]

    picks = st.sidebar.multiselect("Instruments", list(TICKERS.keys())[:-1], default=default_syms)

    watchlist = [(name, TICKERS[name]) for name in picks]



period = st.sidebar.selectbox("Period", ["6mo", "1y", "2y", "5y", "10y", "max"], index=3)

interval = st.sidebar.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)



refresh = st.sidebar.button(":arrows_counterclockwise: Refresh live data", width="stretch")

st.sidebar.caption("Cached 5 min per instrument/period. Refresh forces a new pull.")



st.sidebar.markdown("---")

st.sidebar.markdown("**Price alerts**")

alert_rsi_high = st.sidebar.slider("Flag RSI above", 60, 95, 70)

alert_rsi_low = st.sidebar.slider("Flag RSI below", 5, 40, 30)

alert_dd = st.sidebar.slider("Flag drawdown beyond", 5, 50, 15, help="Percent below peak") / 100



if refresh:

    fetch_live.clear()



if not watchlist:

    st.warning("Pick at least one instrument in the sidebar.")

    st.stop()



# ---------------------------------------------------------------------------

# FETCH ALL WATCHLIST DATA

# ---------------------------------------------------------------------------

frames = {}

for name, tkr in watchlist:

    raw = fetch_live(tkr, period, interval)

    if raw is not None and not raw.empty:

        frames[name] = prep_frame(raw)



if not frames:

    st.error("No data returned for the selected instrument(s). Check symbols, period, or your connection.")

    st.stop()



primary_name = watchlist[0][0]

primary_ticker = watchlist[0][1]

df = frames.get(primary_name)

last_fetch = datetime.now().strftime("%H:%M:%S")



st.markdown(f"### {primary_name.upper()} — LEDGER" if mode == "Single Instrument" else "### PORTFOLIO — LEDGER")

st.caption(f"Live via Yahoo Finance · last pulled {last_fetch} · interval {interval}")



# ---------------------------------------------------------------------------

# ALERTS BANNER

# ---------------------------------------------------------------------------

alert_msgs = []

for name, d in frames.items():

    last_rsi = d["rsi"].iloc[-1]

    cummax = d["price"].cummax()

    dd_now = (d["price"].iloc[-1] - cummax.iloc[-1]) / cummax.iloc[-1]

    if pd.notna(last_rsi) and last_rsi >= alert_rsi_high:

        alert_msgs.append(f"{name}: RSI {last_rsi:.0f} (overbought)")

    if pd.notna(last_rsi) and last_rsi <= alert_rsi_low:

        alert_msgs.append(f"{name}: RSI {last_rsi:.0f} (oversold)")

    if dd_now <= -alert_dd:

        alert_msgs.append(f"{name}: drawdown {dd_now:.1%} from peak")



if alert_msgs:

    st.markdown(

        "".join(f"<span class='alert-badge'>:warning: {m}</span>" for m in alert_msgs),

        unsafe_allow_html=True,

    )

else:

    st.markdown("<span class='ok-badge'>:white_check_mark: No alerts triggered</span>", unsafe_allow_html=True)



st.markdown("---")



# ---------------------------------------------------------------------------

# HEADER METRICS (primary instrument)

# ---------------------------------------------------------------------------

last = df.iloc[-1]

week_chg = (df["price"].iloc[-1] / df["price"].iloc[-6] - 1) if len(df) > 6 else 0

month_chg = (df["price"].iloc[-1] / df["price"].iloc[-22] - 1) if len(df) > 22 else 0

period_chg = df["price"].iloc[-1] / df["price"].iloc[0] - 1



c1, c2, c3, c4 = st.columns(4)

c1.metric("This Week", f"{week_chg:+.2%}")

c2.metric("This Month", f"{month_chg:+.2%}")

c3.metric("Period Return", f"{period_chg:+.2%}")

c4.metric("Last Price", f"{last['price']:,.2f}")



st.markdown("---")



tab_overview, tab_portfolio, tab_movers, tab_heatmap, tab_strategy, tab_compare = st.tabs(

    [

        ":bar_chart: Overview", ":briefcase: Portfolio", ":dart: Top Movers",

        ":fire: Heatmap", ":gear: Strategy Builder", ":scales: Compare Strategies",

    ]

)



# ---------------------------------------------------------------------------

# TAB — OVERVIEW (price + RSI + volatility overlay)

# ---------------------------------------------------------------------------

with tab_overview:

    col_price, col_right = st.columns([2, 1])



    with col_price:

        st.markdown("**PRICE with RSI & VOLATILITY OVERLAY**")

        fig = make_subplots(

            rows=3, cols=1, shared_xaxes=True, row_heights=[0.55, 0.22, 0.23],

            vertical_spacing=0.04,

        )

        fig.add_trace(

            go.Scatter(x=df.index, y=df["price"], mode="lines", name="Price",

                       line=dict(color=PISTACHIO, width=2), fill="tozeroy",

                       fillcolor="rgba(77,124,62,0.10)"),

            row=1, col=1,

        )

        fig.add_trace(

            go.Scatter(x=df.index, y=df["rsi"], mode="lines", name="RSI (14)",

                       line=dict(color=MAROON, width=1.5)),

            row=2, col=1,

        )

        fig.add_hline(y=70, line_dash="dot", line_color=INK_MUTED, row=2, col=1)

        fig.add_hline(y=30, line_dash="dot", line_color=INK_MUTED, row=2, col=1)

        fig.add_trace(

            go.Scatter(x=df.index, y=df["vol_20"], mode="lines", name="20d Ann. Volatility",

                       line=dict(color=PISTACHIO_DEEP, width=1.5), fill="tozeroy",

                       fillcolor="rgba(47,85,37,0.08)"),

            row=3, col=1,

        )

        fig.update_layout(

            paper_bgcolor=PAPER, plot_bgcolor=PANEL, font_color=INK,

            height=520, margin=dict(t=10, b=10, l=10, r=10), showlegend=False,

        )

        fig.update_yaxes(gridcolor=LINE, title_text="Price", row=1, col=1)

        fig.update_yaxes(gridcolor=LINE, title_text="RSI", range=[0, 100], row=2, col=1)

        fig.update_yaxes(gridcolor=LINE, title_text="Vol", tickformat=".0%", row=3, col=1)

        fig.update_xaxes(gridcolor=LINE, row=3, col=1)

        st.plotly_chart(fig, width="stretch")



    with col_right:

        st.markdown("**RISK SNAPSHOT**")

        vol_annual = df["return"].std() * np.sqrt(252)

        sharpe = (df["return"].mean() * 252) / vol_annual if vol_annual > 0 else 0

        cummax = df["price"].cummax()

        dd = (df["price"] - cummax) / cummax

        max_dd = dd.min()

        for label, val, fmt in [

            ("Annualized Volatility", vol_annual, "{:.2%}"),

            ("Sharpe (rf=0)", sharpe, "{:.2f}"),

            ("Max Drawdown", max_dd, "{:.2%}"),

            ("Current RSI (14)", df["rsi"].iloc[-1], "{:.1f}"),

        ]:

            st.markdown(

                f"<div class='ledger-row'><span style='color:{INK_MUTED}'>{label}</span>"

                f"<span style='float:right; font-weight:700; color:{PISTACHIO_DEEP}'>{fmt.format(val)}</span></div>",

                unsafe_allow_html=True,

            )



        st.markdown("**EXPORT**")

        csv_bytes = df.to_csv().encode("utf-8")

        st.download_button(

            ":inbox_tray: Download price/RSI/vol data (CSV)",

            data=csv_bytes,

            file_name=f"{primary_ticker.replace('^', '')}_{period}_{interval}.csv",

            mime="text/csv",

            width="stretch",

        )

        report_lines = [

            f"MarketVault report — {primary_name} ({primary_ticker})",

            f"Generated: {last_fetch}  Period: {period}  Interval: {interval}",

            "",

            f"Last price: {last['price']:,.2f}",

            f"This week: {week_chg:+.2%}",

            f"This month: {month_chg:+.2%}",

            f"Period return: {period_chg:+.2%}",

            f"Annualized volatility: {vol_annual:.2%}",

            f"Sharpe (rf=0): {sharpe:.2f}",

            f"Max drawdown: {max_dd:.2%}",

            f"Current RSI (14): {df['rsi'].iloc[-1]:.1f}",

        ]

        st.download_button(

            ":page_facing_up: Download summary report (TXT)",

            data="\n".join(report_lines).encode("utf-8"),

            file_name=f"{primary_ticker.replace('^', '')}_report.txt",

            mime="text/plain",

            width="stretch",

        )



# ---------------------------------------------------------------------------

# TAB — PORTFOLIO

# ---------------------------------------------------------------------------

with tab_portfolio:

    if mode == "Single Instrument":

        st.info("Switch the sidebar to **Portfolio** mode and pick multiple instruments to compare them here.")

    else:

        st.markdown("**NORMALIZED PERFORMANCE — GROWTH OF ₹1**")

        fig_p = go.Figure()

        palette = [PISTACHIO, MAROON, PISTACHIO_DEEP, INK_MUTED, "#8a6d3b", "#3f6b8a"]

        for i, (name, d) in enumerate(frames.items()):

            norm = d["price"] / d["price"].iloc[0]

            fig_p.add_trace(

                go.Scatter(x=d.index, y=norm, mode="lines", name=name,

                           line=dict(color=palette[i % len(palette)], width=2))

            )

        fig_p.update_layout(

            paper_bgcolor=PAPER, plot_bgcolor=PANEL, font_color=INK, height=380,

            margin=dict(t=10, b=10, l=10, r=10),

            xaxis=dict(gridcolor=LINE), yaxis=dict(gridcolor=LINE, title="Growth of ₹1"),

            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),

        )

        st.plotly_chart(fig_p, width="stretch")



        st.markdown("**PORTFOLIO SUMMARY**")

        rows = []

        for name, d in frames.items():

            ann_vol = d["return"].std() * np.sqrt(252)

            sharpe_p = (d["return"].mean() * 252) / ann_vol if ann_vol > 0 else 0

            cm = d["price"].cummax()

            mdd = ((d["price"] - cm) / cm).min()

            rows.append({

                "Instrument": name,

                "Period Return": f"{d['price'].iloc[-1] / d['price'].iloc[0] - 1:+.2%}",

                "Ann. Volatility": f"{ann_vol:.2%}",

                "Sharpe": f"{sharpe_p:.2f}",

                "Max Drawdown": f"{mdd:.2%}",

                "RSI (14)": f"{d['rsi'].iloc[-1]:.1f}" if pd.notna(d["rsi"].iloc[-1]) else "N/A",

            })

        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)



        st.download_button(

            ":inbox_tray: Download portfolio summary (CSV)",

            data=pd.DataFrame(rows).to_csv(index=False).encode("utf-8"),

            file_name="portfolio_summary.csv",

            mime="text/csv",

        )



# ---------------------------------------------------------------------------

# TAB — TOP MOVERS

# ---------------------------------------------------------------------------

with tab_movers:

    st.markdown(f"**TOP MOVERS — {primary_name.upper()} · LAST 10 BARS**")

    last10 = df.tail(10).copy().sort_values("return", ascending=False)

    for date, row in last10.iterrows():

        color = GREEN_UP if row["return"] >= 0 else RED_DOWN

        sign = "+" if row["return"] >= 0 else ""

        st.markdown(

            f"<div class='ledger-row'>"

            f"<b>{pd.Timestamp(str(date)).strftime('%d %b %Y')}</b><br>"

            f"<span style='color:{INK_MUTED}'>{row['price']:,.2f}</span> "

            f"<span style='color:{color}; float:right; font-weight:700;'>{sign}{row['return']:.2%}</span></div>",

            unsafe_allow_html=True,

        )



# ---------------------------------------------------------------------------

# TAB — HEATMAP

# ---------------------------------------------------------------------------

with tab_heatmap:

    st.markdown(f"**MONTHLY RETURNS HEATMAP — {primary_name.upper()}**")

    d = df.copy()

    d["year"] = pd.DatetimeIndex(d.index).year

    d["month"] = pd.DatetimeIndex(d.index).month

    monthly = d.groupby(["year", "month"])["price"].agg(["first", "last"])

    monthly["ret"] = monthly["last"] / monthly["first"] - 1

    pivot = monthly["ret"].unstack("month")

    fig3 = go.Figure(

        data=go.Heatmap(

            z=pivot.values,

            x=[f"M{m}" for m in pivot.columns],

            y=[str(y) for y in pivot.index],

            colorscale=[[0, RED_DOWN], [0.5, PANEL], [1, GREEN_UP]],

            zmid=0,

            text=[[f"{v:.1%}" if pd.notna(v) else "" for v in row] for row in pivot.values],

            texttemplate="%{text}",

            showscale=False,

        )

    )

    fig3.update_layout(

        paper_bgcolor=PAPER, plot_bgcolor=PANEL, font_color=INK, height=320,

        margin=dict(t=10, b=10, l=10, r=10),

    )

    st.plotly_chart(fig3, width="stretch")



# ---------------------------------------------------------------------------

# TAB — STRATEGY BUILDER

# ---------------------------------------------------------------------------

with tab_strategy:

    st.markdown(f"**STRATEGY BUILDER — {primary_name.upper()}**")

    st.caption(

        "Combine signals to build a rule-based long/flat strategy, backtested on the primary "

        "instrument. AND requires every active signal to agree; OR triggers long if any agree."

    )



    signal_choices = st.multiselect(

        "Signals to include", ["Moving Average Crossover", "RSI", "Bollinger Bands"],

        default=["Moving Average Crossover"], key="sb_signals",

    )

    combine_logic = st.radio("Combine logic", ["AND (all must agree)", "OR (any may trigger)"],

                              horizontal=True, key="sb_logic")



    strat = df[["price"]].copy()

    container = st.container()

    strat, signal_cols = run_signals(strat, signal_choices, "sb", container)



    if not signal_cols:

        st.info("Pick at least one signal above to build a strategy.")

    else:

        strat = backtest(strat, signal_cols, combine_logic)

        stats = strategy_stats(strat)



        m1, m2, m3, m4, m5 = st.columns(5)

        m1.metric("Strategy Return", f"{stats['strategy_return']:+.2%}")

        m2.metric("Buy & Hold Return", f"{stats['buyhold_return']:+.2%}")

        m3.metric("Strategy Sharpe", f"{stats['sharpe']:.2f}")

        m4.metric("Max Drawdown", f"{stats['max_drawdown']:.2%}")

        m5.metric("Trades Taken", f"{stats['n_trades']}")



        st.markdown("**EQUITY CURVE — STRATEGY vs BUY & HOLD**")

        fig4 = go.Figure()

        fig4.add_trace(go.Scatter(x=strat.index, y=strat["strategy_equity"], mode="lines",

                                   name="Strategy", line=dict(color=PISTACHIO_DEEP, width=2)))

        fig4.add_trace(go.Scatter(x=strat.index, y=strat["buyhold_equity"], mode="lines",

                                   name="Buy & Hold", line=dict(color=MAROON, width=2, dash="dot")))

        fig4.update_layout(

            paper_bgcolor=PAPER, plot_bgcolor=PANEL, font_color=INK, height=340,

            margin=dict(t=10, b=10, l=10, r=10),

            xaxis=dict(gridcolor=LINE), yaxis=dict(gridcolor=LINE, title="Growth of ₹1"),

            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),

        )

        st.plotly_chart(fig4, width="stretch")



        st.markdown("**PRICE WITH ENTRY / EXIT MARKERS**")

        entries = strat[stats["trades"] == 1]

        exits = strat[stats["trades"] == -1]

        fig5 = go.Figure()

        fig5.add_trace(go.Scatter(x=strat.index, y=strat["price"], mode="lines", name="Price",

                                   line=dict(color=INK_MUTED, width=1.3)))

        fig5.add_trace(go.Scatter(x=entries.index, y=entries["price"], mode="markers", name="Entry",

                                   marker=dict(color=GREEN_UP, size=9, symbol="triangle-up")))

        fig5.add_trace(go.Scatter(x=exits.index, y=exits["price"], mode="markers", name="Exit",

                                   marker=dict(color=MAROON, size=9, symbol="triangle-down")))

        fig5.update_layout(

            paper_bgcolor=PAPER, plot_bgcolor=PANEL, font_color=INK, height=320,

            margin=dict(t=10, b=10, l=10, r=10),

            xaxis=dict(gridcolor=LINE), yaxis=dict(gridcolor=LINE),

            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),

        )

        st.plotly_chart(fig5, width="stretch")



        st.download_button(

            ":inbox_tray: Download strategy backtest (CSV)",

            data=strat.to_csv().encode("utf-8"),

            file_name=f"{primary_ticker.replace('^', '')}_strategy_backtest.csv",

            mime="text/csv",

        )



        st.caption(

            "Backtest is signal-only: no transaction costs, slippage, or position sizing. "

            "Positions are entered the bar after a signal fires to avoid look-ahead bias. Not investment advice."

        )



# ---------------------------------------------------------------------------

# TAB — COMPARE STRATEGIES

# ---------------------------------------------------------------------------

with tab_compare:

    st.markdown(f"**COMPARE TWO STRATEGIES — {primary_name.upper()}**")

    st.caption("Configure Strategy A and Strategy B independently and compare their equity curves.")



    colA, colB = st.columns(2)



    with colA:

        st.markdown("#### Strategy A")

        sig_a = st.multiselect("Signals (A)", ["Moving Average Crossover", "RSI", "Bollinger Bands"],

                                default=["Moving Average Crossover"], key="cmp_a_signals")

        logic_a = st.radio("Logic (A)", ["AND (all must agree)", "OR (any may trigger)"], key="cmp_a_logic")

        strat_a = df[["price"]].copy()

        strat_a, cols_a = run_signals(strat_a, sig_a, "cmpA", st.container())



    with colB:

        st.markdown("#### Strategy B")

        sig_b = st.multiselect("Signals (B)", ["Moving Average Crossover", "RSI", "Bollinger Bands"],

                                default=["RSI"], key="cmp_b_signals")

        logic_b = st.radio("Logic (B)", ["AND (all must agree)", "OR (any may trigger)"], key="cmp_b_logic")

        strat_b = df[["price"]].copy()

        strat_b, cols_b = run_signals(strat_b, sig_b, "cmpB", st.container())



    if not cols_a or not cols_b:

        st.info("Pick at least one signal for both Strategy A and Strategy B.")

    else:

        strat_a = backtest(strat_a, cols_a, logic_a)

        strat_b = backtest(strat_b, cols_b, logic_b)

        stats_a = strategy_stats(strat_a)

        stats_b = strategy_stats(strat_b)



        comp_df = pd.DataFrame({

            "Metric": ["Total Return", "Sharpe", "Max Drawdown", "Trades"],

            "Strategy A": [f"{stats_a['strategy_return']:+.2%}", f"{stats_a['sharpe']:.2f}",

                          f"{stats_a['max_drawdown']:.2%}", str(stats_a["n_trades"])],

            "Strategy B": [f"{stats_b['strategy_return']:+.2%}", f"{stats_b['sharpe']:.2f}",

                          f"{stats_b['max_drawdown']:.2%}", str(stats_b["n_trades"])],

            "Buy & Hold": [f"{stats_a['buyhold_return']:+.2%}", "—", "—", "—"],

        })

        st.dataframe(comp_df, width="stretch", hide_index=True)



        st.markdown("**EQUITY CURVES — A vs B vs BUY & HOLD**")

        fig6 = go.Figure()

        fig6.add_trace(go.Scatter(x=strat_a.index, y=strat_a["strategy_equity"], mode="lines",

                                   name="Strategy A", line=dict(color=PISTACHIO_DEEP, width=2)))

        fig6.add_trace(go.Scatter(x=strat_b.index, y=strat_b["strategy_equity"], mode="lines",

                                   name="Strategy B", line=dict(color=MAROON, width=2)))

        fig6.add_trace(go.Scatter(x=strat_a.index, y=strat_a["buyhold_equity"], mode="lines",

                                   name="Buy & Hold", line=dict(color=INK_MUTED, width=1.5, dash="dot")))

        fig6.update_layout(

            paper_bgcolor=PAPER, plot_bgcolor=PANEL, font_color=INK, height=380,

            margin=dict(t=10, b=10, l=10, r=10),

            xaxis=dict(gridcolor=LINE), yaxis=dict(gridcolor=LINE, title="Growth of ₹1"),

            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),

        )

        st.plotly_chart(fig6, width="stretch")



        st.caption(

            "Both backtests are signal-only: no transaction costs, slippage, or position sizing. "

            "Not investment advice."

        )



