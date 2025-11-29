# BackTestPilot API Reference

Complete reference for BackTestPilot's REST API, Python API, and internal tools.

## Table of Contents

1. [REST API](#rest-api)
2. [Python API](#python-api)
3. [Agent API](#agent-api)
4. [Tool API](#tool-api)
5. [Data Models](#data-models)

---

## REST API

Base URL: `https://your-service.run.app` (or `http://localhost:8000` for local development)

### Authentication

Currently, the API is unauthenticated. For production deployments, consider adding:
- API keys
- OAuth 2.0
- JWT tokens

### Endpoints

#### GET /

**Description**: API information and available endpoints

**Response**:
```json
{
  "name": "BackTestPilot API",
  "version": "1.0.0",
  "description": "AI-Powered Trading Strategy Backtesting & Optimization",
  "endpoints": {
    "health": "/health",
    "backtest": "POST /backtest",
    "experiments": "GET /experiments/{id}",
    "best_experiment": "GET /experiments/best"
  },
  "documentation": "/docs"
}
```

---

#### GET /health

**Description**: Health check endpoint for monitoring

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-17T10:30:00",
  "environment": "production"
}
```

**Status Codes**:
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is unhealthy

---

#### POST /backtest

**Description**: Submit a backtest request

**Request Body**:
```json
{
  "query": "Compare SMA vs RSI on BTC from 2021 to 2024",
  "user_id": "user123",  // Optional
  "async_mode": false    // Optional
}
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Natural language backtest request (10-1000 chars) |
| `user_id` | string | No | User identifier for session tracking |
| `async_mode` | boolean | No | If true, process asynchronously (returns job ID) |

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Backtest completed successfully",
  "experiment_id": 42,
  "results": {
    "strategies": [
      {
        "name": "SMA(20,50)",
        "symbol": "BTC",
        "metrics": {
          "sharpe_ratio": 1.32,
          "total_return": 0.583,
          "max_drawdown": 0.182,
          "win_rate": 0.47,
          "total_trades": 42
        }
      },
      {
        "name": "RSI(14,30-70)",
        "symbol": "BTC",
        "metrics": {
          "sharpe_ratio": 1.08,
          "total_return": 0.425,
          "max_drawdown": 0.153,
          "win_rate": 0.52,
          "total_trades": 58
        }
      }
    ],
    "best_strategy": {
      "name": "SMA(20,50)",
      "symbol": "BTC",
      "sharpe_ratio": 1.32
    }
  },
  "execution_time": 2.35,
  "timestamp": "2025-11-17T10:30:00"
}
```

**Error Response** (400 Bad Request):
```json
{
  "success": false,
  "detail": "Invalid query: Query must be between 10 and 1000 characters"
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "success": false,
  "detail": "Internal server error: [error details]"
}
```

**Example**:
```bash
curl -X POST https://your-service.run.app/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Compare SMA vs RSI on BTC from 2021 to 2024",
    "user_id": "trader-001"
  }'
```

---

#### GET /experiments/{experiment_id}

**Description**: Retrieve a specific experiment by ID

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `experiment_id` | integer | Experiment ID from backtest response |

**Response** (200 OK):
```json
{
  "experiment_id": 42,
  "timestamp": "2025-11-17T10:30:00",
  "user_query": "Compare SMA vs RSI on BTC from 2021 to 2024",
  "symbols": ["BTC"],
  "strategies": ["SMA", "RSI"],
  "results": {
    "strategies": [...],
    "best_strategy": {...}
  },
  "execution_time": 2.35
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Experiment 42 not found"
}
```

**Example**:
```bash
curl https://your-service.run.app/experiments/42
```

---

#### GET /experiments/best

**Description**: Get the best experiment based on a specific metric

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `metric` | string | `sharpe_ratio` | Metric to optimize for |
| `symbol` | string | None | Filter by symbol (optional) |
| `strategy` | string | None | Filter by strategy (optional) |
| `days` | integer | 30 | Look back period in days |

**Supported Metrics**:
- `sharpe_ratio`
- `sortino_ratio`
- `total_return`
- `calmar_ratio`
- `win_rate`
- `profit_factor`

**Response** (200 OK):
```json
{
  "experiment_id": 38,
  "timestamp": "2025-11-10T15:22:00",
  "user_query": "Optimize SMA on BTC",
  "symbols": ["BTC"],
  "strategies": ["SMA"],
  "results": {
    "strategy": "SMA(12,55)",
    "metrics": {
      "sharpe_ratio": 1.68,
      "total_return": 0.78
    }
  },
  "metric_value": 1.68
}
```

**Example**:
```bash
# Best Sharpe ratio for BTC in last 7 days
curl "https://your-service.run.app/experiments/best?metric=sharpe_ratio&symbol=BTC&days=7"
```

---

#### GET /experiments

**Description**: List recent experiments with optional filtering

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 10 | Maximum number of results (max: 100) |
| `offset` | integer | 0 | Number of results to skip |
| `symbol` | string | None | Filter by symbol (optional) |
| `strategy` | string | None | Filter by strategy (optional) |

**Response** (200 OK):
```json
{
  "count": 15,
  "limit": 10,
  "offset": 0,
  "experiments": [
    {
      "experiment_id": 42,
      "timestamp": "2025-11-17T10:30:00",
      "user_query": "Compare SMA vs RSI on BTC",
      "best_sharpe": 1.32
    },
    ...
  ]
}
```

**Example**:
```bash
# Get 20 most recent BTC experiments
curl "https://your-service.run.app/experiments?limit=20&symbol=BTC"
```

---

#### GET /metrics

**Description**: Prometheus metrics endpoint

**Response**: Prometheus exposition format
```
# HELP api_requests_total Total API requests
# TYPE api_requests_total counter
api_requests_total{endpoint="/backtest",method="POST",status="200"} 142.0

# HELP backtest_duration_seconds Backtest execution time
# TYPE backtest_duration_seconds histogram
backtest_duration_seconds_bucket{le="1.0"} 23.0
backtest_duration_seconds_bucket{le="5.0"} 98.0
...
```

---

## Python API

### UserAgent

**Module**: `src.agents.user_agent`

**Class**: `UserAgent`

**Description**: Main orchestrator for processing backtest requests

**Methods**:

#### `process_request(query: str, user_id: Optional[str] = None) -> Dict[str, Any]`

Process a natural language backtest request.

**Parameters**:
- `query` (str): Natural language request
- `user_id` (str, optional): User identifier for session tracking

**Returns**: Dictionary containing:
- `success` (bool): Whether request succeeded
- `results` (dict): Backtest results
- `symbols` (list): Extracted symbols
- `strategies` (list): Tested strategies
- `execution_time` (float): Time in seconds
- `error` (str, optional): Error message if failed

**Example**:
```python
from src.agents.user_agent import UserAgent

agent = UserAgent()
result = await agent.process_request(
    query="Backtest SMA on BTC from 2021 to 2024",
    user_id="trader-001"
)

print(f"Sharpe: {result['results']['best_strategy']['sharpe_ratio']}")
```

---

### DataAgent

**Module**: `src.agents.data_agent`

**Class**: `DataAgent`

**Methods**:

#### `fetch_data(symbols: List[str], start_date: str, end_date: str) -> Dict[str, pd.DataFrame]`

Fetch OHLCV data for multiple symbols in parallel.

**Parameters**:
- `symbols` (List[str]): List of symbol codes (e.g., ["BTC", "ETH"])
- `start_date` (str): Start date in YYYY-MM-DD format
- `end_date` (str): End date in YYYY-MM-DD format

**Returns**: Dictionary mapping symbols to DataFrames

**Example**:
```python
from src.agents.data_agent import DataAgent

agent = DataAgent()
data = await agent.fetch_data(
    symbols=["BTC", "ETH"],
    start_date="2021-01-01",
    end_date="2024-12-31"
)

print(f"BTC data shape: {data['BTC'].shape}")
```

---

### BacktestAgent

**Module**: `src.agents.backtest_agent`

**Class**: `BacktestAgent`

**Methods**:

#### `run_backtest(strategy: str, symbol: str, data: pd.DataFrame, params: Dict) -> Dict`

Execute a single backtest.

**Parameters**:
- `strategy` (str): Strategy name ("SMA", "RSI", "BuyHold", etc.)
- `symbol` (str): Symbol code
- `data` (pd.DataFrame): OHLCV data
- `params` (Dict): Strategy parameters

**Returns**: Dictionary with equity curve and trades

**Example**:
```python
from src.agents.backtest_agent import BacktestAgent

agent = BacktestAgent()
result = await agent.run_backtest(
    strategy="SMA",
    symbol="BTC",
    data=btc_data,
    params={"short_period": 20, "long_period": 50}
)
```

#### `run_parallel_backtests(tasks: List[Dict]) -> List[Dict]`

Execute multiple backtests concurrently.

**Parameters**:
- `tasks` (List[Dict]): List of backtest specifications

**Returns**: List of results

---

### RiskAgent

**Module**: `src.agents.risk_agent`

**Class**: `RiskAgent`

**Methods**:

#### `compute_metrics(equity_curve: pd.Series) -> Dict[str, float]`

Compute all risk metrics for an equity curve.

**Parameters**:
- `equity_curve` (pd.Series): Cumulative returns over time

**Returns**: Dictionary with metrics:
- `sharpe_ratio`
- `sortino_ratio`
- `calmar_ratio`
- `max_drawdown`
- `volatility`
- `total_return`
- `win_rate`
- `profit_factor`

**Example**:
```python
from src.agents.risk_agent import RiskAgent

agent = RiskAgent()
metrics = agent.compute_metrics(equity_curve)

print(f"Sharpe: {metrics['sharpe_ratio']:.2f}")
print(f"Max DD: {metrics['max_drawdown']:.2%}")
```

---

### OptimizationAgent

**Module**: `src.agents.optimization_agent`

**Class**: `OptimizationAgent`

**Methods**:

#### `optimize(strategy: str, symbol: str, data: pd.DataFrame, targets: Dict, max_iterations: int = 5) -> Dict`

Optimize strategy parameters to meet targets.

**Parameters**:
- `strategy` (str): Strategy name
- `symbol` (str): Symbol code
- `data` (pd.DataFrame): OHLCV data
- `targets` (Dict): Target metrics (e.g., {"sharpe_ratio": {">": 1.5}})
- `max_iterations` (int): Maximum optimization iterations

**Returns**: Dictionary with best parameters and results

**Example**:
```python
from src.agents.optimization_agent import OptimizationAgent

agent = OptimizationAgent()
result = await agent.optimize(
    strategy="SMA",
    symbol="BTC",
    data=btc_data,
    targets={"sharpe_ratio": {">": 1.5}, "max_drawdown": {"<": 0.15}},
    max_iterations=5
)

print(f"Best params: {result['best_params']}")
```

---

## Tool API

### Data Tools

**Module**: `src.tools.data_tools`

#### `get_supported_symbols() -> List[str]`

Get list of supported symbols.

**Returns**: List of symbol codes

**Example**:
```python
from src.tools.data_tools import get_supported_symbols

symbols = get_supported_symbols()
# ['BTC', 'ETH', 'LTC', 'XRP']
```

#### `load_ohlcv(symbol: str, start_date: str, end_date: str) -> pd.DataFrame`

Load OHLCV data for a single symbol.

**Parameters**:
- `symbol` (str): Symbol code
- `start_date` (str): Start date (YYYY-MM-DD)
- `end_date` (str): End date (YYYY-MM-DD)

**Returns**: DataFrame with columns: Date, Open, High, Low, Close, Volume

**Example**:
```python
from src.tools.data_tools import load_ohlcv

data = load_ohlcv("BTC", "2021-01-01", "2024-12-31")
print(data.head())
```

---

### Risk Tools

**Module**: `src.tools.risk_tools`

#### `compute_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float`

Calculate annualized Sharpe ratio.

**Parameters**:
- `returns` (pd.Series): Daily returns
- `risk_free_rate` (float): Annual risk-free rate (default: 0.0)

**Returns**: Sharpe ratio

**Example**:
```python
from src.tools.risk_tools import compute_sharpe_ratio

sharpe = compute_sharpe_ratio(daily_returns, risk_free_rate=0.02)
```

#### `compute_max_drawdown(equity: pd.Series) -> float`

Calculate maximum drawdown.

**Parameters**:
- `equity` (pd.Series): Cumulative equity curve

**Returns**: Maximum drawdown (negative value)

**Example**:
```python
from src.tools.risk_tools import compute_max_drawdown

max_dd = compute_max_drawdown(equity_curve)
print(f"Max Drawdown: {max_dd:.2%}")
```

---

### Visualization Tools

**Module**: `src.tools.visualization_tools`

#### `plot_equity_curve(equity: pd.Series, trades: pd.DataFrame) -> Figure`

Plot equity curve with trade markers.

**Parameters**:
- `equity` (pd.Series): Cumulative returns
- `trades` (pd.DataFrame): Trade log with columns: Date, Type (buy/sell), Price

**Returns**: Matplotlib Figure

**Example**:
```python
from src.tools.visualization_tools import plot_equity_curve

fig = plot_equity_curve(equity_curve, trades)
fig.savefig('equity_curve.png')
```

---

## Data Models

### BacktestRequest

```python
class BacktestRequest(BaseModel):
    query: str = Field(..., min_length=10, max_length=1000)
    user_id: Optional[str] = None
    async_mode: bool = False
```

### BacktestResponse

```python
class BacktestResponse(BaseModel):
    success: bool
    message: str
    experiment_id: Optional[int] = None
    results: Optional[Dict[str, Any]] = None
    execution_time: Optional[float] = None
    timestamp: str
```

### Strategy

```python
class Strategy:
    name: str
    parameters: Dict[str, Any]
    symbol: str
    equity_curve: pd.Series
    trades: pd.DataFrame
    metrics: Dict[str, float]
```

### Experiment

```python
class Experiment:
    id: int
    timestamp: datetime
    user_query: str
    symbols: List[str]
    strategies: List[str]
    parameters: Dict[str, Any]
    results: Dict[str, Any]
    execution_time: float
```

---

## Rate Limits

Current rate limits (can be adjusted in deployment):

- **Backtest requests**: 100 per hour per IP
- **Experiment queries**: 1000 per hour per IP
- **Health checks**: Unlimited

For higher limits, contact support or deploy your own instance.

---

## Versioning

API version: `1.0.0`

The API follows semantic versioning:
- **Major version**: Breaking changes
- **Minor version**: New features (backward compatible)
- **Patch version**: Bug fixes

Version is included in all responses and can be queried via `GET /`.

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 404 | Not Found (experiment not found) |
| 429 | Too Many Requests (rate limit exceeded) |
| 500 | Internal Server Error |
| 503 | Service Unavailable (health check failed) |

---

*Last Updated: November 17, 2025*
