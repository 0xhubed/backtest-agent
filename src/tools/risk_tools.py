"""
Risk metrics calculation tools for backtesting.

These tools compute various risk and performance metrics for trading strategies,
including Sharpe ratio, Sortino ratio, maximum drawdown, and more.
All metrics follow standard financial conventions with 252 trading days per year.
"""

import numpy as np
import pandas as pd
from typing import Dict, Union, Optional


def compute_sharpe_ratio(
    returns: Union[pd.Series, np.ndarray],
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252
) -> float:
    """
    Calculate annualized Sharpe ratio.

    Sharpe Ratio = (Mean Return - Risk Free Rate) / Std Dev of Returns * sqrt(periods_per_year)

    Args:
        returns: Series or array of returns (not equity curve)
        risk_free_rate: Annual risk-free rate (default 0.0)
        periods_per_year: Number of trading periods per year (252 for daily)

    Returns:
        Annualized Sharpe ratio

    Edge cases:
        - Zero volatility → returns 0.0 (not infinity)
        - Empty returns → returns 0.0
    """
    if len(returns) == 0:
        return 0.0

    returns = pd.Series(returns) if isinstance(returns, np.ndarray) else returns

    # Remove NaN values
    returns = returns.dropna()

    if len(returns) == 0:
        return 0.0

    # Calculate excess returns
    mean_return = returns.mean()
    std_return = returns.std()

    # Handle zero volatility case
    if std_return == 0 or np.isnan(std_return):
        return 0.0

    # Annualize
    daily_rf = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    sharpe = (mean_return - daily_rf) / std_return * np.sqrt(periods_per_year)

    return float(sharpe)


def compute_sortino_ratio(
    returns: Union[pd.Series, np.ndarray],
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252
) -> float:
    """
    Calculate annualized Sortino ratio.

    Similar to Sharpe but only penalizes downside volatility.
    Sortino Ratio = (Mean Return - Risk Free Rate) / Downside Deviation * sqrt(periods_per_year)

    Args:
        returns: Series or array of returns
        risk_free_rate: Annual risk-free rate (default 0.0)
        periods_per_year: Number of trading periods per year

    Returns:
        Annualized Sortino ratio

    Edge cases:
        - No negative returns → returns Sharpe ratio
        - Zero downside deviation → returns 0.0
    """
    if len(returns) == 0:
        return 0.0

    returns = pd.Series(returns) if isinstance(returns, np.ndarray) else returns
    returns = returns.dropna()

    if len(returns) == 0:
        return 0.0

    mean_return = returns.mean()

    # Calculate downside deviation (only negative returns)
    downside_returns = returns[returns < 0]

    if len(downside_returns) == 0:
        # No downside → return Sharpe ratio instead
        return compute_sharpe_ratio(returns, risk_free_rate, periods_per_year)

    downside_std = downside_returns.std()

    if downside_std == 0 or np.isnan(downside_std):
        return 0.0

    # Annualize
    daily_rf = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    sortino = (mean_return - daily_rf) / downside_std * np.sqrt(periods_per_year)

    return float(sortino)


def compute_max_drawdown(equity_curve: Union[pd.Series, np.ndarray]) -> Dict[str, float]:
    """
    Calculate maximum drawdown and related metrics.

    Max Drawdown = Largest peak-to-trough decline in equity curve

    Args:
        equity_curve: Series or array of portfolio values over time

    Returns:
        Dictionary containing:
            - max_drawdown: Maximum drawdown as a percentage (negative value)
            - max_drawdown_duration: Number of periods in drawdown
            - peak_idx: Index of the peak before max drawdown
            - trough_idx: Index of the trough (lowest point)
    """
    if len(equity_curve) == 0:
        return {
            'max_drawdown': 0.0,
            'max_drawdown_duration': 0,
            'peak_idx': None,
            'trough_idx': None
        }

    equity_curve = pd.Series(equity_curve) if isinstance(equity_curve, np.ndarray) else equity_curve
    equity_curve = equity_curve.dropna()

    if len(equity_curve) == 0:
        return {
            'max_drawdown': 0.0,
            'max_drawdown_duration': 0,
            'peak_idx': None,
            'trough_idx': None
        }

    # Calculate running maximum
    running_max = equity_curve.expanding().max()

    # Calculate drawdown at each point
    drawdown = (equity_curve - running_max) / running_max

    # Find maximum drawdown
    max_dd = drawdown.min()

    if pd.isna(max_dd):
        max_dd = 0.0

    # Find the trough (lowest point)
    trough_idx = drawdown.idxmin()

    # Find the peak before the trough
    if trough_idx is not None and len(equity_curve[:trough_idx]) > 0:
        peak_idx = equity_curve[:trough_idx].idxmax()
    else:
        peak_idx = None

    # Calculate drawdown duration
    if peak_idx is not None and trough_idx is not None:
        time_diff = trough_idx - peak_idx
        # Handle both integer indices and datetime indices
        if hasattr(time_diff, 'days'):  # Timedelta from datetime index
            duration = int(time_diff.days)
        else:  # Integer difference
            duration = int(time_diff)
    else:
        duration = 0

    return {
        'max_drawdown': float(max_dd),
        'max_drawdown_duration': duration,
        'peak_idx': peak_idx,
        'trough_idx': trough_idx
    }


