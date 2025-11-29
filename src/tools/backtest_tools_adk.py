"""
ADK-compatible backtesting tools for Backtest Agent.

These tools execute trading strategies and return backtest results.
They wrap the existing strategy classes to provide a clean ADK interface.
"""

from typing import Dict, List, Optional
import pandas as pd

from src.strategies.sma_crossover import SMACrossover
from src.strategies.rsi_mean_reversion import RSIMeanReversion
from src.strategies.bollinger_bands import BollingerBands
from src.strategies.buy_and_hold import BuyAndHold
from src.tools.risk_tools import compute_all_metrics


def execute_sma_backtest(
    symbol: str,
    start_date: str,
    end_date: str,
    short_period: int = 20,
    long_period: int = 50,
    initial_capital: float = 10000.0
) -> dict:
    """
    Executes a Simple Moving Average (SMA) crossover strategy backtest.

    This strategy generates buy signals when the short-term SMA crosses above
    the long-term SMA (golden cross) and sell signals when it crosses below
    (death cross). The tool automatically fetches the required data.

    Args:
        symbol: Symbol to backtest (BTC, ETH, LTC, or XRP)
        start_date: Start date in YYYY-MM-DD format (e.g., "2021-01-01")
        end_date: End date in YYYY-MM-DD format (e.g., "2024-12-31")
        short_period: Period for short-term SMA in days (default: 20)
        long_period: Period for long-term SMA in days (default: 50)
        initial_capital: Starting capital in USD (default: 10000.0)

    Returns:
        Dictionary containing:
        - success (bool): Whether backtest completed successfully
        - symbol (str): Symbol that was backtested
        - strategy (str): Strategy name and parameters
        - metrics (dict): Performance metrics (returns, Sharpe, drawdown, etc.)
        - trades (int): Number of trades executed
        - error (str): Error message if unsuccessful

    Example:
        >>> result = execute_sma_backtest("BTC", "2021-01-01", "2024-12-31", short_period=10, long_period=30)
        >>> if result['success']:
        >>>     print(f"Sharpe Ratio: {result['metrics']['sharpe_ratio']:.2f}")
    """
    try:
        # Fetch data first
        from src.tools.data_tools import load_ohlcv

        data_result = load_ohlcv(symbol, start_date, end_date)
        if not data_result['success']:
            return {
                'success': False,
                'symbol': symbol,
                'strategy': f"SMA({short_period},{long_period})",
                'error': f"Failed to load data: {data_result.get('error', 'Unknown error')}"
            }

        data = data_result['data']

        # Create strategy
        strategy = SMACrossover(
            short_period=short_period,
            long_period=long_period,
            initial_capital=initial_capital
        )

        # Run backtest
        backtest_result = strategy.backtest(data)

        # Extract key metrics
        metrics = {
            'initial_capital': float(backtest_result['initial_capital']),
            'final_equity': float(backtest_result['final_equity']),
            'total_return': float(backtest_result['total_return']),
            'total_return_pct': float(backtest_result['total_return'] * 100),
        }

        # Calculate risk metrics
        if 'equity_curve' in backtest_result and 'returns' in backtest_result:
            equity_curve = backtest_result['equity_curve']
            returns = backtest_result['returns']

            try:
                risk_metrics = compute_all_metrics(
                    returns=returns,
                    equity_curve=equity_curve,
                    risk_free_rate=0.02,
                    periods_per_year=252
                )
                # Convert all numpy/pandas types to Python primitives
                for key, value in risk_metrics.items():
                    if value is None:
                        metrics[key] = None
                    elif hasattr(value, 'days'):  # Timedelta object
                        metrics[key] = int(value.days)
                    elif hasattr(value, 'item'):  # numpy scalar
                        metrics[key] = float(value.item())
                    elif isinstance(value, (int, float)):
                        metrics[key] = float(value)
                    else:
                        metrics[key] = str(value)  # Fallback to string
            except Exception as e:
                # If risk metrics fail, continue without them
                metrics['risk_metrics_error'] = str(e)

        return {
            'success': True,
            'symbol': symbol,
            'strategy': f"SMA({short_period},{long_period})",
            'strategy_type': 'SMA Crossover',
            'parameters': {
                'short_period': int(short_period),
                'long_period': int(long_period),
                'initial_capital': float(initial_capital)
            },
            'metrics': metrics,
            'trades': int(backtest_result.get('trades', 0)),
            'summary': f"SMA({short_period},{long_period}) on {symbol}: Return={metrics['total_return_pct']:.2f}%, Trades={backtest_result.get('trades', 0)}"
        }

    except Exception as e:
        return {
            'success': False,
            'symbol': symbol,
            'strategy': f"SMA({short_period},{long_period})",
            'error': f"Backtest failed: {str(e)}"
        }


