# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**BackTestPilot** is a multi-agent AI system built with Google ADK that transforms natural-language trading requests into fully backtested, risk-analyzed strategies with automated parameter optimization. This is a capstone project for the Google AI Agents Intensive Course (Enterprise Agents track).

**Core Value**: Enables quantitative traders to prototype strategies 10x faster through natural language rather than manual coding.

## Architecture Philosophy

### Multi-Agent System Design

The system uses a **hierarchical agent orchestration** pattern with three execution modes:

1. **Sequential Flow**: UserAgent → DataAgent → BacktestAgent → RiskAgent → ReportAgent
2. **Parallel Flow**: Multiple assets/strategies processed concurrently (critical for performance)
3. **Loop Flow**: OptimizationAgent iterates until targets met or max iterations reached

**Key Architectural Principle**: Each agent is autonomous and communicates through well-defined tool interfaces. Agents never directly call each other—the UserAgent orchestrates all workflows.

### Agent Responsibilities

- **UserAgent** (Gemini 2.0 Flash): NLP parsing, orchestration, conversation state management
- **DataAgent**: Parallel OHLCV data fetching with caching
- **ValidationAgent**: Input validation (date ranges, parameters, symbol existence)
- **BacktestAgent**: Parallel strategy execution across multiple assets
- **RiskAgent**: Parallel computation of risk metrics (Sharpe, drawdown, etc.)
- **OptimizationAgent**: Loop agent for goal-driven parameter refinement
- **ReportAgent** (Gemini 2.0 Flash): Natural language report generation with visualizations

### Tool Layer

Tools are **pure functions** that agents invoke. They should:
- Accept explicit parameters (no hidden state)
- Return structured dictionaries (JSON-serializable)
- Handle errors gracefully with descriptive messages
- Be independently testable

**Critical**: Tools are the only layer that touches external systems (data files, databases, APIs).

### Memory Architecture

**Experiment Memory Bank** (SQLite):
- Every backtest run is persisted with full metadata
- Enables queries like "What was our best BTC strategy last week?"
- Schema: `experiments(id, timestamp, user_query, symbols, strategies, parameters, results, execution_time, agent_trace)`

**Session State** (InMemorySessionService):
- Tracks conversation context within a single user session
- Used for multi-turn conversations (e.g., "Now try it with ETH")

## Development Commands

### Environment Setup

```bash
# Initial setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Download Kaggle dataset
kaggle datasets download -d sudalairajkumar/cryptocurrencypricehistory
unzip cryptocurrencypricehistory.zip -d data/raw/
```

### Running the System

```bash
# CLI mode
python src/main.py --query "Backtest SMA(20,50) on BTC from 2021 to 2024"

# Interactive mode
python src/main.py --interactive

# API server (development)
uvicorn deployment.api:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_tools.py -v

# Run single test
pytest tests/test_tools.py::test_load_ohlcv -v

# Test with coverage
pytest --cov=src --cov-report=html
```

### Deployment

```bash
# Docker build and run
docker build -t backtestpilot:latest .
docker run -p 8080:8080 --env-file .env backtestpilot:latest

# Google Cloud Run deployment
gcloud builds submit --tag gcr.io/PROJECT_ID/backtestpilot
gcloud run deploy backtestpilot \
  --image gcr.io/PROJECT_ID/backtestpilot \
  --platform managed \
  --region us-central1
```

## Critical Implementation Details

### Parallel Execution Strategy

When implementing parallel agents, use this pattern:

```python
# Correct: Parallel execution for independent tasks
results = await asyncio.gather(
    backtest_agent.run(strategy="SMA", symbol="BTC"),
    backtest_agent.run(strategy="SMA", symbol="ETH"),
    backtest_agent.run(strategy="RSI", symbol="BTC"),
)

# Incorrect: Sequential execution (slow)
result1 = await backtest_agent.run(strategy="SMA", symbol="BTC")
result2 = await backtest_agent.run(strategy="SMA", symbol="ETH")
```