def compute_calmar_ratio(
    returns: Union[pd.Series, np.ndarray],
    equity_curve: Union[pd.Series, np.ndarray],
    periods_per_year: int = 252
) -> float:
    """
    Calculate Calmar ratio.

    Calmar Ratio = Annualized Return / Absolute Max Drawdown

    Args:
        returns: Series or array of returns
        equity_curve: Series or array of portfolio values
        periods_per_year: Number of trading periods per year

    Returns:
        Calmar ratio

    Edge cases:
        - Zero max drawdown → returns 0.0
        - Negative returns with drawdown → returns negative ratio
    """
    if len(returns) == 0 or len(equity_curve) == 0:
        return 0.0

    returns = pd.Series(returns) if isinstance(returns, np.ndarray) else returns
    returns = returns.dropna()

    if len(returns) == 0:
        return 0.0

    # Annualized return
    mean_return = returns.mean()
    annualized_return = mean_return * periods_per_year

    # Max drawdown
    dd_info = compute_max_drawdown(equity_curve)
    max_dd = abs(dd_info['max_drawdown'])

    if max_dd == 0:
        return 0.0

    calmar = annualized_return / max_dd

    return float(calmar)


def compute_volatility(
    returns: Union[pd.Series, np.ndarray],
    periods_per_year: int = 252
) -> float:
    """
    Calculate annualized volatility.

    Args:
        returns: Series or array of returns
        periods_per_year: Number of trading periods per year

    Returns:
        Annualized volatility (standard deviation)
    """
    if len(returns) == 0:
        return 0.0

    returns = pd.Series(returns) if isinstance(returns, np.ndarray) else returns
    returns = returns.dropna()

    if len(returns) == 0:
        return 0.0

    std_return = returns.std()
    annualized_vol = std_return * np.sqrt(periods_per_year)

    return float(annualized_vol)


def compute_win_rate(returns: Union[pd.Series, np.ndarray]) -> float:
    """
    Calculate win rate (percentage of profitable periods).

    Args:
        returns: Series or array of returns

    Returns:
        Win rate as a percentage (0-100)
    """
    if len(returns) == 0:
        return 0.0

    returns = pd.Series(returns) if isinstance(returns, np.ndarray) else returns
    returns = returns.dropna()

    if len(returns) == 0:
        return 0.0

    winning_periods = (returns > 0).sum()
    total_periods = len(returns)

    win_rate = (winning_periods / total_periods) * 100

    return float(win_rate)


def compute_profit_factor(returns: Union[pd.Series, np.ndarray]) -> float:
    """
    Calculate profit factor.

    Profit Factor = Sum of Gains / Sum of Losses

    Args:
        returns: Series or array of returns

    Returns:
        Profit factor (>1 is profitable, <1 is losing)

    Edge cases:
        - No losses → returns infinity (capped at 999.0)
        - No gains → returns 0.0
    """
    if len(returns) == 0:
        return 0.0

    returns = pd.Series(returns) if isinstance(returns, np.ndarray) else returns
    returns = returns.dropna()

    if len(returns) == 0:
        return 0.0

    gains = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())

    if losses == 0:
        # No losses - very profitable
        return 999.0 if gains > 0 else 0.0

    if gains == 0:
        # No gains - all losses
        return 0.0

    profit_factor = gains / losses

    return float(profit_factor)


