"""
Unit tests for data tools.

Tests data loading, caching, validation, and parallel fetching.
"""

import pytest
import pandas as pd
import asyncio
from datetime import datetime

from src.tools.data_tools import (
    get_supported_symbols,
    load_ohlcv,
    load_ohlcv_parallel,
    get_data_info
)
from src.utils.validators import (
    validate_symbol,
    validate_symbols,
    validate_date_range,
    validate_data_sufficient
)


class TestDataTools:
    """Test suite for data tools."""

    def test_get_supported_symbols(self):
        """Test getting supported symbols."""
        symbols = get_supported_symbols()
        assert isinstance(symbols, list)
        assert len(symbols) > 0
        assert "BTC" in symbols
        assert "ETH" in symbols

    def test_validate_symbol_valid(self):
        """Test symbol validation with valid symbols."""
        is_valid, error = validate_symbol("BTC")
        assert is_valid is True
        assert error == ""

        is_valid, error = validate_symbol("eth")  # Test lowercase
        assert is_valid is True

    def test_validate_symbol_invalid(self):
        """Test symbol validation with invalid symbols."""
        is_valid, error = validate_symbol("INVALID")
        assert is_valid is False
        assert "not supported" in error.lower()

    def test_validate_symbols_list(self):
        """Test validating a list of symbols."""
        is_valid, error = validate_symbols(["BTC", "ETH"])
        assert is_valid is True

        is_valid, error = validate_symbols([])
        assert is_valid is False

        is_valid, error = validate_symbols(["BTC", "INVALID"])
        assert is_valid is False

    def test_validate_date_range_valid(self):
        """Test date range validation with valid ranges."""
        is_valid, error = validate_date_range("2020-01-01", "2021-01-01")
        assert is_valid is True
        assert error == ""

    def test_validate_date_range_invalid(self):
        """Test date range validation with invalid ranges."""
        # End before start
        is_valid, error = validate_date_range("2021-01-01", "2020-01-01")
        assert is_valid is False

        # Too short
        is_valid, error = validate_date_range("2020-01-01", "2020-01-10")
        assert is_valid is False
        assert "too short" in error.lower()

        # Invalid format
        is_valid, error = validate_date_range("2020/01/01", "2021-01-01")
        assert is_valid is False

    def test_validate_data_sufficient(self):
        """Test data sufficiency validation."""
        # Create mock data
        dates = pd.date_range(start='2020-01-01', periods=250, freq='D')
        data = pd.DataFrame({
            'Open': [100] * 250,
            'High': [105] * 250,
            'Low': [95] * 250,
            'Close': [102] * 250,
            'Volume': [1000000] * 250
        }, index=dates)

        is_sufficient, error = validate_data_sufficient(data)
        assert is_sufficient is True

        # Test insufficient data
        short_data = data.head(50)
        is_sufficient, error = validate_data_sufficient(short_data, required_days=200)
        assert is_sufficient is False

    def test_load_ohlcv_validation(self):
        """Test OHLCV loading with validation errors."""
        # Invalid symbol
        result = load_ohlcv("INVALID", "2020-01-01", "2021-01-01")
        assert result['success'] is False
        assert 'symbol' in result
        assert 'error' in result

        # Invalid date range
        result = load_ohlcv("BTC", "2021-01-01", "2020-01-01")
        assert result['success'] is False

    @pytest.mark.asyncio
    async def test_load_ohlcv_parallel_validation(self):
        """Test parallel loading with validation."""
        # Test with invalid symbols
        result = await load_ohlcv_parallel(
            ["BTC", "INVALID"],
            "2020-01-01",
            "2021-01-01"
        )
        assert result['success'] is False
        assert len(result['errors']) > 0

    def test_get_data_info_validation(self):
        """Test getting data info for symbols."""
        result = get_data_info("BTC")
        assert 'success' in result
        assert 'symbol' in result
        assert result['symbol'] == "BTC"

        # Invalid symbol
        result = get_data_info("INVALID")
        assert result['success'] is False


class TestValidators:
    """Test suite for validators."""

    def test_sma_parameters_valid(self):
        """Test SMA parameter validation with valid parameters."""
        from src.utils.validators import validate_sma_parameters

        is_valid, error = validate_sma_parameters(20, 50)
        assert is_valid is True

        is_valid, error = validate_sma_parameters(10, 200)
        assert is_valid is True

    def test_sma_parameters_invalid(self):
        """Test SMA parameter validation with invalid parameters."""
        from src.utils.validators import validate_sma_parameters

        # Short >= Long
        is_valid, error = validate_sma_parameters(50, 20)
        assert is_valid is False

        # Zero or negative
        is_valid, error = validate_sma_parameters(0, 50)
        assert is_valid is False

        # Too long
        is_valid, error = validate_sma_parameters(20, 300)
        assert is_valid is False

    def test_rsi_parameters_valid(self):
        """Test RSI parameter validation with valid parameters."""
        from src.utils.validators import validate_rsi_parameters

        is_valid, error = validate_rsi_parameters(14, 30, 70)
        assert is_valid is True

        is_valid, error = validate_rsi_parameters(14, 20, 80)
        assert is_valid is True

    def test_rsi_parameters_invalid(self):
        """Test RSI parameter validation with invalid parameters."""
        from src.utils.validators import validate_rsi_parameters

        # Lower >= Upper
        is_valid, error = validate_rsi_parameters(14, 70, 30)
        assert is_valid is False

        # Out of range
        is_valid, error = validate_rsi_parameters(14, -10, 70)
        assert is_valid is False

        is_valid, error = validate_rsi_parameters(14, 30, 110)
        assert is_valid is False

        # Unrealistic thresholds
        is_valid, error = validate_rsi_parameters(14, 50, 60)
        assert is_valid is False