def execute_rsi_backtest(
    symbol: str,
    start_date: str,
    end_date: str,
    period: int = 14,
    lower_threshold: int = 30,
    upper_threshold: int = 70,
    initial_capital: float = 10000.0
) -> dict:
    """
    Executes an RSI (Relative Strength Index) mean reversion strategy backtest.

    This strategy buys when RSI falls below the lower threshold (oversold) and
    sells when RSI rises above the upper threshold (overbought). The tool
    automatically fetches the required data.

    Args:
        symbol: Symbol to backtest (BTC, ETH, LTC, or XRP)
        start_date: Start date in YYYY-MM-DD format (e.g., "2021-01-01")
        end_date: End date in YYYY-MM-DD format (e.g., "2024-12-31")
        period: RSI calculation period in days (default: 14)
        lower_threshold: RSI buy threshold for oversold (default: 30)
        upper_threshold: RSI sell threshold for overbought (default: 70)
        initial_capital: Starting capital in USD (default: 10000.0)

    Returns:
        Dictionary containing:
        - success (bool): Whether backtest completed successfully
        - symbol (str): Symbol that was backtested
        - strategy (str): Strategy name and parameters
        - metrics (dict): Performance metrics
        - trades (int): Number of trades executed
        - error (str): Error message if unsuccessful

    Example:
        >>> result = execute_rsi_backtest("ETH", "2021-01-01", "2024-12-31", period=14, lower_threshold=30, upper_threshold=70)
        >>> if result['success']:
        >>>     print(f"Total Return: {result['metrics']['total_return_pct']:.2f}%")
    """
    try:
        # Fetch data first
        from src.tools.data_tools import load_ohlcv

        data_result = load_ohlcv(symbol, start_date, end_date)
        if not data_result['success']:
            return {
                'success': False,
                'symbol': symbol,
                'strategy': f"RSI({period},{lower_threshold}-{upper_threshold})",
                'error': f"Failed to load data: {data_result.get('error', 'Unknown error')}"
            }

        data = data_result['data']

        # Create strategy
        strategy = RSIMeanReversion(
            period=period,
            lower_threshold=lower_threshold,
            upper_threshold=upper_threshold,
            initial_capital=initial_capital
        )

        # Run backtest
        backtest_result = strategy.backtest(data)

        # Extract key metrics
        metrics = {
            'initial_capital': float(backtest_result['initial_capital']),
            'final_equity': float(backtest_result['final_equity']),
            'total_return': float(backtest_result['total_return']),
            'total_return_pct': float(backtest_result['total_return'] * 100),
        }

        # Calculate risk metrics
        if 'equity_curve' in backtest_result and 'returns' in backtest_result:
            equity_curve = backtest_result['equity_curve']
            returns = backtest_result['returns']

            try:
                risk_metrics = compute_all_metrics(
                    returns=returns,
                    equity_curve=equity_curve,
                    risk_free_rate=0.02,
                    periods_per_year=252
                )
                # Convert all numpy/pandas types to Python primitives
                for key, value in risk_metrics.items():
                    if value is None:
                        metrics[key] = None
                    elif hasattr(value, 'days'):  # Timedelta object
                        metrics[key] = int(value.days)
                    elif hasattr(value, 'item'):  # numpy scalar
                        metrics[key] = float(value.item())
                    elif isinstance(value, (int, float)):
                        metrics[key] = float(value)
                    else:
                        metrics[key] = str(value)  # Fallback to string
            except Exception as e:
                # If risk metrics fail, continue without them
                metrics['risk_metrics_error'] = str(e)

        return {
            'success': True,
            'symbol': symbol,
            'strategy': f"RSI({period},{lower_threshold}-{upper_threshold})",
            'strategy_type': 'RSI Mean Reversion',
            'parameters': {
                'period': period,
                'lower_threshold': lower_threshold,
                'upper_threshold': upper_threshold,
                'initial_capital': initial_capital
            },
            'metrics': metrics,
            'trades': backtest_result.get('trades', 0),
            'summary': f"RSI({period},{lower_threshold}-{upper_threshold}) on {symbol}: Return={metrics['total_return_pct']:.2f}%, Trades={backtest_result.get('trades', 0)}"
        }

    except Exception as e:
        return {
            'success': False,
            'symbol': symbol,
            'strategy': f"RSI({period},{lower_threshold}-{upper_threshold})",
            'error': f"Backtest failed: {str(e)}"
        }


