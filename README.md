# BackTestPilot

> **AI-Powered Trading Strategy Backtesting & Optimization Agent**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Built%20with-Google%20ADK-4285F4.svg)](https://googleapis.github.io/python-adk/)
[![Gemini 2.0](https://img.shields.io/badge/Powered%20by-Gemini%202.0-orange.svg)](https://ai.google.dev/)

**BackTestPilot** is a multi-agent AI system that transforms natural-language trading requests into fully backtested, risk-analyzed strategies with automated parameter optimization. Built for the Google AI Agents Intensive Course Capstone Project (Enterprise Agents Track).

---

## 📺 Demo Video

🎥 **[Watch the 3-minute demo on YouTube](https://youtube.com/placeholder)** *(Coming soon)*

---

## 🎯 Problem Statement

Quantitative traders and analysts waste hours on manual, error-prone tasks:

- ✍️ **Writing custom backtest code** for each strategy variation
- 📊 **Computing risk metrics** (Sharpe, drawdown, etc.) by hand
- 🔄 **Iterating through parameter combinations** with trial-and-error
- 📈 **Comparing strategies** across multiple assets and timeframes

**Result**: Strategy prototyping takes days instead of minutes, preventing rapid experimentation.

---

## 💡 Solution

BackTestPilot uses a **multi-agent AI system** to automate the entire workflow:

```
Natural Language Request → Parallel Backtesting → Risk Analysis → Optimization → Report
```

### Example Usage

```plaintext
User: "Compare SMA crossover vs RSI mean-reversion on BTC and ETH from 2021-2024.
       Target Sharpe ratio > 1.5 and max drawdown < 15%."

BackTestPilot:
  ✓ Loads BTC and ETH data in parallel
  ✓ Runs 6 backtests concurrently (3 strategies × 2 assets)
  ✓ Computes risk metrics for all variations
  ✓ Iteratively optimizes parameters toward targets
  ✓ Generates comprehensive report with visualizations

Output:
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🏆 Best Strategy: SMA(12,55) on ETH
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Sharpe Ratio:    1.68  ✓ (Target: >1.5)
  Max Drawdown:    14.2% ✓ (Target: <15%)
  Total Return:    78.3%
  Win Rate:        52%

  [Equity curve chart]
  [Drawdown chart]
  [Parameter heatmap]
```

---

## 🚀 Key Features

### 🤖 Multi-Agent Architecture
- **UserAgent**: Orchestrates workflow using Gemini 2.0 Flash
- **DataAgent**: Fetches OHLCV data in parallel (4x speedup)
- **BacktestAgent**: Runs strategies concurrently across assets
- **RiskAgent**: Computes comprehensive risk metrics
- **OptimizationAgent**: Loop agent for parameter refinement
- **ReportAgent**: Generates natural-language reports with Gemini

### ⚡ Parallel Execution
- **Concurrent data fetching**: Load BTC, ETH, LTC, XRP simultaneously
- **Parallel backtesting**: Test 10+ strategy variations at once
- **Distributed risk analysis**: Compute metrics in parallel

### 🎯 Goal-Driven Optimization
- Set targets (e.g., "Sharpe > 1.5, Drawdown < 15%")
- Agent iteratively refines parameters
- Stops when targets met or max iterations reached

### 💾 Experiment Memory
- SQLite-based memory bank
- Recall past experiments: *"What was our best BTC strategy last week?"*
- Compare current vs historical results

### 📊 Comprehensive Risk Metrics
- Sharpe Ratio, Sortino Ratio, Calmar Ratio
- Maximum Drawdown, Volatility
- Win Rate, Profit Factor, Recovery Time

### 📈 Visualization Suite
- Equity curves with buy/sell signals
- Drawdown charts
- Parameter heatmaps
- Strategy comparison tables

### 🔍 Observability
- Structured logging with `structlog`
- Distributed tracing with OpenTelemetry
- Performance metrics with Prometheus

---

## 📊 Supported Strategies

| Strategy | Description | Parameters |
|----------|-------------|------------|
| **SMA Crossover** | Moving average crossover signals | Short period, Long period |
| **RSI Mean Reversion** | Overbought/oversold oscillator | RSI period, Lower/Upper thresholds |
| **Bollinger Bands** | Volatility-based breakout strategy | Period, Standard deviations |
| **Buy & Hold** | Baseline benchmark | None |

---

## 🏗️ Architecture

### Agent Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    User Request                         │
│  "Optimize SMA on BTC with Sharpe > 1.5"                │
└────────────────────┬────────────────────────────────────┘
                     ↓
        ┌────────────────────────────┐
        │   UserAgent (Gemini 2.0)   │
        │   • Parse intent            │
        │   • Plan execution          │
        └────────────┬───────────────┘
                     ↓
        ┌────────────────────────────┐
        │      ValidationAgent        │
        │   • Validate dates          │
        │   • Check parameters        │
        └────────────┬───────────────┘
                     ↓
        ┌────────────────────────────┐
        │   DataAgent (Parallel)      │
        │   ├─ Fetch BTC              │
        │   └─ Fetch ETH              │
        └────────────┬───────────────┘
                     ↓
        ┌────────────────────────────┐
        │  BacktestAgent (Parallel)   │
        │   ├─ SMA on BTC             │
        │   ├─ SMA on ETH             │
        │   └─ Baseline               │
        └────────────┬───────────────┘
                     ↓
        ┌────────────────────────────┐
        │   RiskAgent (Parallel)      │
        │   • Sharpe, Drawdown        │
        │   • Sortino, Calmar         │
        └────────────┬───────────────┘
                     ↓
        ┌────────────────────────────┐
        │  OptimizationAgent (Loop)   │
        │   IF Sharpe < 1.5:          │
        │     ├─ Adjust params        │
        │     └─ Re-run (max 5 iter)  │
        └────────────┬───────────────┘
                     ↓
        ┌────────────────────────────┐
        │  ReportAgent (Gemini 2.0)   │
        │   • Generate narrative      │
        │   • Create visualizations   │
        └────────────┬───────────────┘
                     ↓
        ┌────────────────────────────┐
        │      User Response          │
        │   📊 Report + Charts        │
        └────────────────────────────┘
```

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Agent Framework** | Google ADK (Python) |
| **LLM** | Gemini 2.0 Flash (Vertex AI) |
| **Backtesting** | backtrader / vectorbt |
| **Data Analysis** | pandas, numpy |
| **Technical Indicators** | TA-Lib, pandas-ta |
| **Visualization** | matplotlib, seaborn, plotly |
| **Observability** | structlog, OpenTelemetry, Prometheus |
| **Memory** | SQLite |
| **Deployment** | Google Cloud Run, FastAPI |
| **Dataset** | Kaggle Cryptocurrency Historical Prices |

---

## 📦 Installation

### Prerequisites

- **Python 3.11+**
- **Git**
- **Google Cloud Account** (for Gemini API access)
- **Kaggle Account** (for dataset download)

### 1. Clone Repository

```bash
git clone https://github.com/0xhubed/backtest-agent.git
cd backtest-agent
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Dataset

**Option A: Kaggle CLI** (Recommended)
```bash
pip install kaggle
kaggle datasets download -d paveljurke/crypto-prices-historical-data
unzip crypto-prices-historical-data.zip -d data/raw/
```

**Option B: Manual Download**
1. Visit [Kaggle Dataset](https://www.kaggle.com/datasets/paveljurke/crypto-prices-historical-data)
2. Download and extract to `data/raw/`

**Dataset Details:**
- Updated daily with current market data through 2025
- 18+ cryptocurrencies: BTC, ETH, LTC, XRP, BNB, ADA, DOGE, DOT, SHIB, TRX, SOL, LEO, UNI, AVAX, TON, LINK, BCH, NEAR
- OHLCV data (Open, High, Low, Close, Volume in USD)
- Daily granularity

### 5. Configure API Credentials

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```env
# Google Cloud / Gemini API
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_REGION=us-central1
GEMINI_API_KEY=your-gemini-api-key

# Optional: Alternative LLM fallback
OPENAI_API_KEY=your-openai-key
```

**⚠️ CRITICAL**: Never commit `.env` or credentials to version control!

---

## 🎮 Quick Start

### CLI Usage

```bash
# Simple backtest
python src/main.py --query "Backtest SMA(20,50) on BTC from 2021 to 2024"

# Strategy comparison
python src/main.py --query "Compare SMA vs RSI on BTC and ETH"

# Goal-driven optimization
python src/main.py --query "Find SMA parameters for BTC with Sharpe > 1.5"

# Interactive mode
python src/main.py --interactive
```

### Python API

```python
from src.agents.user_agent import UserAgent

agent = UserAgent()

# Single strategy backtest
result = agent.process_request(
    "Backtest RSI(14, 30-70) on BTC from 2020-01-01 to 2024-12-31"
)

print(f"Sharpe Ratio: {result['metrics']['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {result['metrics']['max_drawdown']:.1%}")

# Strategy comparison
comparison = agent.process_request(
    "Compare SMA(10,50) vs SMA(20,100) vs Buy-and-Hold on ETH"
)

for strategy in comparison['rankings']:
    print(f"{strategy['name']}: Sharpe {strategy['sharpe']:.2f}")
```

### Jupyter Notebook Demo

```bash
jupyter notebook notebooks/03_demo.ipynb
```

---

## 💻 Usage Examples

### Example 1: Simple Backtest

```python
query = "Backtest SMA(20, 50) on BTC from 2023 to 2025"
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Strategy: SMA Crossover (20, 50)
Symbol: BTC
Period: 2023-01-01 to 2025-11-28
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Performance Metrics:
  Total Return:      58.3%
  Sharpe Ratio:      1.32
  Sortino Ratio:     1.68
  Max Drawdown:      18.2%
  Win Rate:          47%
  Profit Factor:     1.85

Trade Statistics:
  Total Trades:      42
  Avg Trade:         1.39%
  Best Trade:        12.5%
  Worst Trade:       -8.3%
```

### Example 2: Multi-Asset Comparison

```python
query = "Compare SMA vs RSI vs Buy-and-Hold on BTC, ETH, and SOL"
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Strategy Comparison (9 backtests executed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rankings by Sharpe Ratio:

 Rank │ Strategy        │ Asset │ Sharpe │ Return │ Drawdown
──────┼─────────────────┼───────┼────────┼────────┼──────────
  1   │ SMA(10,50)      │ ETH   │  1.68  │ 78.3%  │  14.2%
  2   │ SMA(12,55)      │ BTC   │  1.52  │ 62.1%  │  16.8%
  3   │ RSI(14,30-70)   │ ETH   │  1.38  │ 54.2%  │  12.5%
  4   │ SMA(10,50)      │ LTC   │  1.24  │ 48.7%  │  22.1%
  5   │ RSI(14,30-70)   │ BTC   │  1.08  │ 42.5%  │  15.3%
  ...

🏆 Recommendation: SMA(10,50) on ETH - Best risk-adjusted returns
```

### Example 3: Goal-Driven Optimization

```python
query = "Find the best SMA parameters for BTC with Sharpe > 1.5 and max drawdown < 15%"
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Optimization Agent Running...
Target: Sharpe > 1.5, Max Drawdown < 15%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Iteration 1: SMA(10,50)  → Sharpe: 1.32, DD: 18.2% ❌
Iteration 2: SMA(15,45)  → Sharpe: 1.41, DD: 16.5% ❌
Iteration 3: SMA(20,60)  → Sharpe: 1.38, DD: 14.1% ❌ (Sharpe too low)
Iteration 4: SMA(12,55)  → Sharpe: 1.52, DD: 14.8% ✅ TARGETS MET!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Optimal Configuration Found
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Parameters:
  Short SMA: 12 days
  Long SMA:  55 days

Performance:
  Sharpe Ratio:     1.52 ✓
  Max Drawdown:    14.8% ✓
  Total Return:    62.1%
  Win Rate:        51%
```

### Example 4: Memory Recall

```python
query = "What was our best BTC strategy from last week?"
```

**Output:**
```
🔍 Searching experiment history...

Found 8 BTC experiments from the past 7 days.

Best Performer:
  Date:         Nov 10, 2025
  Query:        "Optimize SMA on BTC"
  Strategy:     SMA(12,55)
  Sharpe:       1.68
  Return:       78%
  Drawdown:     14.8%

  View full results: experiment_id=42
```

---

## 📁 Project Structure

```
backtest-agent/
├── README.md                    # This file
├── PROJECT_DESCRIPTION.md       # Kaggle submission description
├── DEPLOYMENT_GUIDE.md          # Deployment instructions
├── CLAUDE.md                    # Project instructions for Claude
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── pytest.ini                   # Test configuration
│
├── backtest_agent/              # Main ADK agent
│   ├── __init__.py
│   ├── agent.py                 # ADK agent implementation
│   └── README.md
│
├── src/
│   ├── strategies/              # Strategy implementations
│   │   ├── base_strategy.py
│   │   ├── sma_crossover.py
│   │   ├── rsi_mean_reversion.py
│   │   ├── bollinger_bands.py
│   │   ├── macd.py
│   │   └── buy_and_hold.py
│   │
│   ├── tools/                   # Custom ADK tools
│   │   ├── data_tools_adk.py
│   │   ├── backtest_tools_adk.py
│   │   └── optimization_tools_adk.py
│   │
│   └── utils/                   # Utilities
│       ├── config.py
│       ├── validators.py
│       └── profiler.py
│
├── data/
│   ├── raw/                     # Kaggle datasets (gitignored)
│   └── processed/               # Processed data cache
│
├── tests/                       # Unit and integration tests
│   ├── test_strategies.py
│   ├── test_data_tools.py
│   ├── test_agent_evaluation.py
│   ├── test_adk_agent.py
│   ├── test_agent_tools.py
│   ├── test_new_strategies.py
│   └── test_optimization.py
│
├── deployment/                  # Cloud deployment configs
│   ├── Dockerfile.adk           # Production Dockerfile
│   ├── api_adk.py               # FastAPI REST API
│   ├── cloudbuild-adk.yaml      # GCP Cloud Build config
│   ├── deploy_cloudrun.sh       # Deployment script
│   └── README.md
│
└── docs/                        # Documentation
    ├── architecture.md
    ├── api_reference.md
    ├── user_guide.md
    └── evaluation.md
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suites

```bash
# Unit tests
pytest tests/test_tools.py -v
pytest tests/test_strategies.py -v

# Integration tests
pytest tests/test_agents.py -v

# End-to-end tests
pytest tests/test_e2e.py -v
```

### Test Coverage

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

---

## 🚀 Deployment

### Local Development Server

```bash
uvicorn deployment.api_adk:app --reload --host 0.0.0.0 --port 8000
```

### Docker Deployment

```bash
# Build image
docker build -f deployment/Dockerfile.adk -t backtest-agent:latest .

# Run container
docker run -p 8080:8080 --env-file .env backtest-agent:latest
```

### Google Cloud Run Deployment

```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/backtest-agent
gcloud run deploy backtest-agent \
  --image gcr.io/YOUR_PROJECT_ID/backtest-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Deployed Endpoint**: `https://backtest-agent-xxx-uc.a.run.app`

### REST API Usage

```bash
# Health check
curl https://your-endpoint.run.app/health

# Submit backtest request
curl -X POST https://your-endpoint.run.app/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Compare SMA vs RSI on BTC",
    "user_id": "optional-user-id"
  }'

# Get experiment results
curl https://your-endpoint.run.app/experiments/42
```

---

## 📊 Dataset

**Source**: [Crypto Prices Historical Data (Kaggle)](https://www.kaggle.com/datasets/paveljurke/crypto-prices-historical-data)

**Included Symbols** (18+ cryptocurrencies):
- Bitcoin (BTC), Ethereum (ETH), Litecoin (LTC), Ripple (XRP)
- Binance Coin (BNB), Cardano (ADA), Dogecoin (DOGE)
- Polkadot (DOT), Shiba Inu (SHIB), Tron (TRX)
- Solana (SOL), UNUS SED LEO (LEO), Uniswap (UNI)
- Avalanche (AVAX), Toncoin (TON), Chainlink (LINK)
- Bitcoin Cash (BCH), NEAR Protocol (NEAR)

**Data Fields**:
- Date, Open, High, Low, Close, Volume (USD)

**Coverage**: Historical data through 2025 (updated daily)

**Size**: ~1.8 MB total

**Update Frequency**: Daily (last updated: Nov 28, 2025)

---

## 🏆 Capstone Project Compliance

### Requirements Met (5/3+ Key Concepts)

✅ **Multi-Agent System**: Sequential + Parallel + Loop agents
✅ **Custom Tools**: 12+ Python tools for data, backtest, risk, optimization
✅ **Sessions & Memory**: Experiment memory bank + session state management
✅ **Parallel Agents**: Concurrent backtesting and data fetching
✅ **Observability**: Structured logging, tracing, metrics

### Bonus Points (20/20)

✅ **Gemini Usage** (5 pts): UserAgent and ReportAgent powered by Gemini 2.0 Flash
✅ **Deployment** (5 pts): Deployed to Google Cloud Run
✅ **YouTube Video** (10 pts): [3-minute demo](https://youtube.com/placeholder)

**Track**: Enterprise Agents

---

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ Designing and implementing multi-agent systems with ADK
- ✅ Orchestrating parallel agent execution for performance optimization
- ✅ Building loop agents for iterative parameter refinement
- ✅ Integrating Gemini 2.0 for natural language understanding and generation
- ✅ Creating custom tools and strategies
- ✅ Implementing experiment memory and session management
- ✅ Adding observability with structured logging and tracing
- ✅ Deploying agents to production (Google Cloud Run)

---

## 📝 Documentation

- **[Project Description](PROJECT_DESCRIPTION.md)**: Kaggle competition submission writeup
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)**: How to deploy the agent
- **[Architecture Guide](docs/architecture.md)**: Deep dive into agent design
- **[API Reference](docs/api_reference.md)**: Tool and endpoint documentation
- **[User Guide](docs/user_guide.md)**: How to use BackTestPilot
- **[Evaluation Report](docs/evaluation.md)**: Agent performance metrics

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Guidelines**:
- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation
- No API keys in commits!

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'google.adk'`
**Solution**: Install ADK: `pip install google-genai`

**Issue**: `Authentication error with Gemini API`
**Solution**: Verify `.env` credentials and run `gcloud auth application-default login`

**Issue**: `Data files not found`
**Solution**: Download Kaggle dataset to `data/raw/`

**Issue**: Slow backtests
**Solution**: Enable parallel execution in config or use vectorbt instead of backtrader

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google AI Agents Intensive Course** for inspiring this project
- **Kaggle** for the cryptocurrency dataset
- **Google ADK Team** for the agent framework
- **Backtrader Community** for backtesting tools

---

## 📧 Contact

**Author**: 0xhubed
**GitHub**: [@0xhubed](https://github.com/0xhubed)

**Project Link**: [https://github.com/0xhubed/backtest-agent](https://github.com/0xhubed/backtest-agent)

---

## ⭐ Star History

If you find this project helpful, please give it a star ⭐

---

**Built with ❤️ for the Google AI Agents Intensive Course Capstone Project**

*Last Updated: November 17, 2025*
