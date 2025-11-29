# BackTestPilot Architecture Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Multi-Agent Architecture](#multi-agent-architecture)
3. [Agent Responsibilities](#agent-responsibilities)
4. [Tool Layer](#tool-layer)
5. [Memory Architecture](#memory-architecture)
6. [Data Flow](#data-flow)
7. [Observability](#observability)
8. [Deployment Architecture](#deployment-architecture)
9. [Design Patterns](#design-patterns)
10. [Performance Considerations](#performance-considerations)

---

## System Overview

BackTestPilot is a **multi-agent AI system** that transforms natural-language trading requests into fully backtested, risk-analyzed strategies with automated parameter optimization.

### Key Architecture Principles

1. **Agent Autonomy**: Each agent is independent and communicates through well-defined tool interfaces
2. **Hierarchical Orchestration**: UserAgent coordinates all sub-agents; agents never directly call each other
3. **Parallel Execution**: Independent tasks run concurrently for maximum performance
4. **Loop-Based Optimization**: Iterative refinement until targets met or max iterations reached
5. **Observable by Design**: Structured logging, tracing, and metrics built into every component

---

## Multi-Agent Architecture

### Agent Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                        UserAgent                             │
│                    (Orchestrator - Gemini)                   │
│  • Parse natural language requests                           │
│  • Plan execution sequence                                   │
│  • Coordinate sub-agents                                     │
│  • Manage session state                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ↓                              ↓
┌──────────────────┐          ┌──────────────────┐
│  ValidationAgent │          │    DataAgent     │
│                  │          │   (Parallel)     │
│  • Validate dates│          │  • Fetch BTC     │
│  • Check params  │          │  • Fetch ETH     │
│  • Symbol check  │          │  • Cache data    │
└────────┬─────────┘          └────────┬─────────┘
         └──────────┬─────────────────┘
                    ↓
        ┌───────────────────────────┐
        │   BacktestAgent           │
        │   (Parallel Execution)    │
        │                           │
        │   ┌─────────────────┐    │
        │   │ SMA Strategy    │────┼──→ BTC, ETH (parallel)
        │   │ RSI Strategy    │────┼──→ BTC, ETH (parallel)
        │   │ BuyHold         │────┼──→ BTC, ETH (parallel)
        │   └─────────────────┘    │
        └───────────┬───────────────┘
                    ↓
        ┌───────────────────────────┐
        │      RiskAgent            │
        │   (Parallel Analysis)     │
        │   • Sharpe Ratio          │
        │   • Max Drawdown          │
        │   • Sortino, Calmar       │
        └───────────┬───────────────┘
                    ↓
        ┌───────────────────────────┐
        │  OptimizationAgent        │
        │  (Loop Agent)             │
        │                           │
        │  LOOP (max 5 iterations): │
        │    IF targets not met:    │
        │      ├─ Adjust parameters │
        │      ├─ Re-run backtest   │
        │      └─ Evaluate metrics  │
        └───────────┬───────────────┘
                    ↓
        ┌───────────────────────────┐
        │    ReportAgent            │
        │    (Gemini 2.0 Flash)     │
        │   • Generate narrative    │
        │   • Create visualizations │
        │   • Rank strategies       │
        │   • Recommendations       │
        └───────────────────────────┘
```

### Execution Modes

**1. Sequential Flow**
```
UserAgent → ValidationAgent → DataAgent → BacktestAgent → RiskAgent → ReportAgent
```
Used for: Simple backtests, single strategy executions

**2. Parallel Flow**
```
DataAgent:     [Fetch BTC] [Fetch ETH] [Fetch LTC] [Fetch XRP]
               └─────────────┬─────────────┘
BacktestAgent: [SMA×BTC] [SMA×ETH] [RSI×BTC] [RSI×ETH] [BH×BTC] [BH×ETH]
               └─────────────────┬─────────────────┘
RiskAgent:     [Metrics for each backtest in parallel]
```
Used for: Multi-asset, multi-strategy comparisons (performance critical)

**3. Loop Flow**
```
OptimizationAgent:
  Iteration 1: Run backtest → Evaluate → Adjust params
  Iteration 2: Run backtest → Evaluate → Adjust params
  ...
  Iteration N: Targets met ✓ OR Max iterations reached
```
Used for: Parameter optimization, target-driven refinement

---

## Agent Responsibilities

### UserAgent (Orchestrator)

**Model**: Gemini 2.0 Flash
**Purpose**: Parse user intent and orchestrate workflow

**Core Capabilities**:
- Natural language understanding (extract symbols, strategies, date ranges, targets)
- Execution planning (determine which agents to invoke and in what order)
- Session management (track conversation context across multiple turns)
- Result summarization (coordinate ReportAgent for final output)

**Example Processing**:
```python
Input: "Compare SMA vs RSI on BTC and ETH from 2021-2024, target Sharpe > 1.5"

UserAgent parses to:
{
    "symbols": ["BTC", "ETH"],
    "strategies": ["SMA", "RSI", "BuyHold"],  # Adds baseline
    "date_range": {"start": "2021-01-01", "end": "2024-12-31"},
    "targets": {"sharpe_ratio": {"operator": ">", "value": 1.5}},
    "optimization_required": True
}
```

**Tools Used**:
- `parse_request()` - Extract structured data from natural language
- `plan_execution()` - Determine agent invocation sequence
- `delegate_to_agent()` - Invoke sub-agents
- `summarize_results()` - Coordinate final report

---

### DataAgent (Parallel Data Fetching)

**Purpose**: Load OHLCV data for multiple symbols concurrently

**Parallelization**:
```python
# Sequential (slow): ~4 seconds
data_btc = load_ohlcv("BTC")
data_eth = load_ohlcv("ETH")
data_ltc = load_ohlcv("LTC")
data_xrp = load_ohlcv("XRP")

# Parallel (fast): ~1 second
data = await asyncio.gather(
    load_ohlcv("BTC"),
    load_ohlcv("ETH"),
    load_ohlcv("LTC"),
    load_ohlcv("XRP")
)
# 4x speedup!
```

**Caching Strategy**:
- Raw CSVs cached in `data/raw/` (gitignored)
- Processed DataFrames cached in `data/processed/`
- Cache invalidation based on date range and symbol

**Tools Used**:
- `get_supported_symbols()` - List available symbols
- `load_ohlcv_parallel()` - Parallel data fetching
- `validate_data()` - Check for missing dates, outliers
- `cache_data()` - Persist processed data

---

### ValidationAgent

**Purpose**: Input validation before expensive operations

**Validation Checks**:
1. **Date ranges**: Start < End, sufficient history for indicators
2. **Symbols**: Exist in dataset, not duplicates
3. **Parameters**: Within valid ranges (e.g., SMA short < long)
4. **Strategies**: Recognized strategy names

**Early Failure**:
```
❌ Invalid Request → Fail Fast (saves computation)
✅ Valid Request → Proceed to DataAgent
```

**Tools Used**:
- `validate_date_range()` - Check date validity
- `validate_symbols()` - Verify symbol existence
- `validate_parameters()` - Check parameter constraints

---

### BacktestAgent (Parallel Strategy Execution)

**Purpose**: Execute backtests concurrently across strategies and assets

**Parallelization Example**:
```
Strategies: [SMA, RSI, BuyHold]
Symbols: [BTC, ETH]

Sequential: 3 × 2 = 6 backtests @ 2s each = 12 seconds
Parallel:   6 backtests @ 2s = 2 seconds
Speedup: 6x
```

**Strategy Execution**:
1. Load strategy class (SMA, RSI, etc.)
2. Generate trading signals
3. Simulate trades with position sizing
4. Calculate equity curve
5. Return results

**Tools Used**:
- `run_backtest_parallel()` - Concurrent execution
- `run_single_backtest()` - Individual strategy execution
- `compare_strategies()` - Rank strategies

---

### RiskAgent

**Purpose**: Compute comprehensive risk metrics for equity curves

**Metrics Calculated** (all parallelizable):
- **Sharpe Ratio**: Risk-adjusted returns
- **Sortino Ratio**: Downside risk only
- **Calmar Ratio**: Return / Max Drawdown
- **Max Drawdown**: Largest peak-to-trough decline
- **Volatility**: Annualized standard deviation
- **Win Rate**: % of profitable trades
- **Profit Factor**: Gross profit / Gross loss

**Formula Reference**:
```python
# Sharpe Ratio (annualized, 252 trading days)
sharpe = (mean_return - risk_free_rate) / std_return * sqrt(252)

# Max Drawdown
equity_curve_cummax = equity.cummax()
drawdown = (equity - equity_curve_cummax) / equity_curve_cummax
max_drawdown = drawdown.min()
```

**Tools Used**:
- `compute_sharpe_ratio()`
- `compute_max_drawdown()`
- `compute_all_metrics()` - Batch computation

---

### OptimizationAgent (Loop Agent)

**Purpose**: Iteratively refine parameters to meet user targets

**Algorithm**:
```python
def optimize(strategy, targets, max_iterations=5):
    best_result = None
    best_params = None

    for iteration in range(max_iterations):
        # Run backtest with current params
        result = backtest(strategy, params)

        # Evaluate against targets
        if meets_targets(result, targets):
            return result  # Success!

        # Adjust parameters
        params = adjust_params(params, result, targets)

        # Track best attempt
        if better_than(result, best_result):
            best_result = result
            best_params = params

    # Return best attempt even if targets not met
    return best_result
```

**Parameter Adjustment Strategies**:
1. **Grid Search**: Exhaustive search over parameter space
2. **Bayesian Optimization**: Sample efficient optimization
3. **Gradient-Based**: Hill climbing for continuous parameters

**Tools Used**:
- `grid_search_parameters()` - Systematic search
- `optimize_toward_target()` - Target-driven refinement
- `evaluate_parameters()` - Fitness function

---

### ReportAgent (Natural Language Generation)

**Model**: Gemini 2.0 Flash
**Purpose**: Generate human-friendly reports from structured results

**Report Components**:
1. **Executive Summary**: 2-3 sentence overview
2. **Strategy Rankings**: Table sorted by Sharpe or other metric
3. **Performance Analysis**: Return vs risk trade-offs
4. **Visualizations**: Equity curves, drawdowns, parameter heatmaps
5. **Recommendations**: Actionable next steps

**Example Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 Best Strategy: SMA(12,55) on ETH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The SMA crossover strategy outperformed RSI and Buy-and-Hold
across both BTC and ETH. ETH showed stronger risk-adjusted
returns (Sharpe 1.68) with lower drawdowns.

Recommendation: Deploy SMA(12,55) on ETH for live trading.
Consider adding stop-loss at 5% to limit downside.
```

**Tools Used**:
- `generate_report()` - Text generation with Gemini
- `create_visualizations()` - Charts and graphs
- `rank_strategies()` - Sort by user-specified metric

---

## Tool Layer

### Design Principles

**Tools are Pure Functions**:
- Accept explicit parameters (no hidden state)
- Return structured dictionaries (JSON-serializable)
- Handle errors gracefully with descriptive messages
- Independently testable

**Tool Categories**:

**1. Data Tools** (`src/tools/data_tools.py`):
```python
get_supported_symbols() -> list
load_ohlcv(symbols, start, end) -> dict
validate_date_range(start, end) -> bool
```

**2. Strategy Tools** (`src/tools/strategy_tools.py`):
```python
run_sma_crossover(symbol, short, long, data) -> EquityCurve
run_rsi_mean_reversion(symbol, period, lower, upper, data) -> EquityCurve
run_buy_and_hold(symbol, data) -> EquityCurve
```

**3. Risk Tools** (`src/tools/risk_tools.py`):
```python
compute_sharpe_ratio(returns, risk_free_rate) -> float
compute_max_drawdown(equity_curve) -> float
compute_all_metrics(equity_curve) -> dict
```

**4. Optimization Tools** (`src/tools/optimization_tools.py`):
```python
grid_search_parameters(strategy, param_grid) -> dict
optimize_toward_target(strategy, target_metric, target_value) -> dict
```

**5. Visualization Tools** (`src/tools/visualization_tools.py`):
```python
plot_equity_curve(equity, trades) -> Figure
plot_drawdown(equity) -> Figure
plot_parameter_heatmap(results) -> Figure
```

**6. Portfolio Tools** (`src/tools/portfolio_tools.py`):
```python
run_portfolio_backtest(strategies, weights) -> EquityCurve
optimize_portfolio_weights(strategies, objective) -> dict
```

---

## Memory Architecture

### Experiment Memory Bank (SQLite)

**Purpose**: Persist all backtest runs for historical analysis

**Schema**:
```sql
CREATE TABLE experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_query TEXT NOT NULL,
    symbols JSON NOT NULL,
    strategies JSON NOT NULL,
    parameters JSON,
    results JSON NOT NULL,
    execution_time REAL,
    agent_trace JSON,
    INDEX idx_timestamp (timestamp),
    INDEX idx_symbols (symbols),
    INDEX idx_strategies (strategies)
);
```

**Query Examples**:
```python
# Get best BTC strategy from last 7 days
best = experiment_store.get_best_experiment(
    metric="sharpe_ratio",
    symbol="BTC",
    days=7
)

# Search experiments by strategy
sma_experiments = experiment_store.search_experiments(
    filters={"strategy": "SMA"}
)
```

**Tools**:
- `save_experiment()` - Persist backtest results
- `get_experiment(id)` - Retrieve by ID
- `search_experiments(filters)` - Query with filters
- `get_best_experiment(metric)` - Find optimal result

### Session Management (In-Memory)

**Purpose**: Track conversation context within a single session

**Implementation**:
```python
from google.adk.session import InMemorySessionService

session = InMemorySessionService()

# Track conversation state
session.set("current_symbols", ["BTC", "ETH"])
session.set("last_results", {...})
session.set("optimization_history", [...])

# Multi-turn conversations
# User: "Backtest SMA on BTC"
# Agent: [saves BTC results]
# User: "Now try it on ETH"
# Agent: [retrieves last strategy, applies to ETH]
```

---

## Data Flow

### End-to-End Request Flow

```
1. User Input
   ↓
2. UserAgent: Parse request with Gemini
   ↓
3. ValidationAgent: Validate inputs
   ↓
4. DataAgent: Load data in parallel
   ↓
5. BacktestAgent: Execute strategies in parallel
   ↓
6. RiskAgent: Compute metrics in parallel
   ↓
7. OptimizationAgent: Refine if needed (loop)
   ↓
8. ReportAgent: Generate report with Gemini
   ↓
9. ExperimentStore: Save results
   ↓
10. Return to User
```

### Data Transformations

```
Raw CSV
  → pd.DataFrame (OHLCV)
    → Strategy Signals (1, -1, 0)
      → Trades (entry/exit points)
        → Equity Curve (cumulative returns)
          → Risk Metrics (Sharpe, DD, etc.)
            → Report (text + visualizations)
```

---

## Observability

### Structured Logging (structlog)

**Log Events**:
```python
logger.info("agent.started", agent="BacktestAgent", strategy="SMA")
logger.info("agent.completed", agent="BacktestAgent", duration=2.3, trades=42)
logger.error("agent.failed", agent="BacktestAgent", error="Invalid params")
```

**Log Levels**:
- **DEBUG**: Detailed execution traces
- **INFO**: Agent lifecycle events
- **WARNING**: Degraded performance, fallbacks
- **ERROR**: Failures with recovery
- **CRITICAL**: Unrecoverable errors

### Distributed Tracing (OpenTelemetry)

**Span Hierarchy**:
```
user_request [10.5s]
├─ parse_request [0.5s]
├─ validate_inputs [0.2s]
├─ load_data [1.2s]
│  ├─ load_btc [0.6s]
│  └─ load_eth [0.6s]
├─ run_backtests [6.0s]
│  ├─ sma_btc [2.0s]
│  ├─ sma_eth [2.0s]
│  └─ rsi_btc [2.0s]
├─ compute_risk [1.5s]
└─ generate_report [1.1s]
```

**Trace Attributes**:
- `agent.name`, `agent.version`
- `user.query`, `user.id`
- `symbols`, `strategies`, `date_range`

### Metrics (Prometheus)

**Key Metrics**:
```python
# Counters
backtests_total.labels(strategy="SMA", symbol="BTC").inc()
api_requests_total.labels(endpoint="/backtest", status="200").inc()

# Histograms
backtest_duration_seconds.observe(2.35)
api_request_duration_seconds.labels(endpoint="/backtest").observe(10.5)

# Gauges
active_backtests.set(6)
```

**Dashboard Queries**:
```promql
# Request rate
rate(api_requests_total[5m])

# P95 latency
histogram_quantile(0.95, backtest_duration_seconds)

# Error rate
rate(api_requests_total{status=~"5.."}[5m])
```

---

## Deployment Architecture

### Cloud Run Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │ HTTPS
       ↓
┌─────────────────────────────────┐
│  Cloud Load Balancer            │
│  • SSL termination              │
│  • DDoS protection              │
└────────────┬────────────────────┘
             │
       ┌─────┴─────┐
       │           │
   ┌───▼───┐   ┌───▼───┐
   │ Pod 1 │   │ Pod 2 │  ... (Auto-scaled)
   └───┬───┘   └───┬───┘
       │           │
       └─────┬─────┘
             │
   ┌─────────▼─────────┐
   │  BackTestPilot    │
   │  FastAPI App      │
   └─────────┬─────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼───┐      ┌──────▼─────┐
│ SQLite│      │ Gemini API │
│ (local│      │ (Vertex AI)│
│  DB)  │      └────────────┘
└───────┘
```

**Auto-Scaling**:
- **Min instances**: 0 (scale to zero for cost savings)
- **Max instances**: 10 (handle traffic spikes)
- **Target CPU**: 80%
- **Concurrency**: 80 requests per instance

**Resource Allocation**:
- **CPU**: 2 vCPU
- **Memory**: 2 GiB
- **Timeout**: 300 seconds (5 minutes)

---

## Design Patterns

### 1. Agent Orchestration Pattern

**Problem**: Agents must coordinate without tight coupling

**Solution**: UserAgent as central orchestrator
```python
class UserAgent:
    def process_request(self, query):
        # Parse intent
        spec = self.parse(query)

        # Delegate to sub-agents
        data = self.data_agent.fetch(spec.symbols)
        results = self.backtest_agent.run(data, spec.strategies)
        metrics = self.risk_agent.analyze(results)

        # Coordinate report
        return self.report_agent.generate(metrics)
```

### 2. Parallel Execution Pattern

**Problem**: Sequential operations are slow

**Solution**: Use asyncio.gather for independent tasks
```python
# Parallel data fetching
data = await asyncio.gather(
    fetch_btc(),
    fetch_eth(),
    fetch_ltc()
)

# Parallel backtesting
results = await asyncio.gather(
    backtest_sma_btc(),
    backtest_sma_eth(),
    backtest_rsi_btc()
)
```

### 3. Loop Agent Pattern

**Problem**: Iterative refinement until targets met

**Solution**: Bounded loop with early termination
```python
for i in range(MAX_ITERATIONS):
    result = run_backtest(params)
    if meets_targets(result):
        return result  # Success!
    params = adjust_params(params, result)
return best_attempt  # Partial success
```

### 4. Tool-Based Architecture

**Problem**: Agents need reusable, testable functions

**Solution**: Pure function tools
```python
# Tool definition
def compute_sharpe(returns: pd.Series, rf_rate: float = 0.0) -> float:
    """Pure function: same inputs → same output"""
    return (returns.mean() - rf_rate) / returns.std() * np.sqrt(252)

# Agent usage
sharpe = self.tools.compute_sharpe(equity_curve.returns())
```

---

## Performance Considerations

### Bottlenecks

**1. Data Loading** (I/O bound)
- **Solution**: Parallel fetching, caching, pre-processing

**2. Backtesting** (CPU bound)
- **Solution**: Vectorized operations, parallel execution

**3. LLM Calls** (API latency)
- **Solution**: Async requests, response caching

### Optimization Strategies

**Vectorization**:
```python
# Slow (loop)
signals = []
for i in range(len(df)):
    if df['sma_short'][i] > df['sma_long'][i]:
        signals.append(1)
    else:
        signals.append(-1)

# Fast (vectorized)
signals = np.where(df['sma_short'] > df['sma_long'], 1, -1)
```

**Caching**:
```python
@lru_cache(maxsize=128)
def compute_indicators(symbol, start, end):
    # Expensive computation cached
    return indicators
```

**Parallel Execution**:
- **6 concurrent backtests**: 2-3 seconds (target met)
- **Sequential equivalent**: 12-18 seconds

---

## Security Considerations

### API Security

- ✅ Input validation on all endpoints
- ✅ Rate limiting (Cloud Armor)
- ✅ CORS restrictions in production
- ✅ No API keys in logs or responses

### Data Security

- ✅ SQLite database not exposed publicly
- ✅ Experiment data encrypted at rest (Cloud Run default)
- ✅ Gemini API credentials in Secret Manager

### Deployment Security

- ✅ Service accounts with minimal permissions
- ✅ VPC connectors for private resources
- ✅ Cloud Audit Logs enabled
- ✅ Vulnerability scanning (Cloud Build)

---

## Conclusion

BackTestPilot demonstrates enterprise-grade agent architecture with:

- **Multi-agent orchestration** (sequential + parallel + loop)
- **Scalable deployment** (Cloud Run with auto-scaling)
- **Comprehensive observability** (logging + tracing + metrics)
- **High performance** (parallel execution, vectorization)
- **Security best practices** (input validation, secret management)

This architecture enables quantitative traders to prototype strategies **10x faster** while maintaining production-grade reliability and observability.

---

*Last Updated: November 17, 2025*
