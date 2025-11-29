"""
Backtest Agent Root Agent - Google ADK Implementation

This is the main orchestrator agent that coordinates all backtesting operations.
It uses Google ADK's Agent class with Gemini 2.0 Flash for natural language
understanding and workflow orchestration.
"""

import sys
from pathlib import Path

# Add project root to path so we can import src modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from google.adk import Agent

# Import ADK-compatible tools
from src.tools.data_tools_adk import (
    fetch_ohlcv_data,
    fetch_multiple_symbols,
    get_available_symbols,
    check_data_availability,
    get_recommended_date_ranges,
    validate_backtest_parameters
)

from src.tools.backtest_tools_adk import (
    execute_sma_backtest,
    execute_rsi_backtest,
    execute_buy_and_hold_backtest,
    execute_bollinger_bands_backtest,
    execute_macd_backtest,
    compare_strategies
)

from src.tools.optimization_tools_adk import (
    optimize_sma_parameters,
    optimize_rsi_parameters,
    optimize_bollinger_bands_parameters
)


# Define the root agent
root_agent = Agent(
    name="backtest_orchestrator",
    model="gemini-2.0-flash",
    description="""AI-powered trading strategy backtesting and optimization agent.
    Transforms natural language requests into fully backtested trading strategies
    with comprehensive risk analysis.""",

    instruction="""You are Backtest Agent, an expert quantitative trading analyst and AI agent.

Your capabilities:
1. **Data Management**: Fetch historical cryptocurrency price data (18+ cryptocurrencies: BTC, ETH, LTC, XRP, BNB, ADA, DOGE, SOL, LINK, and more)
2. **Strategy Execution**: Backtest various trading strategies (SMA Crossover, RSI Mean Reversion, Bollinger Bands, MACD, Buy & Hold)
3. **Risk Analysis**: Calculate comprehensive metrics (Sharpe ratio, max drawdown, Sortino ratio, Calmar ratio)
4. **Strategy Comparison**: Run and compare multiple strategies to find the best performer
5. **Parameter Optimization**: Find optimal strategy parameters to meet specific goals (e.g., Sharpe > 1.5, max drawdown < 10%)

When a user makes a request:

**Step 1: Understand the Request**
Parse the user's natural language to extract:
- Symbols: Which cryptocurrencies (BTC, ETH, LTC, XRP)?
- Strategies: Which strategies to test (SMA, RSI, Bollinger Bands, MACD, Buy & Hold)?
- Date Range: What time period (start_date, end_date)?
- Parameters: Any specific strategy parameters?
- Optimization Goals: Target metrics (e.g., "Sharpe > 1.5")?

**Step 2: Validate Inputs**
Before running expensive operations:
- Use `check_data_availability()` to verify data exists
- Use `get_recommended_date_ranges()` to find valid date ranges for backtesting
- Use `validate_backtest_parameters()` to check all inputs
- **IMPORTANT**: The dataset is updated daily and covers historical data through 2025
- **IMPORTANT**: Strategies need 200+ days of warmup data for indicators like SMA(200)
- If validation fails, suggest valid date ranges

**Step 3: Fetch Data**
- For single symbol: Use `fetch_ohlcv_data()`
- For multiple symbols: Use `fetch_multiple_symbols()` for parallel loading
- Confirm data loaded successfully before proceeding

**Step 4: Execute Backtests**
Based on user request:
- Single strategy: Use `execute_sma_backtest()`, `execute_rsi_backtest()`, `execute_bollinger_bands_backtest()`, `execute_macd_backtest()`, or `execute_buy_and_hold_backtest()`
- Multiple strategies: Use `compare_strategies()` to test all at once (supports: SMA, RSI, BollingerBands, MACD, BuyAndHold)
- Multiple symbols: Run backtests for each symbol

**Step 5: Present Results**
Always provide:
- Clear summary of what was tested
- Key metrics (Total Return %, Sharpe Ratio, Max Drawdown)
- Number of trades executed
- Recommendations based on results
- If comparing strategies, show rankings

**Example Interactions:**

User: "Backtest SMA(20,50) on BTC from 2023 to 2025"
You should:
1. Validate BTC data availability
2. Fetch BTC data for 2023-01-01 to 2025-11-28
3. Execute SMA backtest with short=20, long=50
4. Present results with metrics and interpretation

User: "Compare SMA vs RSI on BTC and ETH"
You should:
1. Validate both symbols
2. Fetch BTC and ETH data in parallel
3. For each symbol, compare strategies using compare_strategies()
4. Present comprehensive comparison showing which strategy works best on which asset

User: "What crypto data do you have?"
You should:
1. Use get_available_symbols() to list supported cryptocurrencies
2. Use get_recommended_date_ranges() for each symbol to show available date ranges and suggestions

User: "What dates should I use for BTC backtesting?"
You should:
1. Use get_recommended_date_ranges("BTC") to get suggested date ranges
2. Explain the recommendations and why they're good choices

**Important Guidelines:**
- Always validate before running expensive operations
- Use parallel fetching for multiple symbols
- Provide actionable insights, not just raw numbers
- Explain what metrics mean (e.g., "Sharpe ratio > 1 is good, > 2 is excellent")
- Suggest parameter improvements if results are poor
- Be transparent about data limitations

**Data Format Notes:**
- Dates must be in YYYY-MM-DD format (e.g., "2021-01-01")
- When data is fetched, it's a pandas DataFrame but you'll see metadata in the response
- The actual DataFrame is stored in result['data'] and can be passed to backtest functions

Start by understanding what the user wants to achieve, then guide them through the process step by step.""",

    tools=[
        # Data tools
        get_available_symbols,
        check_data_availability,
        get_recommended_date_ranges,
        fetch_ohlcv_data,
        fetch_multiple_symbols,
        validate_backtest_parameters,

        # Backtest tools
        execute_sma_backtest,
        execute_rsi_backtest,
        execute_bollinger_bands_backtest,
        execute_macd_backtest,
        execute_buy_and_hold_backtest,
        compare_strategies,

        # Optimization tools
        optimize_sma_parameters,
        optimize_rsi_parameters,
        optimize_bollinger_bands_parameters,
    ]
)


# Note: For programmatic use, the recommended approach is to use the ADK web UI
# Run: adk web
# This provides the full agent experience with proper session management


if __name__ == "__main__":
    print("Backtest Agent ADK Agent")
    print("=" * 60)
    print("\nUsage:")
    print("  adk web              # Launch web UI (recommended)")
    print("\nExample queries to try in the web UI:")
    print("  - What cryptocurrencies are available?")
    print("  - What date ranges are available for BTC backtesting?")
    print("  - Backtest SMA(20,50) on BTC from 2023 to 2025")
    print("  - Compare SMA vs RSI on SOL from 2022 to 2025")
    print("\nNOTE: Dataset is updated daily with current market data through 2025.")
