# language_python/yfinance_test.py
# Testing yfinance – download Nifty 50 data

import yfinance as yf
import pandas as pd

print("===== TESTING YFINANCE =====")

# Download Nifty 50 (^NSEI)
nifty = yf.download("^NSEI", start="2020-01-01", end="2026-06-28")

print(f"Data shape: {nifty.shape}")
print(f"Columns: {nifty.columns.tolist()}")
print("\nFirst 5 rows:")
print(nifty.head())
print("\nLast 5 rows:")
print(nifty.tail())