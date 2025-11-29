"""
ADK-compatible data tools for BackTestPilot.

These are plain Python functions that serve as tools for Google ADK agents.
Each function has proper type hints and docstrings that ADK uses to understand
what the tool does and how to call it.
"""

from typing import Dict, List
import pandas as pd
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.tools.data_tools import (
    load_ohlcv,
    get_supported_symbols as _get_supported_symbols,
    check_symbol_data_exists,
    get_data_info as _get_data_info
)


def fetch_ohlcv_data(symbol: str, start_date: str, end_date: str) -> dict:
    """
    Fetches OHLCV (Open, High, Low, Close, Volume) data for a cryptocurrency symbol.

    This tool loads historical price data from the Kaggle cryptocurrency dataset.
    Data is automatically cached for faster subsequent requests.

    Args:
        symbol: Cryptocurrency symbol (BTC, ETH, LTC, or XRP)
        start_date: Start date in YYYY-MM-DD format (e.g., "2021-01-01")
        end_date: End date in YYYY-MM-DD format (e.g., "2024-12-31")

    Returns:
        Dictionary containing:
        - success (bool): Whether data was loaded successfully
        - symbol (str): The cryptocurrency symbol
        - data (DataFrame): OHLCV data with Date index if successful
        - error (str): Error message if unsuccessful
        - from_cache (bool): Whether data was loaded from cache

    Example:
        >>> result = fetch_ohlcv_data("BTC", "2021-01-01", "2022-01-01")
        >>> if result['success']:
        >>>     df = result['data']
        >>>     print(f"Loaded {len(df)} days of {result['symbol']} data")
    """
    result = load_ohlcv(symbol, start_date, end_date)

    # Convert DataFrame to serializable format for ADK
    if result.get('success') and 'data' in result:
        # Keep DataFrame for now, but flag it for serialization
        result['data_shape'] = result['data'].shape
        result['data_columns'] = list(result['data'].columns)
        result['data_info'] = f"{len(result['data'])} records from {result['data'].index[0]} to {result['data'].index[-1]}"

    return result


def fetch_multiple_symbols(symbols: List[str], start_date: str, end_date: str) -> dict:
    """
    Fetches OHLCV data for multiple cryptocurrency symbols in parallel.

    This tool loads data for multiple symbols concurrently, providing significant
    speedup compared to sequential loading. Useful for comparing strategies across
    multiple assets.

    Args:
        symbols: List of cryptocurrency symbols (e.g., ["BTC", "ETH", "LTC"])
        start_date: Start date in YYYY-MM-DD format (e.g., "2021-01-01")
        end_date: End date in YYYY-MM-DD format (e.g., "2024-12-31")

    Returns:
        Dictionary containing:
        - success (bool): True if all symbols loaded successfully
        - results (dict): Mapping of symbol to individual fetch results
        - errors (list): List of error messages for failed symbols
        - summary (str): Human-readable summary of results

    Example:
        >>> result = fetch_multiple_symbols(["BTC", "ETH"], "2021-01-01", "2022-01-01")
        >>> if result['success']:
        >>>     btc_data = result['results']['BTC']['data']
        >>>     eth_data = result['results']['ETH']['data']
    """
    # Run async function in sync context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        from src.tools.data_tools import load_ohlcv_parallel
        result = loop.run_until_complete(
            load_ohlcv_parallel(symbols, start_date, end_date)
        )
    finally:
        loop.close()

    # Add summary for ADK
    success_count = sum(1 for r in result['results'].values() if r['success'])
    total_count = len(symbols)

    result['summary'] = f"Loaded {success_count}/{total_count} symbols successfully"

    # Add data info for each successful symbol
    for symbol, symbol_result in result['results'].items():
        if symbol_result.get('success') and 'data' in symbol_result:
            df = symbol_result['data']
            symbol_result['data_shape'] = df.shape
            symbol_result['data_columns'] = list(df.columns)
            symbol_result['data_info'] = f"{len(df)} records from {df.index[0]} to {df.index[-1]}"

    return result


def get_available_symbols() -> dict:
    """
    Returns the list of supported cryptocurrency symbols.

    This tool provides information about which cryptocurrencies have data available
    in the system. Use this before attempting to fetch data.

    Returns:
        Dictionary containing:
        - symbols (list): List of available symbol strings (e.g., ["BTC", "ETH", "LTC", "XRP"])
        - count (int): Number of available symbols
        - description (str): Human-readable description

    Example:
        >>> result = get_available_symbols()
        >>> print(result['symbols'])  # ['BTC', 'ETH', 'LTC', 'XRP']
    """
    symbols = _get_supported_symbols()

    return {
        "symbols": symbols,
        "count": len(symbols),
        "description": f"BackTestPilot supports {len(symbols)} cryptocurrencies: {', '.join(symbols)}"
    }


def check_data_availability(symbol: str) -> dict:
    """
    Checks if data is available for a specific cryptocurrency symbol.

    This tool verifies that the required CSV data file exists for the symbol
    and provides information about the available date range and record count.

    Args:
        symbol: Cryptocurrency symbol to check (BTC, ETH, LTC, or XRP)

    Returns:
        Dictionary containing:
        - symbol (str): The cryptocurrency symbol
        - available (bool): Whether data file exists
        - date_range (tuple): (start_date, end_date) if available
        - record_count (int): Number of records if available
        - message (str): Human-readable status message

    Example:
        >>> result = check_data_availability("BTC")
        >>> if result['available']:
        >>>     print(f"BTC data: {result['date_range'][0]} to {result['date_range'][1]}")
    """
    info = _get_data_info(symbol)

    if not info['success']:
        return {
            "symbol": symbol,
            "available": False,
            "message": info.get('error', 'Unknown error')
        }

    if not info.get('file_exists', False):
        return {
            "symbol": symbol,
            "available": False,
            "message": f"Data file for {symbol} not found. Please download the Kaggle dataset."
        }

    date_range = info['date_range']
    record_count = info['record_count']

    return {
        "symbol": symbol,
        "available": True,
        "date_range": date_range,
        "record_count": record_count,
        "message": f"{symbol} data available: {record_count} records from {date_range[0]} to {date_range[1]}"
    }


