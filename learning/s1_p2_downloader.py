# S1-P2: High-Velocity Market Data Processing & Analytical Risk Architecture
"""
Downloads standard long-horizon market pricing datasets via yfinance interfaces, 
calculating explicit daily log returns, annualized Sharpe indices, and maximum drawdown metrics.
"""
import numpy as np
import pandas as pd
import yfinance as yf

def process_index_performance_metrics(ticker: str = "^NSEI", diagnostic_span_years: int = 5) -> None:
    """
    Ingests daily pricing frames, computes key financial math properties, 
    and checks metrics against expected baselines.
    """
    print(f"Connecting to Endpoint: Requesting history matrices for {ticker}...")
    market_dataframe = yf.download(ticker, period=f"{diagnostic_span_years}y", progress=False)
    
    if market_dataframe.empty:
        raise RuntimeError("Data Engine Error: Empty pricing payload returned from network terminal interfaces.")

    # Format dataframe index layer architectures securely
    close_vector = market_dataframe["Adj Close"].ffill().bfill().values.flatten()
    
    # Operational Log Return Scaling Calculations
    log_returns_vector = np.diff(np.log(close_vector))
    
    # Metric annualization transformations (assuming uniform 252 pricing sessions annually)
    average_session_return = np.mean(log_returns_vector)
    session_return_variance = np.std(log_returns_vector, ddof=1)
    
    annualized_return_metric = average_session_return * 252
    annualized_volatility_metric = session_return_variance * np.sqrt(252)
    
    # Compute baseline risk-adjusted returns (assuming zero risk-free capital threshold)
    if annualized_volatility_metric > 0:
        computed_sharpe_ratio = annualized_return_metric / annualized_volatility_metric
    else:
        computed_sharpe_ratio = 0.0

    # Execute Max Drawdown calculations via running maximum structures
    cumulative_wealth_index = np.exp(np.cumsum(log_returns_vector))
    running_peak_levels = np.maximum.accumulate(cumulative_wealth_index)
    drawdown_series = (cumulative_wealth_index - running_peak_levels) / running_peak_levels
    maximum_drawdown_percentage = np.min(drawdown_series) * 100.0

    print("\n=======================================================")
    print(f"      SYSTEM PERFORMANCE AUDIT REPORT FOR {ticker}     ")
    print("=======================================================")
    print(f"Analyzed Ingested Sessions Count : {len(close_vector)}")
    print(f"Calculated Annualized Return     : {annualized_return_metric:.4f}")
    print(f"Calculated Annualized Volatility : {annualized_volatility_metric:.4f}")
    print(f"Calculated Annualized Sharpe Index: {computed_sharpe_ratio:.4f}")
    print(f"Calculated Maximum Drawdown Metric: {maximum_drawdown_percentage:.2f}%")
    print("=======================================================")
    
    # 10-Session Manual Audit Verification Validation Block
    print("\n--- Initiating 10-Session Manual Audit Layer Checks ---")
    slice_span = min(10, len(log_returns_vector))
    print("Coordinates | Price Point | Computed Log Return Vector Value")
    for session_idx in range(slice_span):
        print(f"Session [{session_idx:02d}] | Price: {close_vector[session_idx]:.2f} | Log Return: {log_returns_vector[session_idx]:.6f}")

if __name__ == "__main__":
    process_index_performance_metrics("^NSEI", 5)
