#!/usr/bin/env python3
"""
Test script for new Bollinger Bands and MACD strategies.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tools.backtest_tools_adk import (
    execute_bollinger_bands_backtest,
    execute_macd_backtest
)


def test_bollinger_bands():
    """Test Bollinger Bands backtest."""
    print("\n" + "="*80)
    print("TEST: Bollinger Bands Backtest")
    print("="*80)

    result = execute_bollinger_bands_backtest(
        symbol="BTC",
        start_date="2020-07-01",
        end_date="2021-07-01",
        period=20,
        std_dev=2.0,
        initial_capital=10000.0
    )

    print(f"✓ Success: {result['success']}")

    if result['success']:
        print(f"✓ Symbol: {result['symbol']}")
        print(f"✓ Strategy: {result['strategy']}")
        print(f"✓ Total Return: {result['metrics']['total_return_pct']:.2f}%")
        print(f"✓ Sharpe Ratio: {result['metrics'].get('sharpe_ratio', 'N/A')}")
        print(f"✓ Max Drawdown: {result['metrics'].get('max_drawdown', 'N/A')}%")
        print(f"✓ Trades: {result['trades']}")
        print("✓ Test PASSED!")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
        print("✗ Test FAILED!")
        return False

    return True


def test_macd():
    """Test MACD backtest."""
    print("\n" + "="*80)
    print("TEST: MACD Backtest")
    print("="*80)

    result = execute_macd_backtest(
        symbol="BTC",
        start_date="2020-07-01",
        end_date="2021-07-01",
        fast_period=12,
        slow_period=26,
        signal_period=9,
        initial_capital=10000.0
    )

    print(f"✓ Success: {result['success']}")

    if result['success']:
        print(f"✓ Symbol: {result['symbol']}")
        print(f"✓ Strategy: {result['strategy']}")
        print(f"✓ Total Return: {result['metrics']['total_return_pct']:.2f}%")
        print(f"✓ Sharpe Ratio: {result['metrics'].get('sharpe_ratio', 'N/A')}")
        print(f"✓ Max Drawdown: {result['metrics'].get('max_drawdown', 'N/A')}%")
        print(f"✓ Trades: {result['trades']}")
        print("✓ Test PASSED!")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
        print("✗ Test FAILED!")
        return False

    return True


if __name__ == "__main__":
    print("\n" + "="*80)
    print("New Strategies Test Suite")
    print("="*80)

    try:
        test1 = test_bollinger_bands()
        test2 = test_macd()

        if test1 and test2:
            print("\n" + "="*80)
            print("✓ ALL TESTS PASSED!")
            print("="*80)
            print("\nBollinger Bands and MACD strategies are now available!")
            print("\nYou can use them in the ADK agent:")
            print('  "Test Bollinger Bands on BTC from 2020 to 2021"')
            print('  "Backtest MACD on ETH from 2020 to 2021"')
            print('  "Compare SMA vs RSI vs Bollinger Bands vs MACD on BTC"')
        else:
            print("\n" + "="*80)
            print("✗ SOME TESTS FAILED")
            print("="*80)
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