def execute_buy_and_hold_backtest(
    symbol: str,
    start_date: str,
    end_date: str,
    initial_capital: float = 10000.0
) -> dict:
    """
    Executes a simple buy-and-hold baseline strategy backtest.

    This strategy buys at the beginning and holds until the end of the period.
    Useful as a benchmark to compare active strategies against. The tool
    automatically fetches the required data.

    Args:
        symbol: Symbol to backtest (BTC, ETH, LTC, or XRP)
        start_date: Start date in YYYY-MM-DD format (e.g., "2021-01-01")
        end_date: End date in YYYY-MM-DD format (e.g., "2024-12-31")
        initial_capital: Starting capital in USD (default: 10000.0)

    Returns:
        Dictionary containing:
        - success (bool): Whether backtest completed successfully
        - symbol (str): Symbol that was backtested
        - strategy (str): Strategy name
        - metrics (dict): Performance metrics
        - trades (int): Number of trades (always 1 for buy-and-hold)
        - error (str): Error message if unsuccessful

    Example:
        >>> result = execute_buy_and_hold_backtest("BTC", "2021-01-01", "2024-12-31")
        >>> print(f"Buy & Hold Return: {result['metrics']['total_return_pct']:.2f}%")
    """
    try:
        # Fetch data first
        from src.tools.data_tools import load_ohlcv

        data_result = load_ohlcv(symbol, start_date, end_date)
        if not data_result['success']:
            return {
                'success': False,
                'symbol': symbol,
                'strategy': "BuyAndHold",
                'error': f"Failed to load data: {data_result.get('error', 'Unknown error')}"
            }

        data = data_result['data']

        # Create strategy
        strategy = BuyAndHold(initial_capital=initial_capital)

        # Run backtest
        backtest_result = strategy.backtest(data)

        # Extract key metrics
        metrics = {
            'initial_capital': float(backtest_result['initial_capital']),
            'final_equity': float(backtest_result['final_equity']),
            'total_return': float(backtest_result['total_return']),
            'total_return_pct': float(backtest_result['total_return'] * 100),
        }

        # Calculate risk metrics
        if 'equity_curve' in backtest_result and 'returns' in backtest_result:
            equity_curve = backtest_result['equity_curve']
            returns = backtest_result['returns']

            try:
                risk_metrics = compute_all_metrics(
                    returns=returns,
                    equity_curve=equity_curve,
                    risk_free_rate=0.02,
                    periods_per_year=252
                )
                # Convert all numpy/pandas types to Python primitives
                for key, value in risk_metrics.items():
                    if value is None:
                        metrics[key] = None
                    elif hasattr(value, 'days'):  # Timedelta object
                        metrics[key] = int(value.days)
                    elif hasattr(value, 'item'):  # numpy scalar
                        metrics[key] = float(value.item())
                    elif isinstance(value, (int, float)):
                        metrics[key] = float(value)
                    else:
                        metrics[key] = str(value)  # Fallback to string
            except Exception as e:
                # If risk metrics fail, continue without them
                metrics['risk_metrics_error'] = str(e)

        return {
            'success': True,
            'symbol': symbol,
            'strategy': "BuyAndHold",
            'strategy_type': 'Buy and Hold',
            'parameters': {
                'initial_capital': initial_capital
            },
            'metrics': metrics,
            'trades': backtest_result.get('trades', 0),
            'summary': f"Buy & Hold on {symbol}: Return={metrics['total_return_pct']:.2f}%"
        }

    except Exception as e:
        return {
            'success': False,
            'symbol': symbol,
            'strategy': "BuyAndHold",
            'error': f"Backtest failed: {str(e)}"
        }


def compare_strategies(
    symbol: str,
    start_date: str,
    end_date: str,
    strategies: List[str],
    initial_capital: float = 10000.0
) -> dict:
    """
    Compares multiple trading strategies on the same dataset.

    Runs backtests for all specified strategies and ranks them by Sharpe ratio
    and total return. Useful for strategy selection and validation. The tool
    automatically fetches the required data.

    Args:
        symbol: Symbol to backtest on (BTC, ETH, LTC, or XRP)
        start_date: Start date in YYYY-MM-DD format (e.g., "2021-01-01")
        end_date: End date in YYYY-MM-DD format (e.g., "2024-12-31")
        strategies: List of strategy names to compare. Supported: ["SMA", "RSI", "BollingerBands", "MACD", "BuyAndHold"]
        initial_capital: Starting capital for all strategies (default: 10000.0)

    Returns:
        Dictionary containing:
        - success (bool): Whether comparison completed
        - symbol (str): Symbol that was tested
        - results (list): List of individual strategy results
        - rankings (dict): Strategies ranked by different metrics
        - best_strategy (str): Best performing strategy by Sharpe ratio
        - summary (str): Human-readable comparison summary

    Example:
        >>> result = compare_strategies("BTC", "2021-01-01", "2021-06-30", ["SMA", "RSI", "BollingerBands", "MACD", "BuyAndHold"])
        >>> print(f"Best strategy: {result['best_strategy']}")
        >>> for rank in result['rankings']['by_sharpe']:
        >>>     print(f"{rank['strategy']}: Sharpe={rank['sharpe']:.2f}")
    """
    try:
        results = []

        # Execute each strategy
        for strategy_name in strategies:
            if strategy_name.upper() == "SMA":
                result = execute_sma_backtest(symbol, start_date, end_date, initial_capital=initial_capital)
            elif strategy_name.upper() == "RSI":
                result = execute_rsi_backtest(symbol, start_date, end_date, initial_capital=initial_capital)
            elif strategy_name.upper() in ["BOLLINGERBANDS", "BOLLINGER_BANDS", "BOLLINGER", "BB"]:
                result = execute_bollinger_bands_backtest(symbol, start_date, end_date, initial_capital=initial_capital)
            elif strategy_name.upper() == "MACD":
                result = execute_macd_backtest(symbol, start_date, end_date, initial_capital=initial_capital)
            elif strategy_name.upper() in ["BUYANDHOLD", "BUY_AND_HOLD", "BNH"]:
                result = execute_buy_and_hold_backtest(symbol, start_date, end_date, initial_capital=initial_capital)
            else:
                # Skip unknown strategies
                continue

            if result['success']:
                results.append(result)

        if not results:
            return {
                'success': False,
                'symbol': symbol,
                'error': 'No valid strategies to compare'
            }

        # Rank by different metrics
        rankings = {
            'by_sharpe': sorted(
                results,
                key=lambda x: x['metrics'].get('sharpe_ratio', -999),
                reverse=True
            ),
            'by_return': sorted(
                results,
                key=lambda x: x['metrics'].get('total_return', -999),
                reverse=True
            ),
            'by_calmar': sorted(
                results,
                key=lambda x: x['metrics'].get('calmar_ratio', -999),
                reverse=True
            )
        }

        best_strategy = rankings['by_sharpe'][0]['strategy']

        # Create summary table
        summary_lines = [
            f"\n{'='*70}",
            f"Strategy Comparison for {symbol}",
            f"{'='*70}",
            f"{'Strategy':<20} {'Return':>10} {'Sharpe':>8} {'MaxDD':>8} {'Trades':>8}",
            f"{'-'*70}"
        ]

        for rank in rankings['by_return']:
            summary_lines.append(
                f"{rank['strategy']:<20} "
                f"{rank['metrics']['total_return_pct']:>9.2f}% "
                f"{rank['metrics'].get('sharpe_ratio', 0):>8.2f} "
                f"{rank['metrics'].get('max_drawdown', 0):>7.1f}% "
                f"{rank['trades']:>8}"
            )

        summary_lines.append(f"{'='*70}")
        summary_lines.append(f"Best Strategy (by Sharpe): {best_strategy}")

        return {
            'success': True,
            'symbol': symbol,
            'strategy_count': len(results),
            'results': results,
            'rankings': {
                'by_sharpe': [
                    {
                        'strategy': r['strategy'],
                        'sharpe': r['metrics'].get('sharpe_ratio', 0),
                        'return': r['metrics']['total_return_pct']
                    }
                    for r in rankings['by_sharpe']
                ],
                'by_return': [
                    {
                        'strategy': r['strategy'],
                        'return': r['metrics']['total_return_pct'],
                        'sharpe': r['metrics'].get('sharpe_ratio', 0)
                    }
                    for r in rankings['by_return']
                ]
            },
            'best_strategy': best_strategy,
            'summary': '\n'.join(summary_lines)
        }

    except Exception as e:
        return {
            'success': False,
            'symbol': symbol,
            'error': f"Strategy comparison failed: {str(e)}"
        }


