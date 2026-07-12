# projects/nifftyvault/visualize.py
# Visualise Nifty 50 price history

import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv("nifty_50_data.csv", index_col=0, parse_dates=True)

# Plot adjusted close
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Adj Close"], label="Nifty 50", color="#1f77b4")
plt.title("Nifty 50 – 5 Year Price History")
plt.xlabel("Date")
plt.ylabel("Price (₹)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("nifty_50_price_chart.png", dpi=150)
print("✅ Chart saved as nifty_50_price_chart.png")
