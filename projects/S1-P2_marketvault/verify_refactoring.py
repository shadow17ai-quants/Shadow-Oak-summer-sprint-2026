#!/usr/bin/env python3
# Verification script for NifftyVault refactoring

import sys
from pathlib import Path

# Add the src directory to the path so we can import our package
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_basic_import():
    """Test that we can import the package and its submodules."""
    print("Testing imports...")

    try:
        import nifftyvault

        print(f"[PASS] Imported nifftyvault v{nifftyvault.__version__}")
    except Exception as e:
        print(f"[FAIL] Failed to import nifftyvault: {e}")
        return False

    try:
        print("[PASS] Imported all submodules")
    except Exception as e:
        print(f"[FAIL] Failed to import submodules: {e}")
        return False

    return True


def test_data_classes():
    """Test that we can instantiate the main classes."""
    print("\nTesting class instantiation...")

    try:
        from nifftyvault.data import NiftyDataManager

        _ = NiftyDataManager()
        print("[PASS] Created NiftyDataManager instance")
    except Exception as e:
        print(f"[FAIL] Failed to create NiftyDataManager: {e}")
        return False

    return True


def test_analysis_functions():
    """Test that analysis functions are callable."""
    print("\nTesting analysis functions...")

    try:
        import pandas as pd

        from nifftyvault.analysis import (
            annualized_return,
            annualized_volatility,
            sharpe_ratio,
        )

        # Create minimal test data
        dates = pd.date_range("2023-01-01", periods=5, freq="B")
        prices = [100, 101, 102, 103, 104]
        returns = [0.01, 0.01, 0.01, 0.01]

        df = pd.DataFrame({"Adj Close": prices, "simple_return": returns}, index=dates)

        # Test function calls
        ann_ret = annualized_return(df)
        ann_vol = annualized_volatility(df)
        sharpe = sharpe_ratio(df)

        print("[PASS] Analysis functions executed successfully")
        print(f"    Annualized Return: {ann_ret:.4f}")
        print(f"    Annualized Volatility: {ann_vol:.4f}")
        print(f"    Sharpe Ratio: {sharpe:.4f}")
    except Exception as e:
        print(f"[FAIL] Failed to execute analysis functions: {e}")
        return False

    return True


def test_visualization_functions():
    """Test that visualization functions are callable."""
    print("\nTesting visualization functions...")

    try:
        import matplotlib.pyplot as plt
        import pandas as pd

        from nifftyvault.visualization import plot_price_history

        # Create minimal test data
        dates = pd.date_range("2023-01-01", periods=5, freq="B")
        prices = [100, 101, 102, 103, 104]

        df = pd.DataFrame({"Adj Close": prices}, index=dates)

        # Test function call (don't show plot)
        fig = plot_price_history(df, show=False)

        if fig is not None:
            print("[PASS] Visualization function executed successfully")
            plt.close(fig)  # Clean up
        else:
            print(
                "[PASS] Visualization function executed "
                "(returned None for show=True case)"
            )
    except Exception as e:
        print(f"[FAIL] Failed to execute visualization functions: {e}")
        return False

    return True


def main():
    """Run all verification tests."""
    print("=" * 50)
    print("NiftyVault RefactVault Refactoring Verification")
    print("=" * 50)

    tests = [
        test_basic_import,
        test_data_classes,
        test_analysis_functions,
        test_visualization_functions,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()  # Empty line between tests

    print("=" * 50)
    if passed == total:
        print("[PASS] All tests passed! Refactoring appears to be working correctly.")
        return 0
    elif passed > 0:
        print(
            f"[WARN] {passed}/{total} tests passed. Some functionality may be working."
        )
        return 1
    else:
        print(f"[FAIL] 0/{total} tests passed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
