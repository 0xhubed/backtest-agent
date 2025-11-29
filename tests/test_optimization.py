#!/usr/bin/env python3
"""
Test script for optimization tools.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tools.optimization_tools_adk import (
    optimize_sma_parameters,
    optimize_rsi_parameters,
    optimize_bollinger_bands_parameters
)


def test_optimize_sma():
    """Test SMA parameter optimization."""
    print("\n" + "="*80)
    print("TEST: Optimize SMA Parameters for High Sharpe Ratio")
    print("="*80)

    result = optimize_sma_parameters(
        symbol="BTC",
        start_date="2020-07-01",
        end_date="2021-07-01",
        target_metric="sharpe_ratio",
        target_value=1.5,  # Try to achieve Sharpe > 1.5
        short_period_range=[5, 10, 15, 20],
        long_period_range=[30, 40, 50, 60],
        max_iterations=20
    )

    print(f"✓ Success: {result['success']}")

    if result['success']:
        print(f"✓ Strategy: {result['strategy']}")
        print(f"✓ Target: {result['target_metric']} > {result['target_value']}")
        print(f"✓ Best Parameters: SMA({result['best_params']['short_period']},{result['best_params']['long_period']})")
        print(f"✓ Best Sharpe Ratio: {result['best_metric_value']:.2f}")
        print(f"✓ Target Met: {result['target_met']}")
        print(f"✓ Tested {result['total_tested']} combinations")

        best_metrics = result['best_metrics']
        print(f"\nBest Configuration Metrics:")
        print(f"  - Total Return: {best_metrics.get('total_return', 0)*100:.2f}%")
        print(f"  - Sharpe Ratio: {best_metrics.get('sharpe_ratio', 0):.2f}")
        print(f"  - Max Drawdown: {best_metrics.get('max_drawdown', 0):.2f}%")
        print(f"  - Trades: {result['trades']}")

        print("\nTop 3 Results:")
        for i, res in enumerate(result['all_results'][:3], 1):
            sharpe = res['metrics'].get('sharpe_ratio', 0)
            print(f"  {i}. SMA({res['short_period']},{res['long_period']}): Sharpe={sharpe:.2f}")

        print("✓ Test PASSED!")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
        print("✗ Test FAILED!")
        return False

    return True


def test_optimize_rsi_max_drawdown():
    """Test RSI optimization for low drawdown."""
    print("\n" + "="*80)
    print("TEST: Optimize RSI Parameters for Low Max Drawdown")
    print("="*80)

    result = optimize_rsi_parameters(
        symbol="BTC",
        start_date="2020-07-01",
        end_date="2021-07-01",
        target_metric="max_drawdown",
        target_value=15.0,  # Try to keep drawdown < 15%
        period_range=[7, 14, 21],
        lower_threshold_range=[25, 30],
        upper_threshold_range=[70, 75],
        max_iterations=20
    )

    print(f"✓ Success: {result['success']}")

    if result['success']:
        print(f"✓ Strategy: {result['strategy']}")
        print(f"✓ Target: abs({result['target_metric']}) < {result['target_value']}%")
        params = result['best_params']
        print(f"✓ Best Parameters: RSI(period={params['period']}, lower={params['lower_threshold']}, upper={params['upper_threshold']})")
        print(f"✓ Best Max Drawdown: {result['best_metric_value']:.2f}%")
        print(f"✓ Target Met: {result['target_met']}")
        print(f"✓ Tested {result['total_tested']} combinations")

        best_metrics = result['best_metrics']
        print(f"\nBest Configuration Metrics:")
        print(f"  - Total Return: {best_metrics.get('total_return', 0)*100:.2f}%")
        print(f"  - Sharpe Ratio: {best_metrics.get('sharpe_ratio', 0):.2f}")
        print(f"  - Max Drawdown: {best_metrics.get('max_drawdown', 0):.2f}%")

        print("✓ Test PASSED!")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
        print("✗ Test FAILED!")
        return False

    return True


def test_optimize_bollinger_bands():
    """Test Bollinger Bands optimization."""
    print("\n" + "="*80)
    print("TEST: Optimize Bollinger Bands Parameters")
    print("="*80)

    result = optimize_bollinger_bands_parameters(
        symbol="BTC",
        start_date="2020-07-01",
        end_date="2021-07-01",
        target_metric="sharpe_ratio",
        target_value=None,  # Just find best, no specific target
        period_range=[15, 20, 25],
        std_dev_range=[1.5, 2.0, 2.5],
        max_iterations=20
    )

    print(f"✓ Success: {result['success']}")

    if result['success']:
        print(f"✓ Strategy: {result['strategy']}")
        print(f"✓ Target: Maximize {result['target_metric']}")
        params = result['best_params']
        print(f"✓ Best Parameters: BollingerBands(period={params['period']}, std_dev={params['std_dev']})")
        print(f"✓ Best Sharpe Ratio: {result['best_metric_value']:.2f}")
        print(f"✓ Tested {result['total_tested']} combinations")

        print("✓ Test PASSED!")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
        print("✗ Test FAILED!")
        return False

    return True


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Optimization Tools Test Suite")
    print("="*80)
    print("\nThis will test parameter optimization for strategies...")

    try:
        test1 = test_optimize_sma()
        test2 = test_optimize_rsi_max_drawdown()
        test3 = test_optimize_bollinger_bands()

        if test1 and test2 and test3:
            print("\n" + "="*80)
            print("✓ ALL OPTIMIZATION TESTS PASSED!")
            print("="*80)
            print("\nOptimization tools are now available in the ADK agent!")
            print("\nExample queries:")
            print('  "Find the best SMA parameters for BTC with Sharpe ratio > 1.5"')
            print('  "Optimize RSI on ETH for max drawdown < 10%"')
            print('  "Find optimal Bollinger Bands parameters for BTC from 2020 to 2021"')
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
