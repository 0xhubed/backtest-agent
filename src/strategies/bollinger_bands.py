"""
Bollinger Bands strategy implementation.

Bollinger Bands use a moving average with upper and lower bands set at
standard deviations above/below. The strategy buys when price touches
the lower band and sells when it touches the upper band (mean reversion).
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

from src.strategies.base_strategy import BaseStrategy


class BollingerBands(BaseStrategy):
    """
    Bollinger Bands mean reversion strategy.

    Signals:
    - BUY: Price crosses below lower band (oversold)
    - SELL: Price crosses above upper band (overbought)
    - HOLD: Price within bands

    Parameters:
    - period: Moving average period (default: 20)
    - std_dev: Number of standard deviations for bands (default: 2.0)
    """

    def __init__(
        self,
        period: int = 20,
        std_dev: float = 2.0,
        initial_capital: float = 10000.0,
        commission: float = 0.001
    ):
        """
        Initialize Bollinger Bands strategy.

        Args:
            period: Moving average period
            std_dev: Number of standard deviations for bands
            initial_capital: Starting capital
            commission: Commission per trade
        """
        super().__init__(initial_capital=initial_capital, commission=commission)
        self.period = period
        self.std_dev = std_dev
        self.strategy_name = "BollingerBands"

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on Bollinger Bands.

        Args:
            data: DataFrame with OHLCV data (must have 'Close' column)

        Returns:
            Series with signals: 1 (buy), -1 (sell), 0 (hold)
        """
        if len(data) < self.period:
            return pd.Series(0, index=data.index)

        # Calculate Bollinger Bands
        close = data['Close']

        # Middle band (SMA)
        middle_band = close.rolling(window=self.period).mean()

        # Calculate standard deviation
        rolling_std = close.rolling(window=self.period).std()

        # Upper and lower bands
        upper_band = middle_band + (self.std_dev * rolling_std)
        lower_band = middle_band - (self.std_dev * rolling_std)

        # Initialize signals
        signals = pd.Series(0, index=data.index)

        # Generate signals based on band crosses
        # Buy when price crosses below lower band (oversold)
        signals[close < lower_band] = 1

        # Sell when price crosses above upper band (overbought)
        signals[close > upper_band] = -1

        # Alternative: Use position changes only
        # Track position: 1 = long, 0 = flat, -1 = short
        position = pd.Series(0, index=data.index)

        for i in range(self.period, len(data)):
            # Enter long when price touches lower band
            if close.iloc[i] <= lower_band.iloc[i] and position.iloc[i-1] <= 0:
                position.iloc[i] = 1
                signals.iloc[i] = 1  # Buy signal

            # Exit long (or enter short) when price touches upper band
            elif close.iloc[i] >= upper_band.iloc[i] and position.iloc[i-1] >= 0:
                if position.iloc[i-1] == 1:
                    signals.iloc[i] = -1  # Sell signal
                position.iloc[i] = 0

            # Hold current position
            else:
                position.iloc[i] = position.iloc[i-1]

        return signals

    def calculate_indicators(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Calculate Bollinger Bands indicators for visualization.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            Dictionary with middle, upper, and lower bands
        """
        close = data['Close']

        # Middle band (SMA)
        middle_band = close.rolling(window=self.period).mean()

        # Calculate standard deviation
        rolling_std = close.rolling(window=self.period).std()

        # Upper and lower bands
        upper_band = middle_band + (self.std_dev * rolling_std)
        lower_band = middle_band - (self.std_dev * rolling_std)

        return {
            'middle_band': middle_band,
            'upper_band': upper_band,
            'lower_band': lower_band,
            'bandwidth': (upper_band - lower_band) / middle_band,  # Band width %
            'percent_b': (close - lower_band) / (upper_band - lower_band)  # %B indicator
        }

    def get_parameters(self) -> Dict[str, Any]:
        """
        Get strategy parameters.

        Returns:
            Dictionary of parameters
        """
        return {
            'strategy': self.strategy_name,
            'period': self.period,
            'std_dev': self.std_dev,
            'initial_capital': self.initial_capital,
            'commission': self.commission
        }

    def __str__(self) -> str:
        """String representation of the strategy."""
        return f"BollingerBands({self.period}, {self.std_dev})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"BollingerBands(period={self.period}, "
            f"std_dev={self.std_dev}, initial_capital={self.initial_capital})"
        )


def run_bollinger_bands(
    symbol: str,
    data: pd.DataFrame,
    period: int = 20,
    std_dev: float = 2.0,
    initial_capital: float = 10000.0,
    position_size: float = 1.0,
    commission: float = 0.001
) -> Dict[str, Any]:
    """
    Run Bollinger Bands backtest (tool function).

    Args:
        symbol: Trading symbol
        data: OHLCV DataFrame
        period: Moving average period
        std_dev: Number of standard deviations
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
        strategy = BollingerBands(
            symbol=symbol,
            period=period,
            std_dev=std_dev,
            initial_capital=initial_capital,
            position_size=position_size,
            commission=commission
        )

        equity_curve, trades = strategy.backtest(data)

        return {
            'success': True,
            'strategy': 'BollingerBands',
            'symbol': symbol,
            'equity_curve': equity_curve,
            'trades': trades,
            'parameters': strategy.get_parameters(),
            'indicators': strategy.calculate_indicators(data)
        }

    except Exception as e:
        return {
            'success': False,
            'strategy': 'BollingerBands',
            'symbol': symbol,
            'error': str(e)
        }
