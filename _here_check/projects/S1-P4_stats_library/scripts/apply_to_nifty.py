"""
Applies the full quant_stats library to 5 years of Nifty 50 log returns.
Reads the CSV already downloaded by the S1-P2 nifftyvault project.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from quant_stats import full_report

NIFTY_CSV = (
    Path(__file__).parent.parent.parent
    / "S1-P2_nifftyvault"
    / "data"
    / "nifty_50_data.csv"
)


def main():
    if not NIFTY_CSV.exists():
        print(f"Could not find {NIFTY_CSV}")
        print("Run the S1-P2 nifftyvault downloader first.")
        return

    df = pd.read_csv(NIFTY_CSV, index_col=0, parse_dates=True)
    price_col = "Adj Close" if "Adj Close" in df.columns else "Close"
    log_returns = np.log(df[price_col] / df[price_col].shift(1)).dropna().values

    print(
        f"Loaded {len(df)} rows, {len(log_returns)} log returns from {NIFTY_CSV.name}"
    )
    print("=" * 70)

    report = full_report(log_returns)

    print("\n--- RATIOS ---")
    for name in [
        "sharpe_ratio",
        "sortino_ratio",
        "calmar_ratio",
        "omega_ratio",
        "max_drawdown",
    ]:
        print(f"\n{name}:")
        for k, v in report[name].items():
            print(f"  {k}: {v}")

    print("\n--- HYPOTHESIS TESTS ---")
    for name in [
        "jarque_bera_test",
        "shapiro_wilk_test",
        "ljung_box_test",
        "adf_test",
        "fit_student_t",
    ]:
        print(f"\n{name}:")
        for k, v in report[name].items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