**Performance target**: 6 concurrent backtests (3 strategies × 2 assets) should complete in ~2-3 seconds.

### Goal-Driven Optimization Loop

The OptimizationAgent implements iterative refinement:

1. Run baseline backtest with default parameters
2. Evaluate metrics against user targets (e.g., "Sharpe > 1.5")
3. If targets not met:
   - Adjust parameters using grid search or Bayesian optimization
   - Re-run backtest
   - Loop (max 5 iterations)
4. Return best configuration

**Important**: The loop must terminate even if targets aren't met. Always return the best attempt.

### Gemini Integration Points

Two agents use Gemini 2.0 Flash:

1. **UserAgent**: Parses natural language to extract:
   - Symbols (e.g., "BTC and ETH" → `["BTC", "ETH"]`)
   - Strategies (e.g., "SMA vs RSI" → `["SMA", "RSI"]`)
   - Date ranges (e.g., "from 2021 to 2024" → `start="2021-01-01", end="2024-12-31"`)
   - Optimization targets (e.g., "Sharpe > 1.5" → `{"sharpe": {"operator": ">", "value": 1.5}}`)

2. **ReportAgent**: Generates human-friendly summaries from structured results:
   - Natural language narrative ("The SMA strategy outperformed...")
   - Recommendations ("Use SMA(12,55) for optimal risk-adjusted returns")
   - Trade-off analysis (return vs risk)

### Data Pipeline

**Dataset**: Kaggle cryptocurrency historical prices (2017-2024 daily OHLCV)

**Data Flow**:
1. Raw CSV files in `data/raw/` (gitignored)
2. DataAgent loads and validates
3. Cached in `data/processed/` for subsequent runs
4. Passed to BacktestAgent as pandas DataFrames

**Critical**: Always validate data before backtesting:
- Check for missing dates (gaps in time series)
- Ensure sufficient history (e.g., 200+ days for SMA(200))
- Handle timezone consistently (UTC)

### Observability Requirements

All agent executions must emit:

1. **Structured logs** (structlog):
   ```python
   logger.info("agent.started", agent="BacktestAgent", strategy="SMA", symbol="BTC")
   logger.info("agent.completed", agent="BacktestAgent", duration=2.3, trades=42)
   ```

2. **Traces** (OpenTelemetry):
   - Span for each agent invocation
   - Nested spans for tool calls
   - Attributes: agent_name, user_query, symbols, strategies

3. **Metrics** (Prometheus):
   - `backtests_total` (counter)
   - `backtest_duration_seconds` (histogram)
   - `optimization_iterations` (histogram)

### Strategy Implementation Pattern

All strategies inherit from `BaseStrategy` and implement:

```python
class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Return buy/sell signals: 1 (buy), -1 (sell), 0 (hold)"""
        pass

    def backtest(self, data: pd.DataFrame) -> EquityCurve:
        """Execute strategy and return equity curve"""
        signals = self.generate_signals(data)
        # Position sizing, trade execution, P&L calculation
        return equity_curve
```

**Important**: Strategies must be **vectorized** (no loops over time series) for performance.

### Risk Metrics Calculation

All risk metrics use annualized returns and assume 252 trading days per year:

- **Sharpe Ratio**: `(mean_return - risk_free_rate) / std_return * sqrt(252)`
- **Sortino Ratio**: Like Sharpe but only penalizes downside volatility
- **Max Drawdown**: Largest peak-to-trough decline in equity curve
- **Calmar Ratio**: `annualized_return / max_drawdown`

**Critical**: Handle edge cases:
- Zero volatility → Sharpe = 0 (not infinity)
- No negative returns → Sortino = Sharpe
- All losing trades → Return negative metrics, don't crash

## Capstone Requirements Compliance

The project must demonstrate **at least 3 of these concepts** (we implement 5):