def compute_total_return(equity_curve: Union[pd.Series, np.ndarray]) -> float:
    """
    Calculate total return percentage.

    Total Return = (Final Value - Initial Value) / Initial Value * 100

    Args:
        equity_curve: Series or array of portfolio values

    Returns:
        Total return as a percentage
    """
    if len(equity_curve) == 0:
        return 0.0

    equity_curve = pd.Series(equity_curve) if isinstance(equity_curve, np.ndarray) else equity_curve
    equity_curve = equity_curve.dropna()

    if len(equity_curve) < 2:
        return 0.0

    initial_value = equity_curve.iloc[0]
    final_value = equity_curve.iloc[-1]

    if initial_value == 0:
        return 0.0

    total_return = ((final_value - initial_value) / initial_value) * 100

    return float(total_return)


def compute_annualized_return(
    equity_curve: Union[pd.Series, np.ndarray],
    periods_per_year: int = 252
) -> float:
    """
    Calculate annualized return (CAGR).

    Args:
        equity_curve: Series or array of portfolio values
        periods_per_year: Number of trading periods per year

    Returns:
        Annualized return as a percentage
    """
    if len(equity_curve) == 0:
        return 0.0

    equity_curve = pd.Series(equity_curve) if isinstance(equity_curve, np.ndarray) else equity_curve
    equity_curve = equity_curve.dropna()

    if len(equity_curve) < 2:
        return 0.0

    initial_value = equity_curve.iloc[0]
    final_value = equity_curve.iloc[-1]
    num_periods = len(equity_curve) - 1

    if initial_value == 0 or num_periods == 0:
        return 0.0

    # CAGR formula
    years = num_periods / periods_per_year
    cagr = ((final_value / initial_value) ** (1 / years) - 1) * 100

    return float(cagr)


def compute_all_metrics(
    returns: Union[pd.Series, np.ndarray],
    equity_curve: Union[pd.Series, np.ndarray],
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252
) -> Dict[str, float]:
    """
    Compute all risk and performance metrics at once.

    This is the main function used by RiskAgent to compute comprehensive metrics.

    Args:
        returns: Series or array of returns
        equity_curve: Series or array of portfolio values
        risk_free_rate: Annual risk-free rate (default 0.0)
        periods_per_year: Number of trading periods per year

    Returns:
        Dictionary containing all metrics:
            - total_return: Total return percentage
            - annualized_return: CAGR percentage
            - sharpe_ratio: Annualized Sharpe ratio
            - sortino_ratio: Annualized Sortino ratio
            - calmar_ratio: Calmar ratio
            - max_drawdown: Maximum drawdown percentage
            - max_drawdown_duration: Drawdown duration in periods
            - volatility: Annualized volatility
            - win_rate: Win rate percentage
            - profit_factor: Profit factor
    """
    returns = pd.Series(returns) if isinstance(returns, np.ndarray) else returns
    equity_curve = pd.Series(equity_curve) if isinstance(equity_curve, np.ndarray) else equity_curve

    # Compute max drawdown info
    dd_info = compute_max_drawdown(equity_curve)

    metrics = {
        'total_return': compute_total_return(equity_curve),
        'annualized_return': compute_annualized_return(equity_curve, periods_per_year),
        'sharpe_ratio': compute_sharpe_ratio(returns, risk_free_rate, periods_per_year),
        'sortino_ratio': compute_sortino_ratio(returns, risk_free_rate, periods_per_year),
        'calmar_ratio': compute_calmar_ratio(returns, equity_curve, periods_per_year),
        'max_drawdown': dd_info['max_drawdown'] * 100,  # Convert to percentage
        'max_drawdown_duration': dd_info['max_drawdown_duration'],
        'volatility': compute_volatility(returns, periods_per_year),
        'win_rate': compute_win_rate(returns),
        'profit_factor': compute_profit_factor(returns),
    }

    return metrics


# Tool function wrapper for ADK agents
def calculate_risk_metrics(
    returns: list,
    equity_curve: list,
    risk_free_rate: float = 0.0
) -> dict:
    """
    Tool function wrapper for computing risk metrics.

    This function is designed to be called by ADK agents as a tool.

    Args:
        returns: List of daily returns
        equity_curve: List of portfolio values over time
        risk_free_rate: Annual risk-free rate (default 0.0)

    Returns:
        Dictionary of all risk metrics
    """
    try:
        metrics = compute_all_metrics(
            returns=np.array(returns),
            equity_curve=np.array(equity_curve),
            risk_free_rate=risk_free_rate,
            periods_per_year=252
        )

        return {
            'success': True,
            'metrics': metrics,
            'error': None
        }
    except Exception as e:
        return {
            'success': False,
            'metrics': None,
            'error': str(e)
        }
