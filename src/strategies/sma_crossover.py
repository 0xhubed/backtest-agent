"""
SMA Crossover Strategy.

Generates buy signals when the short-term SMA crosses above the long-term SMA,
and sell signals when the short-term SMA crosses below the long-term SMA.
"""

import pandas as pd
import numpy as np

from src.strategies.base_strategy import BaseStrategy
from src.utils.validators import validate_sma_parameters


class SMACrossover(BaseStrategy):
    """
    Simple Moving Average (SMA) Crossover Strategy.

    Buy when short_sma > long_sma (golden cross)
    Sell when short_sma < long_sma (death cross)
    """

    def __init__(
        self,
        short_period: int = 20,
        long_period: int = 50,
        initial_capital: float = 10000.0,
        commission: float = 0.001
    ):
        """
        Initialize SMA Crossover strategy.

        Args:
            short_period: Period for short-term SMA (default: 20)
            long_period: Period for long-term SMA (default: 50)
            initial_capital: Starting capital (default: 10000)
            commission: Commission per trade (default: 0.001)
        """
        super().__init__(initial_capital, commission)

        # Validate parameters
        is_valid, error = validate_sma_parameters(short_period, long_period)
        if not is_valid:
            raise ValueError(error)

        self.short_period = short_period
        self.long_period = long_period

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on SMA crossover.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            Series with signals: 1 (buy), -1 (sell), 0 (hold)
        """
        # Calculate SMAs
        short_sma = data['Close'].rolling(window=self.short_period).mean()
        long_sma = data['Close'].rolling(window=self.long_period).mean()

        # Initialize signals
        signals = pd.Series(0, index=data.index)

        # Generate signals
        # Buy when short SMA crosses above long SMA
        # Sell when short SMA crosses below long SMA

        # Calculate crossovers
        # Position: 1 when short > long, 0 otherwise
        position = (short_sma > long_sma).astype(int)

        # Signal is the difference in position (change)
        signals = position.diff()

        # signals will be:
        #  1: when crossing above (buy)
        # -1: when crossing below (sell)
        #  0: no change

        # Fill NaN values with 0 (no signal when not enough data)
        signals = signals.fillna(0)

        return signals

    def get_parameters(self) -> dict:
        """
        Get strategy parameters.

        Returns:
            Dictionary of parameters
        """
        params = super().get_parameters()
        params.update({
            "short_period": self.short_period,
            "long_period": self.long_period
        })
        return params

    def __str__(self) -> str:
        """String representation."""
        return f"SMA({self.short_period},{self.long_period})"
