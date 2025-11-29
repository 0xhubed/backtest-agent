"""
MACD (Moving Average Convergence Divergence) strategy implementation.

MACD is a trend-following momentum indicator that shows the relationship
between two moving averages. The strategy generates buy signals when the
MACD line crosses above the signal line and sell signals when it crosses below.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

from src.strategies.base_strategy import BaseStrategy


class MACD(BaseStrategy):
    """
    MACD trend-following strategy.

    Signals:
    - BUY: MACD line crosses above signal line (bullish crossover)
    - SELL: MACD line crosses below signal line (bearish crossover)
    - HOLD: No crossover

    Parameters:
    - fast_period: Fast EMA period (default: 12)
    - slow_period: Slow EMA period (default: 26)
    - signal_period: Signal line EMA period (default: 9)
    """

    def __init__(
        self,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
        initial_capital: float = 10000.0,
        commission: float = 0.001
    ):
        """
        Initialize MACD strategy.

        Args:
            fast_period: Fast EMA period
            slow_period: Slow EMA period
            signal_period: Signal line period
            initial_capital: Starting capital
            commission: Commission per trade
        """
        super().__init__(initial_capital=initial_capital, commission=commission)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.strategy_name = "MACD"

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on MACD.

        Args:
            data: DataFrame with OHLCV data (must have 'Close' column)

        Returns:
            Series with signals: 1 (buy), -1 (sell), 0 (hold)
        """
        min_periods = self.slow_period + self.signal_period

        if len(data) < min_periods:
            return pd.Series(0, index=data.index)

        # Calculate MACD components
        close = data['Close']

        # Fast and slow EMAs
        fast_ema = close.ewm(span=self.fast_period, adjust=False).mean()
        slow_ema = close.ewm(span=self.slow_period, adjust=False).mean()

        # MACD line
        macd_line = fast_ema - slow_ema

        # Signal line (EMA of MACD)
        signal_line = macd_line.ewm(span=self.signal_period, adjust=False).mean()

        # MACD histogram
        histogram = macd_line - signal_line

        # Initialize signals
        signals = pd.Series(0, index=data.index)

        # Generate signals based on MACD and signal line crossovers
        # Buy when MACD crosses above signal line
        macd_above = (macd_line > signal_line).fillna(False)
        macd_above_prev = macd_above.shift(1).fillna(False)

        # Bullish crossover
        bullish_cross = (macd_above) & (~macd_above_prev)
        signals[bullish_cross] = 1

        # Bearish crossover
        bearish_cross = (~macd_above) & (macd_above_prev)
        signals[bearish_cross] = -1

        # Alternative: Use histogram zero crossings
        # histogram_positive = histogram > 0
        # histogram_positive_prev = histogram_positive.shift(1)
        # bullish_cross = histogram_positive & ~histogram_positive_prev
        # bearish_cross = ~histogram_positive & histogram_positive_prev

        return signals

    def calculate_indicators(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Calculate MACD indicators for visualization.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            Dictionary with MACD line, signal line, and histogram
        """
        close = data['Close']

        # Fast and slow EMAs
        fast_ema = close.ewm(span=self.fast_period, adjust=False).mean()
        slow_ema = close.ewm(span=self.slow_period, adjust=False).mean()

        # MACD line
        macd_line = fast_ema - slow_ema

        # Signal line (EMA of MACD)
        signal_line = macd_line.ewm(span=self.signal_period, adjust=False).mean()

        # MACD histogram
        histogram = macd_line - signal_line

        return {
            'fast_ema': fast_ema,
            'slow_ema': slow_ema,
            'macd_line': macd_line,
            'signal_line': signal_line,
            'histogram': histogram
        }

    def get_parameters(self) -> Dict[str, Any]:
        """
        Get strategy parameters.

        Returns:
            Dictionary of parameters
        """
        return {
            'strategy': self.strategy_name,
            'fast_period': self.fast_period,
            'slow_period': self.slow_period,
            'signal_period': self.signal_period,
            'initial_capital': self.initial_capital,
            'commission': self.commission
        }

    def __str__(self) -> str:
        """String representation of the strategy."""
        return f"MACD({self.fast_period},{self.slow_period},{self.signal_period})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"MACD(fast={self.fast_period}, "
            f"slow={self.slow_period}, signal={self.signal_period}, "
            f"initial_capital={self.initial_capital})"
        )


def run_macd(
    symbol: str,
    data: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
    initial_capital: float = 10000.0,
    position_size: float = 1.0,
    commission: float = 0.001
) -> Dict[str, Any]:
    """
    Run MACD backtest (tool function).

    Args:
        symbol: Trading symbol
        data: OHLCV DataFrame
        fast_period: Fast EMA period
        slow_period: Slow EMA period
        signal_period: Signal line period
        initial_capital: Starting capital
        position_size: Position size (fraction of capital)
        commission: Commission rate

    Returns:
        Backtest result dictionary with:
        - success: bool
        - strategy: str
        - symbol: str
        - equity_curve: pd.DataFrame
        - trades: List[Dict]
        - parameters: Dict
        - error: str (if failed)
    """
    try:
        strategy = MACD(
            symbol=symbol,
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
            initial_capital=initial_capital,
            position_size=position_size,
            commission=commission
        )

        equity_curve, trades = strategy.backtest(data)

        return {
            'success': True,
            'strategy': 'MACD',
            'symbol': symbol,
            'equity_curve': equity_curve,
            'trades': trades,
            'parameters': strategy.get_parameters(),
            'indicators': strategy.calculate_indicators(data)
        }

    except Exception as e:
        return {
            'success': False,
            'strategy': 'MACD',
            'symbol': symbol,
            'error': str(e)
        }
