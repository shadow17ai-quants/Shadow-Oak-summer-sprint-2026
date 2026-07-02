# projects/nifftyvault/analyzer.py
# NifftyVault – Sharpe Ratio & Max Drawdown Calculator

import pandas as pd
import numpy as np

def load_data(filename="nifty_50_data.csv"):
    """Load the CSV data and drop NaN rows."""
    df = pd.read_csv(filename, index_col=0, parse_dates=True)
    df = df.dropna()  # Remove first row with NaN return
    return df

def annualized_return(df, column="simple_return"):
    """Compute annualized return from daily returns."""
    daily_mean = df[column].mean()
    trading_days = 252  # approximate
    annual_ret = (1 + daily_mean) ** trading_days - 1
    return annual_ret

def annualized_volatility(df, column="simple_return"):
    """Compute annualized volatility from daily returns."""
    daily_std = df[column].std()
    trading_days = 252
    annual_vol = daily_std * np.sqrt(trading_days)
    return annual_vol

def sharpe_ratio(df, risk_free_rate=0.0, column="simple_return"):
    """Compute annualized Sharpe ratio."""
    ann_ret = annualized_return(df, column)
    ann_vol = annualized_volatility(df, column)
    sharpe = (ann_ret - risk_free_rate) / ann_vol
    return sharpe

def max_drawdown(df, price_column="Adj Close"):
    """Compute maximum drawdown from price series."""
    # Compute cumulative max
    cumulative_max = df[price_column].cummax()
    # Drawdown = (current - cumulative_max) / cumulative_max
    drawdown = (df[price_column] - cumulative_max) / cumulative_max
    max_dd = drawdown.min()  # most negative value
    return max_dd

def main():
    print("===== NIFTYVAULT: METRICS CALCULATOR =====")
    
    # Load data
    df = load_data()
    print(f"Loaded {len(df)} days of data (after dropping NaN)")
    
    # Compute metrics
    ann_ret = annualized_return(df)
    ann_vol = annualized_volatility(df)
    sharpe = sharpe_ratio(df)
    max_dd = max_drawdown(df)
    
    print("\n===== RESULTS =====")
    print(f"Annualized Return:       {ann_ret:.4%}")
    print(f"Annualized Volatility:   {ann_vol:.4%}")
    print(f"Sharpe Ratio (0% RFR):   {sharpe:.4f}")
    print(f"Maximum Drawdown:        {max_dd:.4%}")
    
    # Also compute with log returns for comparison
    ann_ret_log = annualized_return(df, "log_return")
    ann_vol_log = annualized_volatility(df, "log_return")
    sharpe_log = sharpe_ratio(df, column="log_return")
    
    print("\n===== USING LOG RETURNS (for reference) =====")
    print(f"Annualized Return (log): {ann_ret_log:.4%}")
    print(f"Annualized Vol (log):    {ann_vol_log:.4%}")
    print(f"Sharpe Ratio (log):      {sharpe_log:.4f}")
    
    print("\n📊 Metrics saved to: nifty_metrics.txt")
    with open("nifty_metrics.txt", "w") as f:
        f.write("NifftyVault – Metrics Summary\n")
        f.write("==============================\n\n")
        f.write(f"Annualized Return (simple): {ann_ret:.4%}\n")
        f.write(f"Annualized Volatility:       {ann_vol:.4%}\n")
        f.write(f"Sharpe Ratio (0% RFR):       {sharpe:.4f}\n")
        f.write(f"Maximum Drawdown:            {max_dd:.4%}\n")

if __name__ == "__main__":
    main()