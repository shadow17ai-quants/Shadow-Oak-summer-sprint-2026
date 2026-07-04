# Sunday Journal – Week 2 (2 July 2026)

**Ryan Kaushal** – Shadow Oak Capitals Summer Sprint  
**Week 2:** 28 June – 2 July 2026

---

## 1. What did I build this week that did not exist last Sunday?

Last Sunday, I had Python fundamentals and a finance tracker. This week, I built:

- ✅ A complete Pandas and NumPy foundation (`pandas_demo.py`, `numpy_demo.py`)
- ✅ A yfinance test script that downloads real Nifty 50 data
- ✅ NifftyVault – a full quant data pipeline:
  - `downloader.py` – downloads 5 years of Nifty data
  - `analyzer.py` – computes Sharpe ratio, max drawdown, annualised return, volatility
  - `visualize.py` – creates price charts
  - `nifty_metrics.txt` – metrics summary
- ✅ Manual verification – proved my code matches hand calculations within 0.001

**What didn't exist last Sunday:** A working quant data pipeline with real market data, Sharpe ratio, and max drawdown.

---

## 2. What is the weakest part of my current code or methodology?

**The weakest part is still understanding the math behind the metrics.**

I can compute Sharpe ratio, but I don't fully internalise what 0.73 Sharpe means in real trading terms. I also haven't yet built a testing suite – no pytest, no validation beyond manual verification.

**Methodology weakness:** I'm still copying patterns from tutorials without always questioning *why* certain functions exist. I need to slow down and build deeper intuition.

---

## 3. What would a sceptic at Man Group say about my backtests?

**"You don't have a backtest yet."**

I have a data pipeline and metrics, but no event‑driven backtest. I haven't tested any strategy. I haven't proven I can avoid lookahead bias. I haven't built the full backtesting engine.

The sceptic would say:
- "Show me your backtest with transaction costs."
- "Prove you didn't use future data."
- "Show me the out‑of‑sample performance."

**That's coming in Phase 2.** This week was about data. Next week is about SQL. The week after is about backtesting.

---

## 4. What does my father think I am missing?

**He would say: "When do you start trading real money?"**

He's practical. He invests. He'd want to see:
- "Is this data clean enough to trade on?"
- "What's your first signal going to be?"
- "Are you logging paper trades yet?"

**The gap:** I have market data, but no trading decisions yet. No signal generation. No paper trade log. That's coming in Phase 2.

---

## 5. What did I do this week that was dishonest – with data, results, or myself?

**I was dishonest about how much time I spent debugging.**

I told myself I "finished quickly" – but I spent hours fixing yfinance column errors, file path issues, and CSV locations. I rationalised it as "learning" – which is true – but I didn't budget enough time for it.

**The fix:** Next week, I'll block out 1 extra hour per day for debugging and error resolution. No more "it'll work first time" assumptions.

---

## 6. What is the next thing that could kill this project, and what is my response?

**The next killer is PostgreSQL setup.**

I need to install, configure, and connect PostgreSQL. Then write SQL queries. Then migrate the finance tracker from SQLite to PostgreSQL.

**This is where many people quit** – because installing databases is boring and frustrating.

**My response:**
1. Watch the freeCodeCamp SQL course (3 hours) – no shortcuts.
2. Follow the Socratica psycopg2 series step‑by‑step.
3. Break it into micro‑tasks – just like I did with Pandas.
4. Ask for help immediately if I hit a blocker – no more "I'll figure it out later."

---

## 7. What is the one thing I would most regret not doing this week?

**I would regret not building NifftyVault.**

I almost pushed it to Week 3 because "Pandas is hard." But I started it anyway – and it worked. The data is clean, the metrics are calculated, and the manual verification is done.

**The lesson:** Start before you're ready. The code will teach you what you need to know.

**The regret I avoided:** Having a Week 2 where I "learned Pandas" but built nothing tangible. Instead, I have a production‑ready data pipeline with real market data.

---

## Final Reflection

Week 2 was about moving from "learning Python" to "building quant tools."

**My commitment:**
- ✅ Daily Git commits.
- ✅ Sunday journals.
- ✅ No more catch‑up marathons – daily progress.
- ✅ Complete NifftyVault – data pipeline with Sharpe and drawdown.

**Week 3 is about SQL and PostgreSQL – the permanent storage layer of the fund.**

---

**Signed:**  
Ryan Kaushal  
2 July 2026