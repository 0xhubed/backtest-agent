"""
RSI Mean Reversion Strategy.

Generates buy signals when RSI falls below the lower threshold (oversold),
and sell signals when RSI rises above the upper threshold (overbought).
"""

import pandas as pd
import numpy as np

from src.strategies.base_strategy import BaseStrategy
from src.utils.validators import validate_rsi_parameters


class RSIMeanReversion(BaseStrategy):
    """
    Relative Strength Index (RSI) Mean Reversion Strategy.

    Buy when RSI < lower_threshold (oversold condition)
    Sell when RSI > upper_threshold (overbought condition)
    """

    def __init__(
        self,
        period: int = 14,
        lower_threshold: int = 30,
        upper_threshold: int = 70,
        initial_capital: float = 10000.0,
        commission: float = 0.001
    ):
        """
        Initialize RSI Mean Reversion strategy.

        Args:
            period: RSI calculation period (default: 14)
            lower_threshold: Oversold threshold for buy signal (default: 30)
            upper_threshold: Overbought threshold for sell signal (default: 70)
            initial_capital: Starting capital (default: 10000)
            commission: Commission per trade (default: 0.001)
        """
        super().__init__(initial_capital, commission)

        # Validate parameters
        is_valid, error = validate_rsi_parameters(period, lower_threshold, upper_threshold)
        if not is_valid:
            raise ValueError(error)

        self.period = period
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def _calculate_rsi(self, prices: pd.Series) -> pd.Series:
        """
        Calculate RSI indicator.

        Args:
            prices: Series of prices

        Returns:
            Series with RSI values (0-100)
        """
        # Calculate price changes
        delta = prices.diff()

        # Separate gains and losses
        gains = delta.copy()
        losses = delta.copy()

        gains[gains < 0] = 0
        losses[losses > 0] = 0
        losses = abs(losses)

        # Calculate average gains and losses using exponential moving average
        avg_gains = gains.ewm(span=self.period, adjust=False).mean()
        avg_losses = losses.ewm(span=self.period, adjust=False).mean()

        # Calculate RS (Relative Strength)
        rs = avg_gains / avg_losses

        # Calculate RSI
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on RSI.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            Series with signals: 1 (buy), -1 (sell), 0 (hold)
        """
        # Calculate RSI
        rsi = self._calculate_rsi(data['Close'])

        # Initialize signals
        signals = pd.Series(0, index=data.index)

        # Track current position (0 = no position, 1 = in position)
        position = 0

        for i in range(len(data)):
            current_rsi = rsi.iloc[i]

            if pd.isna(current_rsi):
                continue

            # Buy signal: RSI crosses below lower threshold and we're not in a position
            if current_rsi < self.lower_threshold and position == 0:
                signals.iloc[i] = 1  # Buy
                position = 1

            # Sell signal: RSI crosses above upper threshold and we're in a position
            elif current_rsi > self.upper_threshold and position == 1:
                signals.iloc[i] = -1  # Sell
                position = 0

        return signals

    def get_parameters(self) -> dict:
        """
        Get strategy parameters.

        Returns:
            Dictionary of parameters
        """
        params = super().get_parameters()
        params.update({
            "period": self.period,
            "lower_threshold": self.lower_threshold,
            "upper_threshold": self.upper_threshold
        })
        return params

    def __str__(self) -> str:
        """String representation."""
        return f"RSI({self.period},{self.lower_threshold}-{self.upper_threshold})"