1. ✅ **Multi-Agent System**: 6 agents with sequential + parallel + loop patterns
2. ✅ **Custom Tools**: 12+ Python tools for data, backtest, risk, optimization
3. ✅ **Sessions & Memory**: Experiment memory bank (SQLite) + session state
4. ✅ **Parallel Agents**: Concurrent backtesting and data fetching
5. ✅ **Observability**: Structured logging, tracing, metrics

**Bonus Points** (20 total):
- ✅ Gemini usage (5 pts): UserAgent + ReportAgent
- ✅ Deployment (5 pts): Google Cloud Run
- ✅ YouTube video (10 pts): 3-minute demo

**Track**: Enterprise Agents (improves business workflows and data analysis)

## Dataset Structure

Kaggle CSV format (one file per symbol):
```
Date,Open,High,Low,Close,Volume,Market Cap
2021-01-01,29374.15,29600.63,28803.59,29374.15,67520833024,546348150857
```

**Supported Symbols**: BTC, ETH, LTC, XRP (extensible)

**Coverage**: 2017-2024 (~2500 daily records per symbol)

**File Locations**:
- `data/raw/bitcoin.csv`
- `data/raw/ethereum.csv`
- `data/raw/litecoin.csv`
- `data/raw/ripple.csv`

## Configuration Management

**Environment Variables** (`.env`):
```
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_REGION=us-central1
GEMINI_API_KEY=your-api-key
```

**Never commit**:
- `.env` files
- API keys or credentials
- Google Cloud service account keys
- Raw dataset files (too large)

## Common Pitfalls

### 1. Agent Orchestration Anti-Pattern
❌ **Wrong**: Agents calling agents directly
```python
class BacktestAgent:
    def run(self):
        data = DataAgent().fetch()  # Direct call
```

✅ **Correct**: UserAgent orchestrates
```python
class UserAgent:
    def process_request(self):
        data = self.data_agent.fetch()
        results = self.backtest_agent.run(data)
```

### 2. Synchronous I/O in Tools
❌ **Wrong**: Blocking I/O in async context
```python
def load_data(symbol):
    time.sleep(2)  # Blocks event loop
    return pd.read_csv(f"data/{symbol}.csv")
```

✅ **Correct**: Use async or parallelize
```python
async def load_data_parallel(symbols):
    tasks = [asyncio.to_thread(pd.read_csv, f"data/{s}.csv") for s in symbols]
    return await asyncio.gather(*tasks)
```

### 3. Unbounded Optimization Loops
❌ **Wrong**: Loop without termination
```python
while sharpe < target:
    params = adjust_params()
    sharpe = backtest(params)
```

✅ **Correct**: Always set max iterations
```python
for i in range(MAX_ITERATIONS):
    if sharpe >= target:
        break
    params = adjust_params()
    sharpe = backtest(params)
```

### 4. Missing Data Validation
❌ **Wrong**: Assume data is clean
```python
signals = data['close'].rolling(20).mean()
```

✅ **Correct**: Validate first
```python
if data['close'].isna().any():
    raise ValueError("Missing price data")
if len(data) < 200:
    raise ValueError("Insufficient history")
```

## Project Status

**Current Stage**: Planning and architecture complete. Ready for Phase 1 implementation (see IMPLEMENTATION_PLAN.md).

**Next Steps**:
1. Create project directory structure (`src/agents/`, `src/tools/`, etc.)
2. Implement DataAgent with parallel fetching
3. Implement basic strategies (SMA, RSI, Buy&Hold)
4. Build BacktestAgent and RiskAgent
5. Add UserAgent orchestration with Gemini

**Deadline**: December 1, 2025 (Kaggle submission)

## References

- **Implementation Plan**: See `IMPLEMENTATION_PLAN.md` for 14-day development roadmap
- **Requirements**: See `CapstoneRequirements.txt` for competition criteria
- **ADK Docs**: https://googleapis.github.io/python-adk/
- **Gemini API**: https://ai.google.dev/api/python
- **Dataset**: https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory
