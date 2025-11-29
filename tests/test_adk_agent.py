"""
Test script for BackTestPilot ADK Agent.

This script tests the ADK-based agent without needing actual API credentials.
It validates that the agent structure is correct and tools are properly configured.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Test that all ADK components can be imported."""
    print("Testing imports...")

    try:
        from google.adk import Agent
        print("✓ Google ADK Agent class imported")
    except ImportError as e:
        print(f"✗ Failed to import Google ADK: {e}")
        return False

    try:
        from backtest_agent.agent import root_agent
        print("✓ Root agent imported")
    except ImportError as e:
        print(f"✗ Failed to import root agent: {e}")
        return False

    try:
        from src.tools.data_tools_adk import (
            fetch_ohlcv_data,
            fetch_multiple_symbols,
            get_available_symbols
        )
        print("✓ Data tools imported")
    except ImportError as e:
        print(f"✗ Failed to import data tools: {e}")
        return False

    try:
        from src.tools.backtest_tools_adk import (
            execute_sma_backtest,
            execute_rsi_backtest,
            compare_strategies
        )
        print("✓ Backtest tools imported")
    except ImportError as e:
        print(f"✗ Failed to import backtest tools: {e}")
        return False

    return True


def test_agent_structure():
    """Test that the agent is properly structured."""
    print("\nTesting agent structure...")

    from backtest_agent.agent import root_agent

    # Check agent properties
    assert root_agent.name == "backtest_orchestrator", "Agent name mismatch"
    print(f"✓ Agent name: {root_agent.name}")

    assert root_agent.model == "gemini-2.0-flash", "Model mismatch"
    print(f"✓ Model: {root_agent.model}")

    # Check tools are attached
    assert len(root_agent.tools) > 0, "No tools attached to agent"
    print(f"✓ Tools attached: {len(root_agent.tools)}")

    # List all tools
    print("\nAvailable tools:")
    for i, tool in enumerate(root_agent.tools, 1):
        tool_name = tool.__name__ if hasattr(tool, '__name__') else str(tool)
        print(f"  {i}. {tool_name}")

    return True


def test_tools_directly():
    """Test that tools can be called directly."""
    print("\nTesting tools directly...")

    # Test get_available_symbols (no data required)
    from src.tools.data_tools_adk import get_available_symbols

    result = get_available_symbols()
    assert 'symbols' in result, "Missing 'symbols' key"
    assert len(result['symbols']) > 0, "No symbols returned"
    print(f"✓ get_available_symbols: {result['symbols']}")

    # Test check_data_availability
    from src.tools.data_tools_adk import check_data_availability

    result = check_data_availability("BTC")
    assert 'symbol' in result, "Missing 'symbol' key"
    assert 'available' in result, "Missing 'available' key"
    print(f"✓ check_data_availability('BTC'): Available={result['available']}")

    if not result['available']:
        print("  ⚠ Warning: BTC data not available. You need to download the Kaggle dataset.")
        print("    See: https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory")

    return True


def test_adk_cli():
    """Test ADK CLI availability."""
    print("\nTesting ADK CLI...")

    import subprocess

    try:
        result = subprocess.run(
            ['adk', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print(f"✓ ADK CLI available: {result.stdout.strip()}")
            print("\nYou can now run:")
            print("  adk web              # Launch web UI at http://localhost:8000")
            print("  adk run root_agent   # Run in terminal mode")
            return True
        else:
            print("✗ ADK CLI not working properly")
            return False

    except FileNotFoundError:
        print("✗ ADK CLI not found in PATH")
        print("  Make sure you're in the Python 3.11 virtual environment:")
        print("  source venv311/bin/activate")
        return False
    except Exception as e:
        print(f"✗ Error testing ADK CLI: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("BackTestPilot ADK Agent Test Suite")
    print("=" * 70)

    tests = [
        ("Imports", test_imports),
        ("Agent Structure", test_agent_structure),
        ("Direct Tool Calls", test_tools_directly),
        ("ADK CLI", test_adk_cli),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status:8} {test_name}")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n✓ All tests passed! Your ADK agent is ready to use.")
        print("\nNext steps:")
        print("1. Copy .env.adk to .env and add your Google API key")
        print("2. Download Kaggle dataset to data/raw/")
        print("3. Run: adk web")
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
