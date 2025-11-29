"""
Input validation utilities for BackTestPilot.

Provides functions to validate user inputs, date ranges, parameters,
and symbol existence.
"""

from datetime import datetime
from typing import List, Optional, Tuple
import pandas as pd

from src.utils.config import SUPPORTED_SYMBOLS


def validate_symbol(symbol: str) -> Tuple[bool, str]:
    """
    Validate if a symbol is supported.

    Args:
        symbol: Symbol to validate (e.g., "BTC", "ETH")

    Returns:
        Tuple of (is_valid, error_message)
    """
    symbol = symbol.upper()
    if symbol not in SUPPORTED_SYMBOLS:
        return False, f"Symbol '{symbol}' not supported. Supported symbols: {list(SUPPORTED_SYMBOLS.keys())}"
    return True, ""


def validate_symbols(symbols: List[str]) -> Tuple[bool, str]:
    """
    Validate a list of symbols.

    Args:
        symbols: List of symbols to validate

    Returns:
        Tuple of (all_valid, error_message)
    """
    if not symbols:
        return False, "At least one symbol must be provided"

    for symbol in symbols:
        is_valid, error = validate_symbol(symbol)
        if not is_valid:
            return False, error

    return True, ""


def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
    """
    Validate a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if start >= end:
            return False, "Start date must be before end date"

        # Check if date range is too short (minimum 30 days for meaningful backtest)
        days_diff = (end - start).days
        if days_diff < 30:
            return False, f"Date range too short ({days_diff} days). Minimum 30 days required."

        return True, ""

    except ValueError as e:
        return False, f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}"


def validate_data_sufficient(data: pd.DataFrame, required_days: int = 200) -> Tuple[bool, str]:
    """
    Validate if data has sufficient history for backtesting.

    Args:
        data: DataFrame with OHLCV data
        required_days: Minimum number of days required

    Returns:
        Tuple of (is_sufficient, error_message)
    """
    if data is None or len(data) == 0:
        return False, "No data available"

    if len(data) < required_days:
        return False, f"Insufficient data: {len(data)} days. Required: {required_days} days."

    # Check for missing values in critical columns
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_columns = [col for col in required_columns if col not in data.columns]

    if missing_columns:
        return False, f"Missing required columns: {missing_columns}"

    # Check for NaN values
    for col in required_columns:
        if data[col].isna().any():
            nan_count = data[col].isna().sum()
            return False, f"Column '{col}' has {nan_count} missing values"

    return True, ""


def validate_sma_parameters(short_period: int, long_period: int) -> Tuple[bool, str]:
    """
    Validate SMA crossover parameters.

    Args:
        short_period: Short SMA period
        long_period: Long SMA period

    Returns:
        Tuple of (is_valid, error_message)
    """
    if short_period <= 0 or long_period <= 0:
        return False, "SMA periods must be positive integers"

    if short_period >= long_period:
        return False, "Short SMA period must be less than long SMA period"

    if short_period < 2:
        return False, "Short SMA period must be at least 2"

    if long_period > 200:
        return False, "Long SMA period should not exceed 200 for practical purposes"

    return True, ""


def validate_rsi_parameters(period: int, lower_threshold: int, upper_threshold: int) -> Tuple[bool, str]:
    """
    Validate RSI mean reversion parameters.

    Args:
        period: RSI period
        lower_threshold: Oversold threshold (buy signal)
        upper_threshold: Overbought threshold (sell signal)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if period <= 0:
        return False, "RSI period must be a positive integer"

    if period < 2:
        return False, "RSI period must be at least 2"

    if not (0 <= lower_threshold <= 100):
        return False, "Lower threshold must be between 0 and 100"

    if not (0 <= upper_threshold <= 100):
        return False, "Upper threshold must be between 0 and 100"

    if lower_threshold >= upper_threshold:
        return False, "Lower threshold must be less than upper threshold"

    # Standard RSI thresholds
    if lower_threshold > 40:
        return False, "Lower threshold typically should be ≤ 40 (common: 30)"

    if upper_threshold < 60:
        return False, "Upper threshold typically should be ≥ 60 (common: 70)"

    return True, ""