def execute_bollinger_bands_backtest(
    symbol: str,
    start_date: str,
    end_date: str,
    period: int = 20,
    std_dev: float = 2.0,
    initial_capital: float = 10000.0
) -> dict:
    """
    Executes a Bollinger Bands mean reversion strategy backtest.

    Bollinger Bands use a moving average with upper and lower bands set at
    standard deviations. The strategy buys when price touches the lower band
    (oversold) and sells when it touches the upper band (overbought).

    Args:
        symbol: Symbol to backtest (BTC, ETH, LTC, or XRP)
        start_date: Start date in YYYY-MM-DD format (e.g., "2021-01-01")
        end_date: End date in YYYY-MM-DD format (e.g., "2024-12-31")
        period: Moving average period in days (default: 20)
        std_dev: Number of standard deviations for bands (default: 2.0)
        initial_capital: Starting capital in USD (default: 10000.0)

    Returns:
        Dictionary containing:
        - success (bool): Whether backtest completed successfully
        - symbol (str): Symbol that was backtested
        - strategy (str): Strategy name and parameters
        - metrics (dict): Performance metrics
        - trades (int): Number of trades executed
        - error (str): Error message if unsuccessful

    Example:
        >>> result = execute_bollinger_bands_backtest("BTC", "2021-01-01", "2024-12-31")
        >>> if result['success']:
        >>>     print(f"Total Return: {result['metrics']['total_return_pct']:.2f}%")
    """
    try:
        # Fetch data first
        from src.tools.data_tools import load_ohlcv

        data_result = load_ohlcv(symbol, start_date, end_date)
        if not data_result['success']:
            return {
                'success': False,
                'symbol': symbol,
                'strategy': f"BollingerBands({period},{std_dev})",
                'error': f"Failed to load data: {data_result.get('error', 'Unknown error')}"
            }

        data = data_result['data']

        # Create strategy
        strategy = BollingerBands(
            period=period,
            std_dev=std_dev,
            initial_capital=initial_capital
        )

        # Run backtest
        backtest_result = strategy.backtest(data)

        # Extract key metrics
        metrics = {
            'initial_capital': float(backtest_result['initial_capital']),
            'final_equity': float(backtest_result['final_equity']),
            'total_return': float(backtest_result['total_return']),
            'total_return_pct': float(backtest_result['total_return'] * 100),
        }

        # Calculate risk metrics
        if 'equity_curve' in backtest_result and 'returns' in backtest_result:
            equity_curve = backtest_result['equity_curve']
            returns = backtest_result['returns']

            try:
                risk_metrics = compute_all_metrics(
                    returns=returns,
                    equity_curve=equity_curve,
                    risk_free_rate=0.02,
                    periods_per_year=252
                )
                # Convert types to primitives
                for key, value in risk_metrics.items():
                    if value is None:
                        metrics[key] = None
                    elif hasattr(value, 'days'):  # Timedelta
                        metrics[key] = int(value.days)
                    elif hasattr(value, 'item'):  # numpy scalar
                        metrics[key] = float(value.item())
                    elif isinstance(value, (int, float)):
                        metrics[key] = float(value)
                    else:
                        metrics[key] = value

            except Exception as e:
                metrics['risk_metrics_error'] = str(e)

        return {
            'success': True,
            'symbol': symbol,
            'strategy': f"BollingerBands({period},{std_dev})",
            'metrics': metrics,
            'trades': int(backtest_result.get('trades', 0))
        }

    except Exception as e:
        return {
            'success': False,
            'symbol': symbol,
            'strategy': f"BollingerBands({period},{std_dev})",
            'error': f"Bollinger Bands backtest failed: {str(e)}"
        }


