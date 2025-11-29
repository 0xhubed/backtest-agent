# Backtest Agent - Project Description (1500 words max)

## Executive Summary

Backtest Agent is a trading strategy analysis system built with Google ADK that allows users to request cryptocurrency backtests through natural language. By combining Gemini's natural language understanding with 15 specialized tools, it aims to simplify the process of prototyping and evaluating trading strategies compared to traditional manual coding approaches.

## Problem Statement

Quantitative traders and financial analysts face significant productivity bottlenecks when developing and testing trading strategies:

**Manual Coding Overhead**: Each strategy variation requires custom implementation in Python, R, or specialized backtesting frameworks. Even simple modifications like changing a moving average period from 20 to 50 require code changes, testing, and debugging.

**Repetitive Calculations**: Risk metrics (Sharpe ratio, maximum drawdown, Sortino ratio, etc.) must be computed manually for each test. This involves understanding complex formulas, handling edge cases, and ensuring calculation accuracy.

**Parameter Optimization**: Finding optimal strategy configurations requires exhaustive trial-and-error. Testing a grid of 50 parameter combinations means running 50 separate backtests and manually comparing results.

**Multi-Asset Analysis**: Comparing how a strategy performs across different assets (Bitcoin vs Ethereum, for example) multiplies the workload, as each asset requires separate data loading, backtesting, and analysis.

**Impact**: Strategy development often takes hours or days when it could potentially be faster. This can slow down experimentation and create barriers for those who understand markets but lack coding skills.

## Solution: Natural Language Trading Analysis

Backtest Agent addresses these challenges through an agent-tool architecture powered by Google ADK and Gemini.

### How It Works

Users interact with the system through natural language queries like:
- "What cryptocurrencies are available for backtesting?"
- "Backtest SMA(20,50) on Bitcoin from 2020 to 2021"
- "Compare SMA vs RSI strategies on BTC and ETH"
- "Optimize RSI parameters to achieve Sharpe ratio above 1.5"

The root agent (powered by Gemini) automatically:
1. **Parses** user intent and extracts parameters (symbols, strategies, date ranges, optimization targets)
2. **Validates** inputs against dataset availability and technical requirements
3. **Selects and sequences** appropriate tools from its 15-tool toolkit
4. **Executes** the backtesting workflow (data fetch → strategy execution → risk analysis)
5. **Generates** human-friendly reports with actionable insights and recommendations

### Core Architecture

Backtest Agent uses Google ADK's agent framework with a tool-based architecture:

```
User (Natural Language)
    ↓
Root Agent (Gemini)
    ↓
Tool Selection & Orchestration
    ↓
┌─────────────┬──────────────┬────────────────┐
│ Data Tools  │ Backtest Tools│ Optimization  │
│ (6 tools)   │ (6 tools)     │ Tools (3)     │
└─────────────┴──────────────┴────────────────┘
    ↓
Results → Natural Language Report
```

This design leverages Google ADK's strengths:
- Gemini handles natural language understanding and orchestration
- Tools implement domain-specific financial logic
- ADK provides session management and observability
- No manual agent coordination required

## Technical Implementation

### 1. Tool Suite (15 ADK-Compatible Tools)

**Data Tools (6 tools)**:
- `get_available_symbols()`: Lists supported cryptocurrencies (BTC, ETH, LTC, XRP)
- `check_data_availability()`: Verifies data exists for requested symbols and date ranges
- `get_recommended_date_ranges()`: Suggests valid timeframes accounting for indicator warmup periods
- `fetch_ohlcv_data()`: Loads OHLCV (Open, High, Low, Close, Volume) data for single symbol
- `fetch_multiple_symbols()`: Parallel data loading for multiple assets (4x speedup)
- `validate_backtest_parameters()`: Pre-execution validation to prevent errors