def get_recommended_date_ranges(symbol: str) -> dict:
    """
    Get recommended date ranges for backtesting a specific cryptocurrency.

    This tool checks the available data and suggests good date ranges that
    have sufficient history for various trading strategies.

    Args:
        symbol: Cryptocurrency symbol (BTC, ETH, LTC, or XRP)

    Returns:
        Dictionary containing:
        - symbol (str): The cryptocurrency symbol
        - available (bool): Whether data is available
        - data_start (str): Earliest available date
        - data_end (str): Latest available date
        - total_days (int): Total days of data available
        - recommended_ranges (dict): Suggested date ranges for backtesting
        - message (str): Human-readable guidance

    Example:
        >>> result = get_recommended_date_ranges("BTC")
        >>> print(result['recommended_ranges']['recent_1year'])
    """
    info = _get_data_info(symbol)

    if not info['success'] or not info.get('file_exists', False):
        return {
            'symbol': symbol,
            'available': False,
            'message': f'No data available for {symbol}. Please download the Kaggle dataset.'
        }

    data_start, data_end = info['date_range']
    total_days = info['record_count']

    from datetime import datetime, timedelta
    end_dt = datetime.strptime(data_end, '%Y-%m-%d')
    start_dt = datetime.strptime(data_start, '%Y-%m-%d')

    # Calculate recommended ranges (leaving 200 days warmup for indicators)
    warmup_days = 200

    # Recent 1 year (if enough data)
    recent_1y_start = end_dt - timedelta(days=365 + warmup_days)
    recent_1y_end = end_dt

    # Recent 2 years
    recent_2y_start = end_dt - timedelta(days=730 + warmup_days)
    recent_2y_end = end_dt

    # Full range (with warmup)
    full_start = start_dt + timedelta(days=warmup_days)
    full_end = end_dt

    recommended = {}

    if recent_1y_start >= start_dt:
        recommended['recent_1year'] = {
            'start': recent_1y_start.strftime('%Y-%m-%d'),
            'end': recent_1y_end.strftime('%Y-%m-%d'),
            'description': 'Recent 1 year of data with sufficient warmup'
        }

    if recent_2y_start >= start_dt:
        recommended['recent_2years'] = {
            'start': recent_2y_start.strftime('%Y-%m-%d'),
            'end': recent_2y_end.strftime('%Y-%m-%d'),
            'description': 'Recent 2 years of data'
        }

    if (full_end - full_start).days > 365:
        recommended['full_range'] = {
            'start': full_start.strftime('%Y-%m-%d'),
            'end': full_end.strftime('%Y-%m-%d'),
            'description': 'Full available data range'
        }

    return {
        'symbol': symbol,
        'available': True,
        'data_start': data_start,
        'data_end': data_end,
        'total_days': total_days,
        'recommended_ranges': recommended,
        'message': f'{symbol} data: {data_start} to {data_end} ({total_days} days). Use dates BEFORE {data_end} and allow 200+ days for indicator warmup.'
    }


def validate_backtest_parameters(
    symbols: List[str],
    start_date: str,
    end_date: str
) -> dict:
    """
    Validates parameters for a backtest request before execution.

    This tool checks that all symbols are supported, dates are valid, and
    data is available for the requested period. Use this to validate user
    input before running expensive backtest operations.

    Args:
        symbols: List of cryptocurrency symbols to validate
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format

    Returns:
        Dictionary containing:
        - valid (bool): Whether all parameters are valid
        - errors (list): List of validation error messages
        - warnings (list): List of warning messages
        - message (str): Human-readable validation summary

    Example:
        >>> result = validate_backtest_parameters(["BTC", "ETH"], "2021-01-01", "2022-01-01")
        >>> if not result['valid']:
        >>>     print("Validation failed:", result['errors'])
    """
    from src.utils.validators import validate_symbol, validate_date_range

    errors = []
    warnings = []

    # Validate each symbol
    for symbol in symbols:
        is_valid, error = validate_symbol(symbol)
        if not is_valid:
            errors.append(f"Symbol {symbol}: {error}")
        else:
            # Check if data exists
            if not check_symbol_data_exists(symbol):
                errors.append(f"Symbol {symbol}: Data file not found")

    # Validate date range
    is_valid, error = validate_date_range(start_date, end_date)
    if not is_valid:
        errors.append(f"Date range: {error}")

    # Check date range length
    from datetime import datetime
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        days = (end - start).days

        if days < 200:
            warnings.append(f"Short date range ({days} days). Strategies like SMA(200) may not have enough data.")

        if days > 2000:
            warnings.append(f"Long date range ({days} days). Backtests may take longer to execute.")

    except Exception as e:
        errors.append(f"Date parsing error: {str(e)}")

    valid = len(errors) == 0

    message = "Validation passed" if valid else f"Validation failed with {len(errors)} error(s)"
    if warnings:
        message += f" and {len(warnings)} warning(s)"

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "message": message
    }
