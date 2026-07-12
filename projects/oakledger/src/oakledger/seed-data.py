import sqlite3, random
from datetime import datetime, timedelta

DB_PATH = "projects/oakledger/trades.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT, instrument TEXT, side TEXT, quantity INTEGER, price REAL,
    reasoning_before TEXT, reasoning_after TEXT, result REAL, signal_used TEXT
)""")
c.execute("DELETE FROM trades")
instr = ["NIFTY", "RELIANCE", "HDFC", "INFY", "TCS"]
sides = ["BUY","SELL"]
reasons = ["Breakout","Oversold","Trend","Reversal","News"]
trades=[]
for _ in range(20):
    d=(datetime.today()-timedelta(days=random.randint(1,90))).strftime("%Y-%m-%d")
    ins=random.choice(instr); side=random.choice(sides); qty=random.randint(1,5)
    price=round(random.uniform(100,5000),2)
    reason=random.choice(reasons)
    result=round(random.uniform(-200,300),2)
    signal=random.choice(["Momentum","MeanRev","Carry"])
    trades.append((d,ins,side,qty,price,reason,"Closed",result,signal))
c.executemany("INSERT INTO trades (trade_date,instrument,side,quantity,price,reasoning_before,reasoning_after,result,signal_used) VALUES (?,?,?,?,?,?,?,?,?)", trades)
conn.commit()
conn.close()
print(f"Inserted {len(trades)} trades")