**Backtest Tools (6 tools)**:
- `execute_sma_backtest()`: SMA Crossover strategy (trend following)
- `execute_rsi_backtest()`: RSI Mean Reversion strategy (momentum-based)
- `execute_bollinger_bands_backtest()`: Bollinger Bands strategy (volatility-based)
- `execute_macd_backtest()`: MACD strategy (momentum indicator)
- `execute_buy_and_hold_backtest()`: Buy & Hold baseline for comparison
- `compare_strategies()`: Multi-strategy comparison with rankings

**Optimization Tools (3 tools)**:
- `optimize_sma_parameters()`: Grid search for optimal SMA periods
- `optimize_rsi_parameters()`: Grid search for RSI thresholds
- `optimize_bollinger_bands_parameters()`: Grid search for Bollinger Band parameters

Each tool is designed as a pure function with:
- Explicit parameters (no hidden state)
- Structured dictionary returns (JSON-serializable for ADK)
- Comprehensive docstrings for Gemini's understanding
- Error handling with descriptive messages
- Independent testability

### 2. Strategy Implementations (5 Professional Strategies)

**SMA Crossover** (Trend Following):
- Buy when short-period moving average crosses above long-period MA
- Sell when short MA crosses below long MA
- Parameters: short_period (5-30), long_period (30-100)
- Best for: Trending markets

**RSI Mean Reversion** (Momentum):
- Buy when RSI drops below lower threshold (oversold)
- Sell when RSI rises above upper threshold (overbought)
- Parameters: period (7-28), lower_threshold (20-35), upper_threshold (65-80)
- Best for: Range-bound markets

**Bollinger Bands** (Volatility):
- Buy on lower band touch (price mean reversion)
- Sell on upper band touch
- Parameters: period (10-30), std_dev (1.5-3.0)
- Best for: Markets with clear volatility patterns

**MACD** (Momentum):
- Buy when MACD line crosses above signal line
- Sell when MACD crosses below signal line
- Parameters: fast_period (8-16), slow_period (20-30), signal_period (7-11)
- Best for: Identifying trend changes

**Buy & Hold** (Baseline):
- Buy at start, hold until end
- No parameters
- Purpose: Benchmark to compare active strategies against passive investment

All strategies:
- Inherit from `BaseStrategy` abstract class
- Implement vectorized signal generation (no loops for performance)
- Calculate comprehensive risk metrics automatically
- Support commission and slippage modeling for realistic results

### 3. Risk Analysis

Every backtest returns comprehensive risk metrics:

- **Sharpe Ratio**: Risk-adjusted returns (annualized, 252 trading days)
- **Sortino Ratio**: Similar to Sharpe but only penalizes downside volatility
- **Calmar Ratio**: Annualized return divided by maximum drawdown
- **Maximum Drawdown**: Largest peak-to-trough decline in equity
- **Volatility**: Annualized standard deviation of returns
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profit divided by gross loss
- **Total Return**: Overall percentage gain/loss
- **Annualized Return**: Compound annual growth rate

All metrics handle edge cases properly:
- Zero volatility → Sharpe ratio = 0 (not infinity)
- No negative returns → Sortino ratio = Sharpe ratio
- No trades executed → Clear error messages

### 4. Parameter Optimization

The optimization tools use grid search to find optimal parameters:

**Process**:
1. Generate all parameter combinations within specified ranges
2. Filter invalid combinations (e.g., short MA must be < long MA)
3. Test each combination via backtesting
4. Rank results by target metric (Sharpe, return, drawdown, etc.)
5. Return best parameters plus top 10 alternatives

**Features**:
- Supports target constraints: "Find parameters where Sharpe > 1.5"
- Iteration limits prevent timeouts (max 50 combinations)
- Returns full metrics for all tested configurations
- Target achievement tracking (did we meet the goal?)

**Example**: Optimizing SMA on Bitcoin tests 36 combinations (6 short periods × 6 long periods) in ~3-5 seconds and identifies the configuration with highest Sharpe ratio.

### 5. Agent Behavior

Gemini provides orchestration and contextual awareness:

**Dataset Awareness**: The Kaggle cryptocurrency dataset ends on 2021-07-06. When users request recent dates, the agent:
- Proactively validates date ranges
- Suggests valid alternatives
- Explains why certain dates aren't available

**Warmup Requirements**: Technical indicators require historical data. For SMA(200), you need 200+ days of warmup. The agent:
- Automatically calculates required warmup periods
- Adjusts date ranges accordingly
- Warns users about insufficient data

**Actionable Insights**: Beyond reporting numbers, the agent:
- Explains what metrics mean ("Sharpe > 1 is good, > 2 is excellent")
- Provides trading recommendations based on results
- Compares strategies and ranks by performance
- Suggests parameter improvements if results are poor

## Technology Stack

- **Framework**: Google ADK 1.19.0+ (Agent Development Kit)
- **LLM**: Gemini via Google AI Studio / Vertex AI
- **Language**: Python 3.11+
- **Data Source**: Kaggle Cryptocurrency Historical Prices (2017-2021, daily OHLCV)
- **Key Libraries**: pandas (data processing), numpy (numerical computations), matplotlib (visualization)
- **Interface**: ADK Web UI (localhost:8000) - chat-based interaction
- **Testing**: pytest (33 tests, 100% passing)
- **Deployment**: Cloud Run ready (FastAPI wrapper included)

## Results & Validation

**Test Coverage**: 33 unit and integration tests with 100% pass rate
- 14 data tool tests (validation, loading, parallel fetching)
- 19 strategy tests (signal generation, backtesting, risk calculations)

**Performance**:
- Data loading: 4x speedup (parallel vs sequential for 4 symbols)
- Single backtest: 50-100ms execution time
- Parameter optimization: 50 combinations in 3-5 seconds

**Accuracy**:
- Risk metrics: Closely match manual calculations (within ±0.01%)
- Signal generation: Produces expected results for tested scenarios
- Parameter optimization: Identifies parameter sets with improved metrics

## Key Features & Potential Value

**Technical Features**:
1. **Natural language interface**: Users can express requests in plain English rather than code
2. **Gemini-powered orchestration**: Sequences workflows automatically based on user intent
3. **Tool-based architecture**: Modular components that can be tested and extended
4. **Contextual validation**: Checks data availability and parameter validity before execution

**Potential Benefits**:
- **Faster iteration**: Reduces time needed to test strategy variations
- **Less manual coding**: Automates repetitive backtesting tasks
- **Lower barrier to entry**: Makes backtesting accessible to users with limited programming experience
- **Easier experimentation**: Simplifies testing multiple parameter combinations

**Enterprise Agents Track Alignment**:
- **Data analysis**: Automates risk metric computation across strategies
- **Decision support**: Provides comparative analysis with rankings
- **Workflow automation**: Handles backtesting workflows through conversation
- **Accessibility**: Opens quantitative analysis to broader user base

## Potential Use Cases

**Quantitative Trading Firms**: Strategy prototyping and initial validation

**Financial Advisors**: Historical backtesting to explore strategy behavior

**Crypto Hedge Funds**: Multi-asset strategy comparison

**Educational Institutions**: Teaching trading concepts with reduced programming requirements

**Individual Traders**: Exploring trading ideas without extensive coding

## Future Enhancements

- **Real-time data integration**: Live trading signals from current market data
- **Portfolio optimization**: Multi-asset allocation strategies with correlation analysis
- **Machine learning integration**: Bayesian optimization for parameter search
- **Custom strategy builder**: Visual interface for users to define their own trading logic
- **Walk-forward analysis**: More robust validation through rolling time windows
- **Multi-timeframe analysis**: Test strategies across different timeframes (daily, hourly, etc.)

## Conclusion

Backtest Agent demonstrates how Google ADK and Gemini can be applied to domain-specific workflows. By combining natural language understanding with specialized tools, it provides a more accessible approach to trading strategy development. The system has been tested with a comprehensive test suite and includes the components needed for deployment, though real-world usage would require additional validation and refinement.

**Word Count**: ~1,485 words
