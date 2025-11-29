"""
Base strategy class for all trading strategies.

All strategies must inherit from this base class and implement
the generate_signals method. The base class provides backtesting
infrastructure and equity curve calculation.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
import pandas as pd
import numpy as np

from src.utils.config import DEFAULT_INITIAL_CAPITAL, DEFAULT_COMMISSION


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.

    Strategies must implement generate_signals() which returns
    buy/sell signals: 1 (buy), -1 (sell), 0 (hold).
    """

    def __init__(
        self,
        initial_capital: float = DEFAULT_INITIAL_CAPITAL,
        commission: float = DEFAULT_COMMISSION
    ):
        """
        Initialize the strategy.

        Args:
            initial_capital: Starting capital in USD (default: 10000)
            commission: Commission per trade as decimal (default: 0.001 = 0.1%)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.name = self.__class__.__name__

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals from OHLCV data.

        Must be implemented by subclasses.

        Args:
            data: DataFrame with OHLCV data (columns: Open, High, Low, Close, Volume)

        Returns:
            Series with signals: 1 (buy), -1 (sell), 0 (hold)
        """
        pass

    def backtest(self, data: pd.DataFrame) -> Dict:
        """
        Execute the strategy and calculate equity curve.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            Dictionary with:
                - equity_curve: pd.Series - equity over time
                - returns: pd.Series - daily returns
                - positions: pd.Series - positions held
                - trades: int - number of trades executed
                - final_equity: float - final portfolio value
                - total_return: float - total return as decimal
        """
        # Generate signals
        signals = self.generate_signals(data)

        # Convert signals to positions (1 = long, 0 = flat)
        # Signals: 1 = buy, -1 = sell, 0 = hold
        # Positions: 1 = long, 0 = flat (cumulative state)
        positions = pd.Series(0, index=data.index, dtype=float)

        current_position = 0
        for i in range(len(signals)):
            if signals.iloc[i] == 1:  # Buy signal
                current_position = 1
            elif signals.iloc[i] == -1:  # Sell signal
                current_position = 0
            positions.iloc[i] = current_position

        # Calculate position changes (when we buy/sell)
        position_changes = positions.diff()

        # Calculate returns
        # We use Close prices for execution
        close_prices = data['Close'].copy()

        # Initialize equity curve
        equity = pd.Series(index=data.index, dtype=float)
        equity.iloc[0] = self.initial_capital

        # Track cash and shares
        cash = self.initial_capital
        shares = 0.0

        trades = 0

        for i in range(len(data)):
            current_price = close_prices.iloc[i]

            # Execute trades
            if i == 0:
                # Handle initial position
                if positions.iloc[0] == 1:
                    # Buy signal on first day
                    shares_to_buy = (cash * (1 - self.commission)) / current_price
                    shares += shares_to_buy
                    cash = 0
                    trades += 1
            else:
                pos_change = position_changes.iloc[i]

                if pos_change > 0:  # Buy signal
                    # Buy with all available cash
                    shares_to_buy = (cash * (1 - self.commission)) / current_price
                    shares += shares_to_buy
                    cash = 0
                    trades += 1

                elif pos_change < 0:  # Sell signal
                    # Sell all shares
                    cash = shares * current_price * (1 - self.commission)
                    shares = 0
                    trades += 1

                # Calculate equity after trade
                equity.iloc[i] = cash + (shares * current_price)

        # Calculate returns
        returns = equity.pct_change().fillna(0)

        # Calculate total return
        final_equity = equity.iloc[-1]
        total_return = (final_equity - self.initial_capital) / self.initial_capital

        return {
            "equity_curve": equity,
            "returns": returns,
            "positions": positions,
            "trades": trades,
            "final_equity": final_equity,
            "total_return": total_return,
            "initial_capital": self.initial_capital
        }

    def get_parameters(self) -> Dict:
        """
        Get strategy parameters.

        Can be overridden by subclasses to return strategy-specific parameters.

        Returns:
            Dictionary of parameter names and values
        """
        return {
            "initial_capital": self.initial_capital,
            "commission": self.commission
        }

    def __str__(self) -> str:
        """String representation of the strategy."""
        params = self.get_parameters()
        param_str = ", ".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.name}({param_str})"
