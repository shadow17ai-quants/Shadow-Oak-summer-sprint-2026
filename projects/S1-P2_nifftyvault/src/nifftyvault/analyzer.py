"""
Example script demonstrating NifftyVault usage.
Downloads data, computes metrics, and saves results.
"""

try:
    # When used as an installed package
    from nifftyvault.analysis import (
        annualized_return,
        annualized_volatility,
        load_data,
        max_drawdown,
        sharpe_ratio,
    )
    from nifftyvault.visualization import plot_price_history
except ImportError:
    # Fallback for running the file directly from the source checkout
    from .analysis import (
        annualized_return,
        annualized_volatility,
        load_data,
        max_drawdown,
        sharpe_ratio,
    )
    from .visualization import plot_price_history


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
    from .analysis import annualized_return as ann_ret_log_func
    from .analysis import annualized_volatility as ann_vol_log_func
    from .analysis import sharpe_ratio as sharpe_log_func

    ann_ret_log = ann_ret_log_func(df, column="log_return")
    ans_vol_log = ann_vol_log_func(df, column="log_return")
    sharpe_log = sharpe_log_func(df, column="log_return")

    print("\n===== USING LOG RETURNS (for reference) =====")
    print(f"Annualized Return (log): {ann_ret_log:.4%}")
    print(f"Annualized Vol (log):    {ans_vol_log:.4%}")
    print(f"Sharpe Ratio (log):      {sharpe_log:.4f}")

    print("\n📊 Metrics saved to: nifty_metrics.txt")
    with open("nifty_metrics.txt", "w") as f:
        f.write("NifftyVault – Metrics Summary\n")
        f.write("==============================\n\n")
        f.write(f"Annualized Return (simple): {ann_ret:.4%}\n")
        f.write(f"Annualized Volatility:       {ann_vol:.4%}\n")
        f.write(f"Sharpe Ratio (0% RFR):       {sharpe:.4f}\n")
        f.write(f"Maximum Drawdown:            {max_dd:.4%}\n")

    # Optional: plot and save price chart
    try:
        plot_price_history(df, save_path="nifty_50_price_chart.png")
        print("✅ Price chart saved as nifty_50_price_chart.png")
    except Exception as e:
        print(f"⚠️ Could not create plot: {e}")


if __name__ == "__main__":
    main()
