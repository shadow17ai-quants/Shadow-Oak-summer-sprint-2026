# Sunday Journal – Week 1 (25 June 2026)

**Ryan Kaushal** – Shadow Oak Capitals Summer Sprint  
**Week 1:** 19 June – 25 June 2026

---

## 1. What did I build this week that did not exist last Sunday?

Last Sunday (14 June), I had never written a line of Python. Today, I have:

- ✅ A working `calculator.py` that handles user input and arithmetic.
- ✅ A fully functional `RPS_game.py` (Rock-Paper-Scissors) with loops and conditionals.
- ✅ A `list_analyzer.py` that takes 5 numbers, computes stats, removes duplicates, and uses tuple unpacking.
- ✅ An `emoji_converter.py` that maps text emoticons to actual emojis using dictionaries and functions.
- ✅ A `personal_finance_tracker.py` with:
  - SQLite database
  - CLI to add income/expense
  - View all transactions
  - PDF report with bar chart and cumulative balance (Matplotlib)
- ✅ Understanding of: lists, tuples, dictionaries, functions (`*args`, `**kwargs`), exceptions, and OOP (classes, classmethods, staticmethods).

This is a complete Python foundation. It didn't exist 7 days ago.

---

## 2. What is the weakest part of my current code or methodology?

**The weakest part is my error handling and input validation.**

While my code works for valid inputs, I haven't been rigorous enough about:
- Handling invalid input gracefully (e.g., user enters text when a number is expected).
- Edge cases like empty databases, missing files, or duplicate entries.
- Writing unit tests – I have zero tests right now.

**Methodology weakness:** I'm still typing code from tutorials without always stopping to ask "Why does this work?" before moving on. I need to slow down and internalize concepts, not just copy.

---

## 3. What would a sceptic at Man Group say about my backtests?

**"You don't have any backtests yet."**

That's the honest answer. Right now, I'm building the Python toolkit. The sceptic would say:
- "Show me your data pipeline."
- "Prove your Sharpe calculation is correct."
- "Where is your no-lookahead test?"

All valid. I need to finish Week 1's foundation, then Week 2–3 will prove the quant engine works. The sceptic is right to be sceptical – I have nothing to show yet except basic Python skills.

**But that changes next week.** S1‑P2 (Nifty 50 data downloader, Sharpe, drawdown) is where I start proving financial competency.

---

## 4. What does my father think I am missing?

**He would ask: "Where is the real money? When do you trade?"**

My father is practical. He invests in the share market. He'd want to know:
- "Is this code actually making decisions, or is it just education?"
- "What's your first trade going to be?"
- "Are you logging paper trades yet?"

He's right to push. I need to:
1. Complete S1‑P3 (Trading Journal – 30 paper trades with reasoning).
2. Get the PostgreSQL trade_log schema live.
3. Show that I'm practising discipline *before* real money is at stake.

**The gap:** I'm learning Python, but I haven't yet connected it to real trading decisions. That happens in Weeks 2–4.

---

## 5. What did I do this week that was dishonest – with data, results, or myself?

**I was dishonest about my time commitment.**

I let Days 3–6 slip by without starting them. I told myself I'd "catch up" – which I did today – but that catch‑up required a 6‑hour marathon session that wasn't sustainable.

**The dishonesty:** I rationalised the delay instead of admitting I was procrastinating. I said "I'll do it tomorrow" and then didn't.

**The fix:** From Week 2 onward, I commit to:
- Daily progress, even if it's just 1 hour.
- No more "I'll catch up on the weekend."
- The Sunday journal is non‑negotiable. I wrote it. I'll keep writing it.

---

## 6. What is the next thing that could kill this project, and what is my response?

**The next killer is the "data valley" – Weeks 2–4.**

I'll have to:
- Install and configure PostgreSQL.
- Learn Pandas, NumPy, and yfinance from scratch.
- Build the data pipeline for Nifty 50 data.

**This is where most beginners quit.** The learning curve steepens. The tutorials get longer. The code gets more complex.

**My response:**
1. Break every day into micro‑tasks (just like I did today).
2. Commit after every micro‑task – even if it's "pandas_demo.py runs without errors."
3. Ask for help immediately if I hit a blocker – no more "I'll figure it out later."
4. Keep the "Shadow Oak" goal in mind: Edge, Proof, Trust, Capital. Every line of code is a brick in that wall.

---

## 7. What is the one thing I would most regret not doing this week?

**I would regret not starting S1‑P1 (Finance Tracker).**

I almost pushed it to Week 2 because "I needed to learn OOP first." But I started it anyway – and it worked. The SQLite schema is live, the CLI works, and the PDF report generates.

**The lesson:** Start before you're ready. The code will teach you what you need to know.

**The regret I avoided:** I would have regretted having a "Week 1" where I built nothing tangible. Instead, I have 6 working projects. That's real momentum.

---

## Final Reflection

Week 1 was about proving I can learn. Week 2 must be about proving I can apply.

**My commitment:**
- ✅ Daily Git commits.
- ✅ Sunday journals.
- ✅ No more catch‑up marathons – daily progress.
- ✅ Begin S1‑P2 (Nifty 50 Sharpe) by 27 June.

The sprint is 91 days. Week 1 is done. Week 2 starts now.

---

**Signed:**  
Ryan Kaushal  
25 June 2026