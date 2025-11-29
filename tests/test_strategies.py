"""
Unit tests for trading strategies.

Tests strategy signal generation, backtesting logic, and parameter validation.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.strategies.base_strategy import BaseStrategy
from src.strategies.sma_crossover import SMACrossover
from src.strategies.rsi_mean_reversion import RSIMeanReversion
from src.strategies.buy_and_hold import BuyAndHold


def create_mock_data(days: int = 100, starting_price: float = 100.0, trend: str = 'up') -> pd.DataFrame:
    """
    Create mock OHLCV data for testing.

    Args:
        days: Number of days of data
        starting_price: Starting price
        trend: 'up', 'down', or 'sideways'

    Returns:
        DataFrame with OHLCV data
    """
    dates = pd.date_range(start='2020-01-01', periods=days, freq='D')

    if trend == 'up':
        # Upward trend with noise
        prices = starting_price + np.linspace(0, 50, days) + np.random.randn(days) * 2
    elif trend == 'down':
        # Downward trend with noise
        prices = starting_price - np.linspace(0, 50, days) + np.random.randn(days) * 2
    else:  # sideways
        # Sideways with noise
        prices = starting_price + np.sin(np.linspace(0, 4*np.pi, days)) * 10 + np.random.randn(days) * 2

    # Ensure prices are positive
    prices = np.maximum(prices, 10)

    data = pd.DataFrame({
        'Open': prices * (1 + np.random.randn(days) * 0.01),
        'High': prices * (1 + np.abs(np.random.randn(days)) * 0.02),
        'Low': prices * (1 - np.abs(np.random.randn(days)) * 0.02),
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, days)
    }, index=dates)

    return data


class TestSMACrossover:
    """Test suite for SMA Crossover strategy."""

    def test_initialization_valid(self):
        """Test strategy initialization with valid parameters."""
        strategy = SMACrossover(short_period=10, long_period=50)
        assert strategy.short_period == 10
        assert strategy.long_period == 50
        assert strategy.initial_capital == 10000.0

    def test_initialization_invalid(self):
        """Test strategy initialization with invalid parameters."""
        # Short >= Long
        with pytest.raises(ValueError):
            SMACrossover(short_period=50, long_period=20)

        # Negative periods
        with pytest.raises(ValueError):
            SMACrossover(short_period=-10, long_period=50)

    def test_generate_signals(self):
        """Test signal generation."""
        strategy = SMACrossover(short_period=5, long_period=10)
        data = create_mock_data(days=100, trend='up')

        signals = strategy.generate_signals(data)

        assert isinstance(signals, pd.Series)
        assert len(signals) == len(data)
        # Signals should be -1, 0, or 1
        assert signals.isin([-1, 0, 1]).all()

    def test_backtest_execution(self):
        """Test backtest execution."""
        strategy = SMACrossover(short_period=5, long_period=10, initial_capital=10000)
        data = create_mock_data(days=100, trend='up')

        result = strategy.backtest(data)

        assert 'equity_curve' in result
        assert 'returns' in result
        assert 'trades' in result
        assert 'final_equity' in result
        assert 'total_return' in result

        assert isinstance(result['equity_curve'], pd.Series)
        assert len(result['equity_curve']) == len(data)
        assert result['final_equity'] > 0

    def test_string_representation(self):
        """Test string representation."""
        strategy = SMACrossover(short_period=20, long_period=50)
        assert str(strategy) == "SMA(20,50)"

    def test_get_parameters(self):
        """Test getting strategy parameters."""
        strategy = SMACrossover(short_period=20, long_period=50)
        params = strategy.get_parameters()

        assert 'short_period' in params
        assert 'long_period' in params
        assert params['short_period'] == 20
        assert params['long_period'] == 50


class TestRSIMeanReversion:
    """Test suite for RSI Mean Reversion strategy."""

    def test_initialization_valid(self):
        """Test strategy initialization with valid parameters."""
        strategy = RSIMeanReversion(period=14, lower_threshold=30, upper_threshold=70)
        assert strategy.period == 14
        assert strategy.lower_threshold == 30
        assert strategy.upper_threshold == 70

    def test_initialization_invalid(self):
        """Test strategy initialization with invalid parameters."""
        # Lower >= Upper
        with pytest.raises(ValueError):
            RSIMeanReversion(period=14, lower_threshold=70, upper_threshold=30)

        # Out of range
        with pytest.raises(ValueError):
            RSIMeanReversion(period=14, lower_threshold=-10, upper_threshold=70)

    def test_generate_signals(self):
        """Test signal generation."""
        strategy = RSIMeanReversion(period=14, lower_threshold=30, upper_threshold=70)
        data = create_mock_data(days=100, trend='sideways')

        signals = strategy.generate_signals(data)

        assert isinstance(signals, pd.Series)
        assert len(signals) == len(data)
        assert signals.isin([-1, 0, 1]).all()

    def test_rsi_calculation(self):
        """Test RSI calculation."""
        strategy = RSIMeanReversion(period=14, lower_threshold=30, upper_threshold=70)
        data = create_mock_data(days=100, trend='up')

        rsi = strategy._calculate_rsi(data['Close'])

        assert isinstance(rsi, pd.Series)
        assert len(rsi) == len(data)
        # RSI should be between 0 and 100 (excluding NaN)
        assert (rsi.dropna() >= 0).all()
        assert (rsi.dropna() <= 100).all()

    def test_backtest_execution(self):
        """Test backtest execution."""
        strategy = RSIMeanReversion(period=14, lower_threshold=30, upper_threshold=70)
        data = create_mock_data(days=100, trend='sideways')

        result = strategy.backtest(data)

        assert 'equity_curve' in result
        assert 'returns' in result
        assert 'trades' in result
        assert 'final_equity' in result
        assert result['final_equity'] > 0

    def test_string_representation(self):
        """Test string representation."""
        strategy = RSIMeanReversion(period=14, lower_threshold=30, upper_threshold=70)
        assert str(strategy) == "RSI(14,30-70)"


class TestBuyAndHold:
    """Test suite for Buy and Hold strategy."""

    def test_initialization(self):
        """Test strategy initialization."""
        strategy = BuyAndHold(initial_capital=10000)
        assert strategy.initial_capital == 10000.0
        assert strategy.commission == 0.001

    def test_generate_signals(self):
        """Test signal generation."""
        strategy = BuyAndHold()
        data = create_mock_data(days=100)

        signals = strategy.generate_signals(data)

        assert isinstance(signals, pd.Series)
        assert len(signals) == len(data)
        # Should have 1 buy signal on first day
        assert signals.iloc[0] == 1
        # Rest should be 0 (hold)
        assert (signals.iloc[1:] == 0).all()

    def test_backtest_execution(self):
        """Test backtest execution."""
        strategy = BuyAndHold(initial_capital=10000)
        data = create_mock_data(days=100, trend='up')

        result = strategy.backtest(data)

        assert 'equity_curve' in result
        assert 'trades' in result
        # Should only have 1 trade (initial buy)
        assert result['trades'] == 1
        assert result['final_equity'] > 0

        # In an uptrend, final equity should be higher than initial
        if data['Close'].iloc[-1] > data['Close'].iloc[0]:
            assert result['total_return'] > 0

    def test_string_representation(self):
        """Test string representation."""
        strategy = BuyAndHold()
        assert str(strategy) == "BuyAndHold"


class TestBaseStrategy:
    """Test suite for base strategy functionality."""

    def test_backtest_commission_impact(self):
        """Test that commission reduces returns."""
        data = create_mock_data(days=100, trend='up')

        # Test with 0% commission
        strategy_no_commission = SMACrossover(
            short_period=5,
            long_period=10,
            commission=0.0
        )
        result_no_commission = strategy_no_commission.backtest(data)

        # Test with 1% commission
        strategy_with_commission = SMACrossover(
            short_period=5,
            long_period=10,
            commission=0.01
        )
        result_with_commission = strategy_with_commission.backtest(data)

        # With commission should have lower or equal final equity
        assert result_with_commission['final_equity'] <= result_no_commission['final_equity']

    def test_backtest_equity_curve_continuity(self):
        """Test that equity curve is continuous and positive."""
        strategy = BuyAndHold(initial_capital=10000)
        data = create_mock_data(days=100)

        result = strategy.backtest(data)
        equity_curve = result['equity_curve']

        # Equity should always be positive
        assert (equity_curve > 0).all()

        # First value should be initial capital
        assert equity_curve.iloc[0] == 10000.0

    def test_backtest_returns_calculation(self):
        """Test that returns are calculated correctly."""
        strategy = BuyAndHold(initial_capital=10000)
        data = create_mock_data(days=100)

        result = strategy.backtest(data)

        equity_curve = result['equity_curve']
        returns = result['returns']

        # First return should be 0 or NaN
        assert returns.iloc[0] == 0

        # Returns should match equity changes
        for i in range(1, len(equity_curve)):
            expected_return = (equity_curve.iloc[i] - equity_curve.iloc[i-1]) / equity_curve.iloc[i-1]
            assert abs(returns.iloc[i] - expected_return) < 1e-10