def execute_macd_backtest(
    symbol: str,
    start_date: str,
    end_date: str,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
    initial_capital: float = 10000.0
) -> dict:
    """
    Executes a MACD (Moving Average Convergence Divergence) strategy backtest.

    MACD is a trend-following momentum indicator. The strategy generates buy
    signals when the MACD line crosses above the signal line (bullish) and
    sell signals when it crosses below (bearish).

    Args:
        symbol: Symbol to backtest (BTC, ETH, LTC, or XRP)
        start_date: Start date in YYYY-MM-DD format (e.g., "2021-01-01")
        end_date: End date in YYYY-MM-DD format (e.g., "2024-12-31")
        fast_period: Fast EMA period in days (default: 12)
        slow_period: Slow EMA period in days (default: 26)
        signal_period: Signal line EMA period in days (default: 9)
        initial_capital: Starting capital in USD (default: 10000.0)

    Returns:
        Dictionary containing:
        - success (bool): Whether backtest completed successfully
        - symbol (str): Symbol that was backtested
        - strategy (str): Strategy name and parameters
        - metrics (dict): Performance metrics
        - trades (int): Number of trades executed
        - error (str): Error message if unsuccessful

    Example:
        >>> result = execute_macd_backtest("BTC", "2021-01-01", "2024-12-31")
        >>> if result['success']:
        >>>     print(f"Sharpe Ratio: {result['metrics']['sharpe_ratio']:.2f}")
    """
    try:
        # Fetch data first
        from src.tools.data_tools import load_ohlcv
        from src.strategies.macd import MACD

        data_result = load_ohlcv(symbol, start_date, end_date)
        if not data_result['success']:
            return {
                'success': False,
                'symbol': symbol,
                'strategy': f"MACD({fast_period},{slow_period},{signal_period})",
                'error': f"Failed to load data: {data_result.get('error', 'Unknown error')}"
            }

        data = data_result['data']

        # Create strategy
        strategy = MACD(
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
            initial_capital=initial_capital
        )

        # Run backtest
        backtest_result = strategy.backtest(data)

        # Extract key metrics
        metrics = {
            'initial_capital': float(backtest_result['initial_capital']),
            'final_equity': float(backtest_result['final_equity']),
            'total_return': float(backtest_result['total_return']),
            'total_return_pct': float(backtest_result['total_return'] * 100),
        }

        # Calculate risk metrics
        if 'equity_curve' in backtest_result and 'returns' in backtest_result:
            equity_curve = backtest_result['equity_curve']
            returns = backtest_result['returns']

            try:
                risk_metrics = compute_all_metrics(
                    returns=returns,
                    equity_curve=equity_curve,
                    risk_free_rate=0.02,
                    periods_per_year=252
                )
                # Convert types to primitives
                for key, value in risk_metrics.items():
                    if value is None:
                        metrics[key] = None
                    elif hasattr(value, 'days'):  # Timedelta
                        metrics[key] = int(value.days)
                    elif hasattr(value, 'item'):  # numpy scalar
                        metrics[key] = float(value.item())
                    elif isinstance(value, (int, float)):
                        metrics[key] = float(value)
                    else:
                        metrics[key] = value

            except Exception as e:
                metrics['risk_metrics_error'] = str(e)

        return {
            'success': True,
            'symbol': symbol,
            'strategy': f"MACD({fast_period},{slow_period},{signal_period})",
            'metrics': metrics,
            'trades': int(backtest_result.get('trades', 0))
        }

    except Exception as e:
        return {
            'success': False,
            'symbol': symbol,
            'strategy': f"MACD({fast_period},{slow_period},{signal_period})",
            'error': f"MACD backtest failed: {str(e)}"
        }
