"""
Data module for NifftyVault.
Handles downloading, storing, and retrieving market data.
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import yfinance as yf

from .config import (
    DEFAULT_DATA_FILE,
    DEFAULT_PERIOD_YEARS,
    DEFAULT_TICKER,
)

# Configure logger
logger = logging.getLogger(__name__)


class DataError(Exception):
    """Custom exception for data-related errors."""

    pass


class NiftyDataManager:
    """Manages Nifty 50 data download and storage."""

    def __init__(
        self,
        data_file: Union[str, Path] = DEFAULT_DATA_FILE,
        ticker: str = DEFAULT_TICKER,
    ):
        """
        Initialize the data manager.

        Args:
            data_file: Path to store/load the CSV data file
            ticker: Stock ticker symbol (default: ^NSEI for Nifty 50)
        """
        self.data_file = Path(data_file)
        self.ticker = ticker.upper()
        self._data: Optional[pd.DataFrame] = None

        # Ensure data directory exists
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(
            f"NiftyDataManager initialized with ticker={self.ticker}, "
            f"data_file={self.data_file}"
        )

    def download_data(
        self, period_years: int = DEFAULT_PERIOD_YEARS, force_download: bool = False
    ) -> pd.DataFrame:
        """
        Download Nifty 50 data from yfinance.

        Args:
            period_years: Number of years of historical data to download
            force_download: If True, download even if file exists

        Returns:
            pandas.DataFrame: Downloaded data with OHLCV columns

        Raises:
            DataError: If download fails or data is invalid
        """
        # Validate inputs
        if not isinstance(period_years, int) or period_years < 1:
            raise DataError(
                f"period_years must be a positive integer, got {period_years}"
            )

        # Check if we should skip download
        if self.data_file.exists() and not force_download:
            logger.info(f"Loading existing data from {self.data_file}")
            try:
                data = self.load_data()
                if not data.empty:
                    return data
                else:
                    logger.warning("Existing data file is empty, re-downloading")
            except Exception as e:
                logger.warning(f"Failed to load existing data: {e}, re-downloading")

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_years * 365)

        logger.info(
            f"Downloading {self.ticker} data from "
            f"{start_date.date()} to {end_date.date()}"
        )

        try:
            # Download data from yfinance
            data = yf.download(
                self.ticker,
                start=start_date,
                end=end_date,
                progress=False,  # Disable progress bar for programmatic use
                auto_adjust=False,  # Keep original OHLCV structure
                repair=False,
                timeout=30,
            )

            if data.empty:
                raise DataError(f"No data downloaded for ticker {self.ticker}")

            # Handle MultiIndex columns if present
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.droplevel(1)

            # Ensure we have the required columns
            required_columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
            missing_columns = [
                col for col in required_columns if col not in data.columns
            ]
            if missing_columns:
                raise DataError(f"Missing required columns: {missing_columns}")

            # Save to CSV
            self.save_data(data)
            self._data = data

            logger.info(
                f"Successfully downloaded {len(data)} rows of {self.ticker} data"
            )
            return data

        except Exception as e:
            logger.error(f"Failed to download data for {self.ticker}: {e}")
            raise DataError(f"Data download failed: {e}") from e

    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV file.

        Returns:
            pandas.DataFrame: Loaded data

        Raises:
            DataError: If file doesn't exist or is invalid
        """
        if not self.data_file.exists():
            raise DataError(f"Data file not found: {self.data_file}")

        try:
            data = pd.read_csv(self.data_file, index_col=0, parse_dates=True)

            if data.empty:
                raise DataError("Loaded data is empty")

            # Ensure datetime index
            if not isinstance(data.index, pd.DatetimeIndex):
                data = data.copy()
                data.index = pd.to_datetime(data.index)

            logger.info(f"Loaded {len(data)} rows from {self.data_file}")
            return data

        except Exception as e:
            logger.error(f"Failed to load data from {self.data_file}: {e}")
            raise DataError(f"Data loading failed: {e}") from e

    def save_data(self, data: pd.DataFrame) -> None:
        """
        Save data to CSV file.

        Args:
            data: DataFrame to save

        Raises:
            DataError: If save operation fails
        """
        if data is None or data.empty:
            raise DataError("Cannot save empty or None data")

        try:
            # Ensure directory exists
            self.data_file.parent.mkdir(parents=True, exist_ok=True)

            # Save to CSV
            data.to_csv(self.data_file)
            logger.info(f"Saved {len(data)} rows to {self.data_file}")

        except Exception as e:
            logger.error(f"Failed to save data to {self.data_file}: {e}")
            raise DataError(f"Data saving failed: {e}") from e

    def get_data(self, force_refresh: bool = False) -> pd.DataFrame:
        """
        Get the data, downloading if necessary.

        Args:
            force_refresh: If True, force re-download even if cached

        Returns:
            pandas.DataFrame: The data
        """
        if self._data is None or force_refresh:
            self._data = self.download_data(force_download=force_refresh)
        return self._data.copy()  # Return a copy to prevent accidental modification

    @property
    def data(self) -> Optional[pd.DataFrame]:
        """Get the cached data (may be None if not loaded)."""
        return self._data.copy() if self._data is not None else None


# Convenience function for backward compatibility
def download_nifty_50(
    period_years: int = DEFAULT_PERIOD_YEARS, force_download: bool = False
) -> pd.DataFrame:
    """
    Convenience function to download Nifty 50 data.

    Args:
        period_years: Number of years of historical data
        force_download: Force re-download even if file exists

    Returns:
        pandas.DataFrame: Downloaded data
    """
    manager = NiftyDataManager()
    return manager.download_data(
        period_years=period_years, force_download=force_download
    )


def load_nifty_50_data(data_file: Union[str, Path] = DEFAULT_DATA_FILE) -> pd.DataFrame:
    """
    Convenience function to load Nifty 50 data from file.

    Args:
        data_file: Path to the CSV data file

    Returns:
        pandas.DataFrame: Loaded data
    """
    manager = NiftyDataManager(data_file=data_file)
    return manager.load_data()


if __name__ == "__main__":
    # Simple test when run directly
    logging.basicConfig(level=logging.INFO)
    try:
        data = download_nifty_50(period_years=1)  # Download just 1 year for quick test
        print(f"Successfully downloaded {len(data)} rows of data")
        print(data.head())
    except Exception as e:
        print(f"Error: {e}")
