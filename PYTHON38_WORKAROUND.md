# Python 3.8 Workaround Guide

## Issue

Your system is running **Python 3.8.10**, but Google ADK requires **Python 3.10+**.

```bash
$ python3 --version
Python 3.8.10
```

## Solutions

You have 3 options:

### Option 1: Use FastAPI REST API (Recommended for Python 3.8)

Instead of using `adk web`, run the FastAPI server:

```bash
# Start the FastAPI server
uvicorn deployment.api_adk:app --reload --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000/docs for the interactive API documentation.

**Available endpoints:**
- `GET /` - Service information
- `GET /health` - Health check
- `GET /tools` - List available tools
- `POST /backtest` - Submit backtest query
- `GET /agent-info` - Agent configuration details

**Example API usage:**
```bash
# Get service info
curl http://localhost:8000/

# List available tools
curl http://localhost:8000/tools

# Submit a backtest query
curl -X POST http://localhost:8000/backtest \
  -H "Content-Type: application/json" \
  -d '{"query": "What cryptocurrencies are available?"}'
```

### Option 2: Upgrade to Python 3.10+ (Recommended for full ADK support)

Install Python 3.10 or higher:

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev

# Create new virtual environment with Python 3.10
python3.10 -m venv venv310
source venv310/bin/activate
pip install -r requirements.txt
```

**On WSL2 (Windows Subsystem for Linux):**
```bash
# Install deadsnakes PPA for newer Python versions
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then uncomment the `google-adk` line in `requirements.txt` and install it.

### Option 3: Use Direct Python Imports (For Testing)

You can interact with the backtesting tools directly in Python without the ADK framework:

```python
# test_agent.py
from src.tools.data_tools_adk import (
    get_available_symbols,
    fetch_ohlcv_data,
    get_recommended_date_ranges
)
from src.tools.backtest_tools_adk import (
    execute_sma_backtest,
    execute_rsi_backtest,
    compare_strategies
)

# Get available symbols
symbols_result = get_available_symbols()
print(f"Available: {symbols_result['symbols']}")

# Get recommended date ranges
ranges = get_recommended_date_ranges('BTC')
print(f"BTC data: {ranges['data_start']} to {ranges['data_end']}")

# Fetch data
data_result = fetch_ohlcv_data('BTC', '2024-01-01', '2024-12-31')
if data_result['success']:
    print(f"Loaded {len(data_result['data'])} days of BTC data")

    # Run backtest
    backtest_result = execute_sma_backtest(
        data_result['data'],
        symbol='BTC',
        short_window=20,
        long_window=50
    )

    print(f"\nBacktest Results:")
    print(f"Total Return: {backtest_result['total_return']:.2f}%")
    print(f"Sharpe Ratio: {backtest_result['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {backtest_result['max_drawdown']:.2f}%")
```

Run it:
```bash
python3 test_agent.py
```

## Recommendation

For your current Python 3.8 environment, **use Option 1 (FastAPI)** which is already set up and ready to use.

For full ADK CLI support with `adk web`, upgrade to Python 3.10+ using **Option 2**.

---

**Sources:**
- [Python - Agent Development Kit - Google](https://google.github.io/adk-docs/get-started/python/)
- [google-adk PyPI](https://pypi.org/project/google-adk/)
- [ADK GitHub Repository](https://github.com/google/adk-python)
