# projects/nifftyvault/downloader.py
# NifftyVault – Nifty 50 Data Downloader (FAST VERSION)

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import yfinance as yf


def download_nifty_50():
    """Download 5 years of Nifty 50 data from yfinance (with threads=False)."""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5 * 365)

    print(f"Downloading Nifty 50 data from {start_date.date()} to {end_date.date()}")

    # Use threads=False for faster download on Windows
    df = yf.download(
        "^NSEI",
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=True,  # Show progress bar so you know it's working
        threads=False,  # Fix for Windows/Anaconda
        timeout=30,  # Timeout after 30 seconds
    )

    if df.empty:
        raise ValueError(
            "No data downloaded. Check your internet connection or ticker symbol."
        )

    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    return df


def compute_log_returns(df):
    """Compute daily log returns from adjusted close prices."""
    df["log_return"] = np.log(df["Adj Close"] / df["Adj Close"].shift(1))
    return df


def compute_simple_returns(df):
    """Compute daily simple returns from adjusted close prices."""
    df["simple_return"] = df["Adj Close"].pct_change()
    return df


def save_data(df, filename="nifty_50_data.csv"):
    """Save the DataFrame to CSV."""
    df.to_csv(filename)
    print(f"Data saved to {filename}")
    return filename


def main():
    print("===== NIFTYVAULT: NIFTY 50 DATA DOWNLOADER =====")

    try:
        # Download data
        df = download_nifty_50()
        print(f"Downloaded {len(df)} rows of data")

        # Compute returns
        df = compute_log_returns(df)
        df = compute_simple_returns(df)

        # Show summary statistics
        print("\n===== SUMMARY STATISTICS =====")
        print(f"Period: {df.index.min()} to {df.index.max()}")
        print(f"Total days: {len(df)}")
        print(f"Mean log return: {df['log_return'].mean():.6f}")
        print(f"Std log return: {df['log_return'].std():.6f}")
        print(f"Mean simple return: {df['simple_return'].mean():.6f}")
        print(f"Std simple return: {df['simple_return'].std():.6f}")

        # Save data
        save_data(df)

        # Show first 5 rows
        print("\n===== FIRST 5 ROWS =====")
        print(df[["Adj Close", "log_return", "simple_return"]].head())

        return df

    except KeyboardInterrupt:
        print(
            "\n⚠️ Download interrupted by user. "
            "Try again with a stable internet connection."
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(
            'Try running with: python -c "import yfinance as yf; print(yf.__version__)"'
        )


if __name__ == "__main__":
    main()
