"""
Data loading and caching tools for BackTestPilot.

Provides functions to load OHLCV data from CSV files, validate data,
and cache processed data for faster subsequent runs.
"""

import hashlib
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.utils.config import DATA_DIR, CACHE_DIR, SUPPORTED_SYMBOLS
from src.utils.validators import validate_symbol, validate_date_range, validate_data_sufficient


def get_supported_symbols() -> List[str]:
    """
    Get list of supported cryptocurrency symbols.

    Returns:
        List of supported symbol strings (e.g., ["BTC", "ETH", "LTC", "XRP"])
    """
    return list(SUPPORTED_SYMBOLS.keys())


def check_symbol_data_exists(symbol: str) -> bool:
    """
    Check if data file exists for a given symbol.

    Args:
        symbol: Symbol to check

    Returns:
        True if data file exists, False otherwise
    """
    symbol_upper = symbol.upper()
    if symbol_upper not in SUPPORTED_SYMBOLS:
        return False

    csv_filename = SUPPORTED_SYMBOLS[symbol_upper]
    csv_path = DATA_DIR / csv_filename

    return csv_path.exists()


def _generate_cache_key(symbol: str, start_date: str, end_date: str) -> str:
    """
    Generate a unique cache key for the data request.

    Args:
        symbol: Symbol string
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format

    Returns:
        Cache key string
    """
    key_string = f"{symbol}_{start_date}_{end_date}"
    return hashlib.md5(key_string.encode()).hexdigest()


def _get_cache_path(cache_key: str) -> Path:
    """
    Get the cache file path for a given cache key.

    Args:
        cache_key: Cache key string

    Returns:
        Path to cache file
    """
    return CACHE_DIR / f"{cache_key}.pkl"


def _load_from_cache(cache_key: str) -> Optional[pd.DataFrame]:
    """
    Load data from cache if it exists.

    Args:
        cache_key: Cache key string

    Returns:
        DataFrame if cache exists, None otherwise
    """
    cache_path = _get_cache_path(cache_key)
    if cache_path.exists():
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            # Cache corrupted, return None
            return None
    return None


def _save_to_cache(cache_key: str, data: pd.DataFrame) -> None:
    """
    Save data to cache.

    Args:
        cache_key: Cache key string
        data: DataFrame to cache
    """
    cache_path = _get_cache_path(cache_key)
    try:
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)
    except Exception:
        # Silently fail if caching doesn't work
        pass


def load_ohlcv(symbol: str, start_date: str, end_date: str, use_cache: bool = True) -> Dict:
    """
    Load OHLCV data for a single symbol.

    Args:
        symbol: Symbol to load (e.g., "BTC", "ETH")
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        use_cache: Whether to use cache (default: True)

    Returns:
        Dictionary with keys:
            - success: bool
            - symbol: str
            - data: pd.DataFrame (if success=True)
            - error: str (if success=False)
    """
    # Validate symbol
    is_valid, error = validate_symbol(symbol)
    if not is_valid:
        return {"success": False, "symbol": symbol, "error": error}

    # Validate date range
    is_valid, error = validate_date_range(start_date, end_date)
    if not is_valid:
        return {"success": False, "symbol": symbol, "error": error}

    # Try to load from cache first
    if use_cache:
        cache_key = _generate_cache_key(symbol, start_date, end_date)
        cached_data = _load_from_cache(cache_key)
        if cached_data is not None:
            return {
                "success": True,
                "symbol": symbol,
                "data": cached_data,
                "from_cache": True
            }

    # Load from CSV file
    symbol_upper = symbol.upper()
    csv_filename = SUPPORTED_SYMBOLS[symbol_upper]
    csv_path = DATA_DIR / csv_filename

    if not csv_path.exists():
        return {
            "success": False,
            "symbol": symbol,
            "error": f"Data file not found: {csv_path}. Please download the dataset."
        }

    try:
        # Read CSV file
        df = pd.read_csv(csv_path)

        # Normalize column names to title case (handle both 'date' and 'Date')
        df.columns = df.columns.str.title()

        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Set Date as index
        df.set_index('Date', inplace=True)

        # Drop ticker column if it exists (not needed for analysis)
        if 'Ticker' in df.columns:
            df.drop('Ticker', axis=1, inplace=True)

        # Sort by date
        df.sort_index(inplace=True)

        # Filter by date range
        df = df.loc[start_date:end_date]

        # Validate data sufficiency
        is_sufficient, error = validate_data_sufficient(df)
        if not is_sufficient:
            return {"success": False, "symbol": symbol, "error": error}

        # Cache the data
        if use_cache:
            cache_key = _generate_cache_key(symbol, start_date, end_date)
            _save_to_cache(cache_key, df)

        return {
            "success": True,
            "symbol": symbol,
            "data": df,
            "from_cache": False
        }

    except Exception as e:
        return {
            "success": False,
            "symbol": symbol,
            "error": f"Error loading data: {str(e)}"
        }


async def load_ohlcv_parallel(symbols: List[str], start_date: str, end_date: str, use_cache: bool = True) -> Dict:
    """
    Load OHLCV data for multiple symbols in parallel.

    Args:
        symbols: List of symbols to load
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        use_cache: Whether to use cache (default: True)

    Returns:
        Dictionary with keys:
            - success: bool
            - results: Dict[str, Dict] - mapping of symbol to load result
            - errors: List[str] - list of error messages
    """
    # Use ThreadPoolExecutor for parallel I/O operations
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        # Create tasks for each symbol
        tasks = [
            loop.run_in_executor(
                executor,
                load_ohlcv,
                symbol,
                start_date,
                end_date,
                use_cache
            )
            for symbol in symbols
        ]

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)

    # Organize results
    results_dict = {}
    errors = []

    for result in results:
        symbol = result['symbol']
        results_dict[symbol] = result

        if not result['success']:
            errors.append(f"{symbol}: {result['error']}")

    return {
        "success": len(errors) == 0,
        "results": results_dict,
        "errors": errors
    }


def get_data_info(symbol: str) -> Dict:
    """
    Get information about available data for a symbol.

    Args:
        symbol: Symbol to check

    Returns:
        Dictionary with data information:
            - success: bool
            - symbol: str
            - file_exists: bool
            - date_range: Tuple[str, str] (start, end) if file exists
            - record_count: int if file exists
            - error: str if error occurred
    """
    # Validate symbol
    is_valid, error = validate_symbol(symbol)
    if not is_valid:
        return {"success": False, "symbol": symbol, "error": error}

    symbol_upper = symbol.upper()
    csv_filename = SUPPORTED_SYMBOLS[symbol_upper]
    csv_path = DATA_DIR / csv_filename

    if not csv_path.exists():
        return {
            "success": True,
            "symbol": symbol,
            "file_exists": False
        }

    try:
        # Read CSV to get info
        df = pd.read_csv(csv_path)

        # Normalize column names to title case
        df.columns = df.columns.str.title()

        df['Date'] = pd.to_datetime(df['Date'])

        min_date = df['Date'].min().strftime('%Y-%m-%d')
        max_date = df['Date'].max().strftime('%Y-%m-%d')

        return {
            "success": True,
            "symbol": symbol,
            "file_exists": True,
            "date_range": (min_date, max_date),
            "record_count": len(df)
        }

    except Exception as e:
        return {
            "success": False,
            "symbol": symbol,
            "error": f"Error reading data file: {str(e)}"
        }
