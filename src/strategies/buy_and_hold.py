"""
Buy and Hold Strategy.

A baseline strategy that buys on the first day and holds until the end.
This serves as a benchmark to compare other strategies against.
"""

import pandas as pd
import numpy as np

from src.strategies.base_strategy import BaseStrategy


class BuyAndHold(BaseStrategy):
    """
    Buy and Hold Strategy.

    Buys on the first available day and holds the position until the end.
    This is a passive strategy used as a performance benchmark.
    """

    def __init__(
        self,
        initial_capital: float = 10000.0,
        commission: float = 0.001
    ):
        """
        Initialize Buy and Hold strategy.

        Args:
            initial_capital: Starting capital (default: 10000)
            commission: Commission per trade (default: 0.001)
        """
        super().__init__(initial_capital, commission)

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals for buy and hold.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            Series with signals: 1 on first day (buy), 0 thereafter (hold)
        """
        # Initialize signals with zeros
        signals = pd.Series(0, index=data.index)

        # Buy on the first day (generate a buy signal)
        signals.iloc[0] = 1

        return signals

    def get_parameters(self) -> dict:
        """
        Get strategy parameters.

        Returns:
            Dictionary of parameters
        """
        return super().get_parameters()

    def __str__(self) -> str:
        """String representation."""
        return "BuyAndHold"
