# BackTest-Agent

AI-powered cryptocurrency strategy backtesting via natural language queries.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Built%20with-Google%20ADK-4285F4.svg)](https://googleapis.github.io/python-adk/)

## Overview

BackTest-Agent automates cryptocurrency trading strategy backtesting through natural language. Built with Google ADK and Gemini 2.0 Flash, it orchestrates 15 specialized tools to handle data fetching, strategy execution, and parameter optimization.

**Built for**: Google AI Agents Intensive Course Capstone Project (Enterprise Agents Track)

## Problem

Testing trading strategies requires repetitive manual work:
- Writing custom code for each strategy variation
- Running multiple backtests to test parameter combinations
- Comparing strategy performance across different cryptocurrencies

## Solution

An ADK agent that processes natural language requests and automatically executes the backtesting workflow.

**Example queries:**
```
"What cryptocurrencies are available?"
"Backtest SMA(20,50) on BTC from 2023 to 2025"
"Compare SMA vs RSI on ETH"
"Optimize RSI parameters for Sharpe ratio above 1.5"
```

**Agent workflow:**
1. Parse user intent (symbols, strategies, dates, targets)
2. Validate inputs against available data
3. Select appropriate tools
4. Execute backtesting pipeline
5. Return results with natural language explanations

## Architecture

```
User Query → Gemini Agent → Tool Selection → Execution → Report
                    ↓
        ┌───────────┼───────────┐
    Data Tools  Backtest    Optimization
      (6)        Tools          (3)
                  (6)
```

## Implementation

**15 ADK-Compatible Tools:**

*Data (6)*: Symbol lists, data availability checks, date range recommendations, OHLCV loading, parallel fetching, parameter validation

*Backtesting (6)*: SMA Crossover, RSI Mean Reversion, Bollinger Bands, MACD, Buy & Hold, strategy comparison

*Optimization (3)*: Grid search for SMA, RSI, and Bollinger Bands parameters

**5 Trading Strategies:**
- SMA Crossover (trend following)
- RSI Mean Reversion (momentum)
- Bollinger Bands (volatility)
- MACD (trend changes)
- Buy & Hold (baseline)

**Risk Metrics:**
Sharpe ratio, Sortino ratio, Calmar ratio, maximum drawdown, volatility, win rate, profit factor, total return

## Technology

- **Framework**: Google ADK 1.19.0
- **LLM**: Gemini 2.0 Flash
- **Language**: Python 3.11
- **Data**: Kaggle Crypto Historical Prices (18 cryptocurrencies, 2010-2025, daily OHLCV)
- **Interface**: `adk web` (interactive chat at localhost:8000)
- **Testing**: pytest (33 tests, 100% pass rate)
- **Deployment**: Google Cloud Run (FastAPI info API)

## Installation

### Prerequisites

- Python 3.11+
- Google Cloud Account (for Gemini API)
- Kaggle Account (for dataset download)

### Setup

```bash
# Clone and install
git clone https://github.com/0xhubed/backtest-agent.git
cd backtest-agent
python -m venv venv311
source venv311/bin/activate  # Windows: venv311\Scripts\activate
pip install -r requirements.txt

# Download dataset
pip install kaggle
kaggle datasets download -d paveljurke/crypto-prices-historical-data
unzip crypto-prices-historical-data.zip -d data/

# Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

**Dataset**: 18 cryptocurrencies (BTC, ETH, LTC, XRP, BNB, ADA, DOGE, DOT, SHIB, TRX, SOL, LEO, UNI, AVAX, TON, LINK, BCH, NEAR) with daily OHLCV data from 2010-2025, updated daily.

## Usage

### Interactive Agent (Primary Interface)

```bash
adk web
```

Opens interactive chat at `http://localhost:8000`

### Example Queries

**Simple backtest:**
```
Backtest SMA(20,50) on BTC from 2023 to 2025
```

**Strategy comparison:**
```
Compare SMA vs RSI on ETH from 2020 to 2024
```

**Parameter optimization:**
```
Optimize RSI parameters for BTC with Sharpe ratio above 1.5
```

**Data availability:**
```
What cryptocurrencies are available?
Show me the date range for ETH
```

More examples in [EXAMPLE_QUERIES.md](EXAMPLE_QUERIES.md)

## Project Structure

```
backtest-agent1/
├── README.md                    # This file
├── PROJECT_DESCRIPTION.md       # Capstone submission description
├── EXAMPLE_QUERIES.md           # Example queries
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── pytest.ini                   # Test configuration
│
├── backtest_agent/              # Main agent package
│   ├── __init__.py
│   └── agent.py                 # ADK agent with 15 tools
│
├── src/
│   ├── strategies/              # 5 trading strategies
│   │   ├── base_strategy.py
│   │   ├── sma_crossover.py
│   │   ├── rsi_mean_reversion.py
│   │   ├── bollinger_bands.py
│   │   ├── macd.py
│   │   └── buy_and_hold.py
│   │
│   ├── tools/                   # 15 ADK tools
│   │   ├── data_tools_adk.py       # Data tools (6)
│   │   ├── backtest_tools_adk.py   # Backtest tools (6)
│   │   └── optimization_tools_adk.py # Optimization tools (3)
│   │
│   └── utils/                   # Utilities
│       ├── config.py
│       ├── validators.py
│       └── profiler.py
│
├── data/
│   └── crypto-markets.csv       # Price data (gitignored)
│
├── tests/                       # 33 unit/integration tests
│   ├── test_adk_agent.py
│   ├── test_agent_evaluation.py
│   ├── test_agent_tools.py
│   ├── test_data_tools.py
│   ├── test_strategies.py
│   ├── test_new_strategies.py
│   └── test_optimization.py
│
└── deployment/                  # Cloud deployment
    ├── Dockerfile.adk
    ├── cloudbuild-adk.yaml
    ├── deploy_cloudrun.sh
    ├── api_adk.py               # Info API (non-interactive)
    └── README.md
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_strategies.py -v

# Run with coverage
pytest --cov=src --cov-report=html
```

**Test Coverage**: 33 tests covering data tools, strategy execution, agent integration, and risk calculations.

## Deployment

### Local Development

```bash
adk web  # Interactive agent at localhost:8000
```

### Cloud Run (Info API Only)

The Cloud Run deployment provides a simple info API demonstrating deployment capability. For full agent functionality, use `adk web` locally.

```bash
# Deploy to Cloud Run
cd deployment
./deploy_cloudrun.sh

# Deployed endpoints
https://backtest-agent-aj3kkr4xeq-uc.a.run.app/          # Service info
https://backtest-agent-aj3kkr4xeq-uc.a.run.app/health   # Health check
https://backtest-agent-aj3kkr4xeq-uc.a.run.app/tools    # List tools
https://backtest-agent-aj3kkr4xeq-uc.a.run.app/docs     # API docs
```

**Note**: The deployed API provides information endpoints only. Use `adk web` for interactive agent functionality.

## Performance

- **Parallel data loading**: 4x speedup when fetching multiple symbols
- **Single backtest**: 50-100ms execution time
- **50-parameter optimization**: 3-5 seconds

## Capstone Requirements

Demonstrates 4 Enterprise Agents Track concepts (3 required):

1. **LLM-powered Agent**: Root agent using Gemini 2.0 Flash for natural language understanding and workflow orchestration
2. **Custom Tools**: 15 ADK-compatible tools for data fetching, backtesting, and optimization
3. **Session Management**: Conversation state persistence through ADK's session framework
4. **Agent Deployment**: Production deployment on Google Cloud Run with health checks and monitoring

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

**Author**: 0xhubed
**GitHub**: [@0xhubed](https://github.com/0xhubed)

## Acknowledgments

- Google AI Agents Intensive Course
- Kaggle for cryptocurrency dataset
- Google ADK team

**Last Updated**: November 29, 2025
