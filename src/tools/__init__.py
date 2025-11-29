"""
Tools module for Backtest Agent.

This module contains all tool functions used by agents for:
- Data loading and processing
- Risk metrics calculation
- Parameter optimization
- Visualization
"""

# Data tools
from src.tools.data_tools import (
    load_ohlcv,
    get_supported_symbols,
    validate_date_range
)

# Risk tools
from src.tools.risk_tools import (
    compute_sharpe_ratio,
    compute_sortino_ratio,
    compute_max_drawdown,
    compute_calmar_ratio,
    compute_volatility,
    compute_win_rate,
    compute_profit_factor,
    compute_total_return,
    compute_annualized_return,
    compute_all_metrics,
    calculate_risk_metrics
)

# Optimization tools
from src.tools.optimization_tools_adk import (
    optimize_sma_parameters,
    optimize_rsi_parameters,
    optimize_bollinger_bands_parameters
)

__all__ = [
    # Data tools
    'load_ohlcv',
    'get_supported_symbols',
    'validate_date_range',
    # Risk tools
    'compute_sharpe_ratio',
    'compute_sortino_ratio',
    'compute_max_drawdown',
    'compute_calmar_ratio',
    'compute_volatility',
    'compute_win_rate',
    'compute_profit_factor',
    'compute_total_return',
    'compute_annualized_return',
    'compute_all_metrics',
    'calculate_risk_metrics',
    # Optimization tools
    'optimize_sma_parameters',
    'optimize_rsi_parameters',
    'optimize_bollinger_bands_parameters',
]
