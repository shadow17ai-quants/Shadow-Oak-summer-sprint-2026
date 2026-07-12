"""
Tests for the data module.
"""

from pathlib import Path

from nifftyvault.data import DEFAULT_DATA_FILE, NiftyDataManager


def test_nifty_data_manager_init():
    manager = NiftyDataManager()
    assert manager.ticker == "^NSEI"
    assert manager.data_file == Path(DEFAULT_DATA_FILE)


def test_custom_init():
    custom_path = Path("./custom_data.csv")
    manager = NiftyDataManager(data_file=custom_path, ticker="RELIANCE.NS")
    assert manager.ticker == "RELIANCE.NS"
    assert manager.data_file == custom_path
