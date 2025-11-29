"""
Trading strategies for Backtest Agent.

Provides various technical trading strategies including trend-following,
mean reversion, and momentum strategies.
"""

from src.strategies.base_strategy import BaseStrategy
from src.strategies.sma_crossover import SMACrossover
from src.strategies.rsi_mean_reversion import RSIMeanReversion
from src.strategies.buy_and_hold import BuyAndHold
from src.strategies.bollinger_bands import BollingerBands
from src.strategies.macd import MACD

__all__ = [
    # Base class
    'BaseStrategy',

    # Strategy classes
    'SMACrossover',
    'RSIMeanReversion',
    'BuyAndHold',
    'BollingerBands',
    'MACD',
]
