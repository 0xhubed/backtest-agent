"""
ADK-compatible optimization tools for Backtest Agent.

These tools perform parameter optimization for trading strategies to find
the best parameters that meet user-defined goals (e.g., Sharpe > 1.5).
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from itertools import product

from src.strategies.sma_crossover import SMACrossover
from src.strategies.rsi_mean_reversion import RSIMeanReversion
from src.strategies.bollinger_bands import BollingerBands
from src.strategies.macd import MACD
from src.tools.risk_tools import compute_all_metrics


def optimize_sma_parameters(
    symbol: str,
    start_date: str,
    end_date: str,
    target_metric: str = "sharpe_ratio",
    target_value: Optional[float] = None,
    short_period_range: Optional[List[int]] = None,
    long_period_range: Optional[List[int]] = None,
    max_iterations: int = 50,
    initial_capital: float = 10000.0
) -> dict:
    """
    Optimize SMA Crossover strategy parameters to meet target goals.

    This tool performs a grid search over SMA period combinations to find
    the parameters that best meet your goals (e.g., highest Sharpe ratio,
    max drawdown < 15%, etc.).

    Args:
        symbol: Symbol to optimize (BTC, ETH, LTC, or XRP)
        start_date: Start date in YYYY-MM-DD format (e.g., "2021-01-01")
        end_date: End date in YYYY-MM-DD format (e.g., "2024-12-31")
        target_metric: Metric to optimize ("sharpe_ratio", "total_return", "max_drawdown", etc.)
        target_value: Optional target value (e.g., Sharpe > 1.5 means target_value=1.5)
        short_period_range: List of short periods to test (default: [5, 10, 15, 20, 25, 30])
        long_period_range: List of long periods to test (default: [30, 40, 50, 60, 70])
        max_iterations: Maximum number of combinations to test (default: 50)
        initial_capital: Starting capital in USD (default: 10000.0)

    Returns:
        Dictionary containing:
        - success (bool): Whether optimization completed
        - best_params (dict): Best parameters found
        - best_metrics (dict): Metrics for best parameters
        - all_results (list): All tested combinations sorted by target metric
        - total_tested (int): Number of combinations tested
        - target_met (bool): Whether target goal was achieved

    Example:
        >>> result = optimize_sma_parameters("BTC", "2021-01-01", "2022-01-01",
        ...                                   target_metric="sharpe_ratio", target_value=1.5)
        >>> print(f"Best SMA: ({result['best_params']['short_period']}, {result['best_params']['long_period']})")
    """
    try:
        # Fetch data first
        from src.tools.data_tools import load_ohlcv

        data_result = load_ohlcv(symbol, start_date, end_date)
        if not data_result['success']:
            return {
                'success': False,
                'error': f"Failed to load data: {data_result.get('error', 'Unknown error')}"
            }

        data = data_result['data']

        # Default parameter ranges
        if short_period_range is None:
            short_period_range = [5, 10, 15, 20, 25, 30]
        if long_period_range is None:
            long_period_range = [30, 40, 50, 60, 70, 100]

        # Generate all combinations
        combinations = list(product(short_period_range, long_period_range))
        # Filter: short must be < long
        combinations = [(s, l) for s, l in combinations if s < l]

        # Limit iterations
        if len(combinations) > max_iterations:
            combinations = combinations[:max_iterations]

        results = []

        for short, long in combinations:
            try:
                # Create and run strategy
                strategy = SMACrossover(
                    short_period=short,
                    long_period=long,
                    initial_capital=initial_capital
                )

                backtest_result = strategy.backtest(data)

                # Calculate metrics
                if 'equity_curve' in backtest_result and 'returns' in backtest_result:
                    metrics = compute_all_metrics(
                        returns=backtest_result['returns'],
                        equity_curve=backtest_result['equity_curve'],
                        risk_free_rate=0.02,
                        periods_per_year=252
                    )

                    # Convert to primitives
                    metrics_clean = {}
                    for key, value in metrics.items():
                        if value is None:
                            metrics_clean[key] = None
                        elif hasattr(value, 'days'):
                            metrics_clean[key] = int(value.days)
                        elif hasattr(value, 'item'):
                            metrics_clean[key] = float(value.item())
                        elif isinstance(value, (int, float)):
                            metrics_clean[key] = float(value)
                        else:
                            metrics_clean[key] = value

                    result_entry = {
                        'short_period': short,
                        'long_period': long,
                        'metrics': metrics_clean,
                        'trades': int(backtest_result.get('trades', 0))
                    }

                    results.append(result_entry)

            except Exception as e:
                # Skip this combination if it fails
                continue

        if not results:
            return {
                'success': False,
                'error': 'No valid parameter combinations found'
            }

        # Sort by target metric
        reverse_sort = target_metric != 'max_drawdown'  # Lower is better for drawdown
        results.sort(
            key=lambda x: x['metrics'].get(target_metric, float('-inf') if reverse_sort else float('inf')),
            reverse=reverse_sort
        )

        best = results[0]
        best_metric_value = best['metrics'].get(target_metric)

        # Check if target was met
        target_met = False
        if target_value is not None and best_metric_value is not None:
            if target_metric == 'max_drawdown':
                # For drawdown, lower (more negative) is better, but we want absolute value < target
                target_met = abs(best_metric_value) < target_value
            else:
                target_met = best_metric_value >= target_value

        return {
            'success': True,
            'symbol': symbol,
            'strategy': 'SMA Crossover',
            'target_metric': target_metric,
            'target_value': target_value,
            'best_params': {
                'short_period': best['short_period'],
                'long_period': best['long_period']
            },
            'best_metrics': best['metrics'],
            'best_metric_value': best_metric_value,
            'trades': best['trades'],
            'target_met': target_met,
            'total_tested': len(results),
            'all_results': results[:10]  # Return top 10 results
        }

    except Exception as e:
        return {
            'success': False,
            'error': f"Optimization failed: {str(e)}"
        }


def optimize_rsi_parameters(
    symbol: str,
    start_date: str,
    end_date: str,
    target_metric: str = "sharpe_ratio",
    target_value: Optional[float] = None,
    period_range: Optional[List[int]] = None,
    lower_threshold_range: Optional[List[int]] = None,
    upper_threshold_range: Optional[List[int]] = None,
    max_iterations: int = 50,
    initial_capital: float = 10000.0
) -> dict:
    """
    Optimize RSI Mean Reversion strategy parameters to meet target goals.

    This tool performs a grid search over RSI period and threshold combinations
    to find the parameters that best meet your goals.

    Args:
        symbol: Symbol to optimize (BTC, ETH, LTC, or XRP)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        target_metric: Metric to optimize ("sharpe_ratio", "max_drawdown", etc.)
        target_value: Optional target value to achieve
        period_range: List of RSI periods to test (default: [7, 14, 21, 28])
        lower_threshold_range: List of lower (oversold) thresholds (default: [20, 25, 30, 35])
        upper_threshold_range: List of upper (overbought) thresholds (default: [65, 70, 75, 80])
        max_iterations: Maximum combinations to test (default: 50)
        initial_capital: Starting capital in USD (default: 10000.0)

    Returns:
        Dictionary containing optimization results similar to optimize_sma_parameters

    Example:
        >>> result = optimize_rsi_parameters("BTC", "2021-01-01", "2022-01-01",
        ...                                   target_metric="max_drawdown", target_value=10.0)
    """
    try:
        # Fetch data
        from src.tools.data_tools import load_ohlcv

        data_result = load_ohlcv(symbol, start_date, end_date)
        if not data_result['success']:
            return {
                'success': False,
                'error': f"Failed to load data: {data_result.get('error', 'Unknown error')}"
            }

        data = data_result['data']

        # Default parameter ranges
        if period_range is None:
            period_range = [7, 14, 21, 28]
        if lower_threshold_range is None:
            lower_threshold_range = [20, 25, 30, 35]
        if upper_threshold_range is None:
            upper_threshold_range = [65, 70, 75, 80]

        # Generate all combinations
        combinations = list(product(period_range, lower_threshold_range, upper_threshold_range))
        # Filter: lower must be < upper
        combinations = [(p, lt, ut) for p, lt, ut in combinations if lt < ut]

        # Limit iterations
        if len(combinations) > max_iterations:
            combinations = combinations[:max_iterations]

        results = []

        for period, lower_threshold, upper_threshold in combinations:
            try:
                strategy = RSIMeanReversion(
                    period=period,
                    lower_threshold=lower_threshold,
                    upper_threshold=upper_threshold,
                    initial_capital=initial_capital
                )

                backtest_result = strategy.backtest(data)

                if 'equity_curve' in backtest_result and 'returns' in backtest_result:
                    metrics = compute_all_metrics(
                        returns=backtest_result['returns'],
                        equity_curve=backtest_result['equity_curve'],
                        risk_free_rate=0.02,
                        periods_per_year=252
                    )

                    metrics_clean = {}
                    for key, value in metrics.items():
                        if value is None:
                            metrics_clean[key] = None
                        elif hasattr(value, 'days'):
                            metrics_clean[key] = int(value.days)
                        elif hasattr(value, 'item'):
                            metrics_clean[key] = float(value.item())
                        elif isinstance(value, (int, float)):
                            metrics_clean[key] = float(value)
                        else:
                            metrics_clean[key] = value

                    result_entry = {
                        'period': period,
                        'lower_threshold': lower_threshold,
                        'upper_threshold': upper_threshold,
                        'metrics': metrics_clean,
                        'trades': int(backtest_result.get('trades', 0))
                    }

                    results.append(result_entry)

            except Exception as e:
                continue

        if not results:
            return {
                'success': False,
                'error': 'No valid parameter combinations found'
            }

        # Sort by target metric
        reverse_sort = target_metric != 'max_drawdown'
        results.sort(
            key=lambda x: x['metrics'].get(target_metric, float('-inf') if reverse_sort else float('inf')),
            reverse=reverse_sort
        )

        best = results[0]
        best_metric_value = best['metrics'].get(target_metric)

        target_met = False
        if target_value is not None and best_metric_value is not None:
            if target_metric == 'max_drawdown':
                target_met = abs(best_metric_value) < target_value
            else:
                target_met = best_metric_value >= target_value

        return {
            'success': True,
            'symbol': symbol,
            'strategy': 'RSI Mean Reversion',
            'target_metric': target_metric,
            'target_value': target_value,
            'best_params': {
                'period': best['period'],
                'lower_threshold': best['lower_threshold'],
                'upper_threshold': best['upper_threshold']
            },
            'best_metrics': best['metrics'],
            'best_metric_value': best_metric_value,
            'trades': best['trades'],
            'target_met': target_met,
            'total_tested': len(results),
            'all_results': results[:10]
        }

    except Exception as e:
        return {
            'success': False,
            'error': f"Optimization failed: {str(e)}"
        }


def optimize_bollinger_bands_parameters(
    symbol: str,
    start_date: str,
    end_date: str,
    target_metric: str = "sharpe_ratio",
    target_value: Optional[float] = None,
    period_range: Optional[List[int]] = None,
    std_dev_range: Optional[List[float]] = None,
    max_iterations: int = 50,
    initial_capital: float = 10000.0
) -> dict:
    """
    Optimize Bollinger Bands strategy parameters to meet target goals.

    Args:
        symbol: Symbol to optimize (BTC, ETH, LTC, or XRP)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        target_metric: Metric to optimize
        target_value: Optional target value to achieve
        period_range: List of periods to test (default: [10, 15, 20, 25, 30])
        std_dev_range: List of std deviations (default: [1.5, 2.0, 2.5, 3.0])
        max_iterations: Maximum combinations to test
        initial_capital: Starting capital in USD

    Returns:
        Dictionary containing optimization results
    """
    try:
        from src.tools.data_tools import load_ohlcv

        data_result = load_ohlcv(symbol, start_date, end_date)
        if not data_result['success']:
            return {
                'success': False,
                'error': f"Failed to load data: {data_result.get('error', 'Unknown error')}"
            }

        data = data_result['data']

        if period_range is None:
            period_range = [10, 15, 20, 25, 30]
        if std_dev_range is None:
            std_dev_range = [1.5, 2.0, 2.5, 3.0]

        combinations = list(product(period_range, std_dev_range))

        if len(combinations) > max_iterations:
            combinations = combinations[:max_iterations]

        results = []

        for period, std_dev in combinations:
            try:
                strategy = BollingerBands(
                    period=period,
                    std_dev=std_dev,
                    initial_capital=initial_capital
                )

                backtest_result = strategy.backtest(data)

                if 'equity_curve' in backtest_result and 'returns' in backtest_result:
                    metrics = compute_all_metrics(
                        returns=backtest_result['returns'],
                        equity_curve=backtest_result['equity_curve'],
                        risk_free_rate=0.02,
                        periods_per_year=252
                    )

                    metrics_clean = {}
                    for key, value in metrics.items():
                        if value is None:
                            metrics_clean[key] = None
                        elif hasattr(value, 'days'):
                            metrics_clean[key] = int(value.days)
                        elif hasattr(value, 'item'):
                            metrics_clean[key] = float(value.item())
                        elif isinstance(value, (int, float)):
                            metrics_clean[key] = float(value)
                        else:
                            metrics_clean[key] = value

                    result_entry = {
                        'period': period,
                        'std_dev': std_dev,
                        'metrics': metrics_clean,
                        'trades': int(backtest_result.get('trades', 0))
                    }

                    results.append(result_entry)

            except Exception as e:
                continue

        if not results:
            return {
                'success': False,
                'error': 'No valid parameter combinations found'
            }

        reverse_sort = target_metric != 'max_drawdown'
        results.sort(
            key=lambda x: x['metrics'].get(target_metric, float('-inf') if reverse_sort else float('inf')),
            reverse=reverse_sort
        )

        best = results[0]
        best_metric_value = best['metrics'].get(target_metric)

        target_met = False
        if target_value is not None and best_metric_value is not None:
            if target_metric == 'max_drawdown':
                target_met = abs(best_metric_value) < target_value
            else:
                target_met = best_metric_value >= target_value

        return {
            'success': True,
            'symbol': symbol,
            'strategy': 'Bollinger Bands',
            'target_metric': target_metric,
            'target_value': target_value,
            'best_params': {
                'period': best['period'],
                'std_dev': best['std_dev']
            },
            'best_metrics': best['metrics'],
            'best_metric_value': best_metric_value,
            'trades': best['trades'],
            'target_met': target_met,
            'total_tested': len(results),
            'all_results': results[:10]
        }

    except Exception as e:
        return {
            'success': False,
            'error': f"Optimization failed: {str(e)}"
        }
