#!/usr/bin/env python3
"""
Test script to verify BackTestPilot ADK tools are working correctly.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tools.data_tools_adk import (
    get_available_symbols,
    check_data_availability,
    get_recommended_date_ranges,
    fetch_ohlcv_data
)

from src.tools.backtest_tools_adk import (
    execute_sma_backtest,
    execute_buy_and_hold_backtest
)


def test_available_symbols():
    """Test getting available symbols."""
    print("\n" + "="*80)
    print("TEST 1: Get Available Symbols")
    print("="*80)

    result = get_available_symbols()
    print(f"✓ Symbols: {result['symbols']}")
    print(f"✓ Count: {result['count']}")
    print(f"✓ Description: {result['description']}")

    assert result['count'] == 4, "Should have 4 symbols"
    assert 'BTC' in result['symbols'], "Should include BTC"
    print("✓ Test passed!")


def test_data_availability():
    """Test checking data availability."""
    print("\n" + "="*80)
    print("TEST 2: Check Data Availability")
    print("="*80)

    result = check_data_availability("BTC")
    print(f"✓ Symbol: {result['symbol']}")
    print(f"✓ Available: {result['available']}")

    if result['available']:
        print(f"✓ Date range: {result['date_range']}")
        print(f"✓ Record count: {result['record_count']}")
        print(f"✓ Message: {result['message']}")

    assert result['available'], "BTC data should be available"
    print("✓ Test passed!")


def test_recommended_date_ranges():
    """Test getting recommended date ranges."""
    print("\n" + "="*80)
    print("TEST 3: Get Recommended Date Ranges")
    print("="*80)

    result = get_recommended_date_ranges("BTC")
    print(f"✓ Symbol: {result['symbol']}")
    print(f"✓ Data start: {result['data_start']}")
    print(f"✓ Data end: {result['data_end']}")
    print(f"✓ Total days: {result['total_days']}")
    print(f"✓ Message: {result['message']}")

    print("\nRecommended ranges:")
    for name, info in result['recommended_ranges'].items():
        print(f"  - {name}: {info['start']} to {info['end']}")
        print(f"    {info['description']}")

    assert result['available'], "BTC data should be available"
    assert 'recommended_ranges' in result, "Should have recommended ranges"
    print("✓ Test passed!")


def test_fetch_data():
    """Test fetching OHLCV data."""
    print("\n" + "="*80)
    print("TEST 4: Fetch OHLCV Data")
    print("="*80)

    # Use date range with at least 200 days for indicator warmup
    result = fetch_ohlcv_data("BTC", "2020-07-01", "2021-07-01")

    print(f"✓ Success: {result['success']}")
    print(f"✓ Symbol: {result['symbol']}")

    if result['success']:
        print(f"✓ Data shape: {result['data_shape']}")
        print(f"✓ Data columns: {result['data_columns']}")
        print(f"✓ Data info: {result['data_info']}")

    assert result['success'], "Should successfully fetch data"
    assert result['data_shape'][0] > 0, "Should have data rows"
    print("✓ Test passed!")


def test_sma_backtest():
    """Test SMA backtest."""
    print("\n" + "="*80)
    print("TEST 5: Execute SMA Backtest")
    print("="*80)

    # Use recommended date range from previous test
    result = execute_sma_backtest(
        symbol="BTC",
        start_date="2020-07-01",
        end_date="2021-07-01",
        short_period=20,
        long_period=50,
        initial_capital=10000.0
    )

    print(f"✓ Success: {result['success']}")

    if result['success']:
        print(f"✓ Symbol: {result['symbol']}")
        print(f"✓ Strategy: {result['strategy']}")
        print(f"✓ Total Return: {result['metrics']['total_return_pct']:.2f}%")
        print(f"✓ Sharpe Ratio: {result['metrics']['sharpe_ratio']:.2f}")
        print(f"✓ Max Drawdown: {result['metrics']['max_drawdown']:.2f}%")
        print(f"✓ Trades: {result['trades']}")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")

    assert result['success'], "Backtest should succeed"
    print("✓ Test passed!")


def test_buy_hold_backtest():
    """Test Buy & Hold backtest."""
    print("\n" + "="*80)
    print("TEST 6: Execute Buy & Hold Backtest")
    print("="*80)

    result = execute_buy_and_hold_backtest(
        symbol="BTC",
        start_date="2020-07-01",
        end_date="2021-07-01",
        initial_capital=10000.0
    )

    print(f"✓ Success: {result['success']}")

    if result['success']:
        print(f"✓ Symbol: {result['symbol']}")
        print(f"✓ Strategy: {result['strategy']}")
        print(f"✓ Total Return: {result['metrics']['total_return_pct']:.2f}%")
        print(f"✓ Sharpe Ratio: {result['metrics']['sharpe_ratio']:.2f}")
        print(f"✓ Max Drawdown: {result['metrics']['max_drawdown']:.2f}%")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")

    assert result['success'], "Backtest should succeed"
    print("✓ Test passed!")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("BackTestPilot ADK Tools Test Suite")
    print("="*80)

    try:
        test_available_symbols()
        test_data_availability()
        test_recommended_date_ranges()
        test_fetch_data()
        test_sma_backtest()
        test_buy_hold_backtest()

        print("\n" + "="*80)
        print("✓ ALL TESTS PASSED!")
        print("="*80)
        print("\nThe agent tools are working correctly.")
        print("You can now run: adk web")
        print("\nTry these queries in the web UI:")
        print("  1. What date ranges are available for BTC backtesting?")
        print("  2. Backtest SMA(20,50) on BTC from 2020-07-01 to 2021-07-01")
        print("  3. Compare SMA vs Buy&Hold on BTC")

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
