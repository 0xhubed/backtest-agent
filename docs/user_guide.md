# BackTestPilot User Guide

Welcome to BackTestPilot! This guide will help you get started with AI-powered trading strategy backtesting and optimization.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Advanced Features](#advanced-features)
4. [Query Syntax Guide](#query-syntax-guide)
5. [Understanding Results](#understanding-results)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## Getting Started

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/backTestPilot.git
cd backTestPilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download dataset
kaggle datasets download -d paveljurke/crypto-prices-historical-data
unzip crypto-prices-historical-data.zip -d data/raw/

# Configure credentials
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### First Run

```bash
# Test the system
python src/main.py --query "Backtest SMA on BTC from 2023 to 2025"
```

If successful, you'll see a comprehensive backtest report!

---

## Basic Usage

### Command Line Interface (CLI)

**Single Query**:
```bash
python src/main.py --query "YOUR_QUERY_HERE"
```

**Interactive Mode**:
```bash
python src/main.py --interactive
```
This starts a conversational session where you can ask follow-up questions.

**Examples**:
```bash
# Simple backtest
python src/main.py --query "Backtest SMA(20,50) on BTC from 2023 to 2025"

# Strategy comparison
python src/main.py --query "Compare SMA vs RSI on ETH"

# Multi-asset analysis
python src/main.py --query "Test Buy-and-Hold on BTC, ETH, and LTC"

# Optimization
python src/main.py --query "Find the best SMA parameters for BTC with Sharpe > 1.5"
```

### Python API

```python
from src.agents.user_agent import UserAgent

# Initialize agent
agent = UserAgent()

# Submit request
result = await agent.process_request(
    query="Compare SMA vs RSI on BTC from 2023 to 2025"
)

# Access results
print(f"Best Strategy: {result['best_strategy']}")
print(f"Sharpe Ratio: {result['metrics']['sharpe_ratio']:.2f}")
```

### REST API

```bash
# Start server
uvicorn deployment.api:app --host 0.0.0.0 --port 8000

# Submit backtest request
curl -X POST http://localhost:8000/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Compare SMA vs RSI on BTC from 2023 to 2025"
  }'

# Get experiment results
curl http://localhost:8000/experiments/42
```

---

## Advanced Features

### 1. Goal-Driven Optimization

Tell BackTestPilot your targets and it will automatically optimize parameters.

**Example**:
```
Query: "Find SMA parameters for BTC with Sharpe > 1.5 and max drawdown < 15%"

Output:
  Iteration 1: SMA(10,50) → Sharpe 1.32, DD 18% ❌
  Iteration 2: SMA(15,45) → Sharpe 1.41, DD 16% ❌
  Iteration 3: SMA(12,55) → Sharpe 1.52, DD 14.8% ✅

  ✨ Optimal Configuration:
     Short SMA: 12 days
     Long SMA: 55 days
```

**Target Syntax**:
- `Sharpe > 1.5` - Minimum Sharpe ratio
- `Sharpe ratio > 1.5` - Same as above
- `max drawdown < 15%` - Maximum acceptable drawdown
- `return > 50%` - Minimum total return
- `win rate > 50%` - Minimum percentage of winning trades

### 2. Multi-Asset, Multi-Strategy Comparison

Compare multiple strategies across multiple assets simultaneously.

**Example**:
```
Query: "Compare SMA, RSI, and Bollinger Bands on BTC and ETH"

This executes 6 backtests in parallel:
  1. SMA on BTC
  2. SMA on ETH
  3. RSI on BTC
  4. RSI on ETH
  5. Bollinger Bands on BTC
  6. Bollinger Bands on ETH

Output: Ranked table of all combinations
```

### 3. Memory Recall

BackTestPilot remembers all your past experiments.

**Example**:
```
Query: "What was our best BTC strategy from last week?"

Output:
  🔍 Searching experiment history...

  Found 8 BTC experiments from the past 7 days.

  Best Performer:
    Date: Nov 10, 2025
    Strategy: SMA(12,55)
    Sharpe: 1.68
    Return: 78%
```

**Memory Queries**:
- "What was our best strategy last week?"
- "Show me all ETH backtests from October"
- "Compare today's results to last month"

### 4. Portfolio-Level Backtesting

Test strategies across a portfolio of assets.

**Example**:
```
Query: "Backtest an equal-weight portfolio of BTC, ETH, and LTC with monthly rebalancing"

Output:
  Portfolio Performance:
    Total Return: 85%
    Sharpe Ratio: 1.42
    Diversification Benefit: +0.28 Sharpe vs best individual asset
```

### 5. Conversational Refinement

Have a multi-turn conversation to refine your strategy.

**Example Session**:
```
You: "Backtest SMA on BTC from 2023 to 2025"
Agent: [Shows results: Sharpe 1.32]

You: "Now try RSI instead"
Agent: [Shows RSI results: Sharpe 1.08]

You: "The SMA was better. Can you optimize it to get Sharpe > 1.5?"
Agent: [Runs optimization, finds SMA(12,55) with Sharpe 1.52]

You: "Perfect! Now test that on ETH"
Agent: [Tests SMA(12,55) on ETH: Sharpe 1.68]
```

---

## Query Syntax Guide

### Supported Strategies

| Strategy | Query Syntax | Parameters |
|----------|--------------|------------|
| **SMA Crossover** | `SMA`, `SMA(20,50)` | Short period, Long period |
| **RSI Mean Reversion** | `RSI`, `RSI(14,30-70)` | Period, Lower threshold, Upper threshold |
| **Bollinger Bands** | `Bollinger`, `BB(20,2)` | Period, Standard deviations |
| **MACD** | `MACD`, `MACD(12,26,9)` | Fast, Slow, Signal |
| **Buy and Hold** | `Buy-and-Hold`, `BuyHold`, `BH` | None (baseline) |

### Supported Symbols

- **BTC** - Bitcoin
- **ETH** - Ethereum
- **LTC** - Litecoin
- **XRP** - Ripple

### Date Specifications

**Absolute Dates**:
- `from 2023 to 2025`
- `from 2023-01-01 to 2025-11-28`
- `from Jan 2023 to Nov 2025`

**Relative Dates**:
- `last year`
- `last 6 months`
- `past 90 days`

**Default**: If no date range specified, uses all available data (updated daily through 2025).

### Query Templates

**1. Simple Backtest**:
```
"Backtest [STRATEGY] on [SYMBOL] from [START] to [END]"
```
Example: `"Backtest SMA(20,50) on BTC from 2023 to 2025"`

**2. Strategy Comparison**:
```
"Compare [STRATEGY1] vs [STRATEGY2] on [SYMBOL]"
```
Example: `"Compare SMA vs RSI vs Buy-and-Hold on ETH"`

**3. Multi-Asset**:
```
"Test [STRATEGY] on [SYMBOL1], [SYMBOL2], and [SYMBOL3]"
```
Example: `"Test RSI on BTC, ETH, and LTC"`

**4. Optimization**:
```
"Find [STRATEGY] parameters for [SYMBOL] with [TARGET1] and [TARGET2]"
```
Example: `"Find SMA parameters for BTC with Sharpe > 1.5 and drawdown < 15%"`

**5. Memory Recall**:
```
"What was our best [SYMBOL] strategy [TIME_PERIOD]?"
```
Example: `"What was our best ETH strategy last month?"`

---

## Understanding Results

### Performance Metrics

**Sharpe Ratio** (risk-adjusted return)
- **> 1.5**: Excellent
- **1.0 - 1.5**: Good
- **0.5 - 1.0**: Acceptable
- **< 0.5**: Poor

**Sortino Ratio** (downside risk)
- Similar to Sharpe but only penalizes downside volatility
- Higher is better

**Maximum Drawdown** (peak-to-trough decline)
- **< 10%**: Conservative
- **10-20%**: Moderate
- **20-30%**: Aggressive
- **> 30%**: High risk

**Calmar Ratio** (return / max drawdown)
- Higher is better
- Measures return per unit of risk

**Win Rate** (% of profitable trades)
- **> 60%**: Very good
- **50-60%**: Good
- **40-50%**: Acceptable
- **< 40%**: Poor (unless large winners)

**Profit Factor** (gross profit / gross loss)
- **> 2.0**: Excellent
- **1.5 - 2.0**: Good
- **1.0 - 1.5**: Acceptable
- **< 1.0**: Losing strategy

### Output Format

**Summary Table**:
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
  Calmar Ratio:      3.20
  Volatility:        24.5% (annualized)

Trade Statistics:
  Total Trades:      42
  Win Rate:          47%
  Profit Factor:     1.85
  Avg Trade:         1.39%
  Best Trade:        12.5%
  Worst Trade:       -8.3%
```

**Comparison Table**:
```
Rankings by Sharpe Ratio:

 Rank │ Strategy        │ Asset │ Sharpe │ Return │ Drawdown │ Trades
──────┼─────────────────┼───────┼────────┼────────┼──────────┼────────
  1   │ SMA(10,50)      │ ETH   │  1.68  │ 78.3%  │  14.2%   │   38
  2   │ SMA(12,55)      │ BTC   │  1.52  │ 62.1%  │  16.8%   │   35
  3   │ RSI(14,30-70)   │ ETH   │  1.38  │ 54.2%  │  12.5%   │   52
```

**Visualizations**:
- **Equity Curve**: Shows cumulative returns over time with buy/sell signals
- **Drawdown Chart**: Visualizes underwater periods
- **Parameter Heatmap**: Shows performance across parameter combinations

---

## Best Practices

### 1. Always Include a Baseline

Compare your strategy against Buy-and-Hold to see if active management adds value.

```
Query: "Compare SMA vs Buy-and-Hold on BTC"
```

If your strategy doesn't beat Buy-and-Hold on a risk-adjusted basis (Sharpe), stick with passive investing!

### 2. Test on Multiple Assets

A strategy that works on BTC might fail on ETH. Always validate across assets.

```
Query: "Test SMA(20,50) on BTC, ETH, SOL, and LINK"
```

### 3. Beware of Overfitting

If you optimize extensively on the same data, your strategy may not generalize.

**Solution**: Use walk-forward optimization or train/test splits (coming soon).

### 4. Consider Transaction Costs

BackTestPilot assumes zero transaction costs. In reality, frequent trading incurs:
- Exchange fees (0.1-0.5%)
- Slippage (0.05-0.2%)

**Rule of Thumb**: If average trade profit < 1%, strategy may not be profitable after costs.

### 5. Combine Metrics

Don't optimize for Sharpe alone. Consider:
- **Sharpe > 1.5** AND **Max Drawdown < 15%** AND **Win Rate > 45%**

### 6. Use Proper Date Ranges

Ensure sufficient data for your indicators:
- SMA(200): Need at least 200 days of history
- RSI(14): Need at least 14 days

BackTestPilot validates this automatically but it's good to be aware.

---

## Troubleshooting

### "No data found for symbol"

**Problem**: Symbol not in dataset or misspelled.

**Solution**:
- Check spelling (BTC not Bitcoin)
- Use supported symbols: BTC, ETH, LTC, XRP, BNB, ADA, DOGE, SOL, LINK, and more (18+ cryptocurrencies)

### "Insufficient data for strategy"

**Problem**: Not enough historical data for indicators.

**Solution**:
- Extend date range (e.g., start from 2022 instead of 2025)
- Use shorter indicator periods (e.g., SMA(10,30) instead of SMA(100,200))

### "Optimization did not meet targets"

**Problem**: Targets may be unrealistic for the strategy/asset.

**Solution**:
- Lower targets (e.g., Sharpe > 1.2 instead of > 2.0)
- Try a different strategy
- Review the best attempt (returned even if targets not met)

### "API timeout"

**Problem**: Request taking too long (> 5 minutes).

**Solution**:
- Reduce number of assets/strategies
- Shorten date range
- Disable optimization

### Slow performance

**Problem**: Backtests taking longer than expected.

**Solution**:
- Ensure parallel execution is enabled (default)
- Use vectorized strategies (built-in ones are optimized)
- Check CPU usage - may need more resources

---

## FAQ

**Q: How accurate are the backtests?**

A: BackTestPilot uses historical price data and simulates trades based on closing prices. Results are indicative but may not reflect real-world trading due to:
- Slippage
- Transaction costs
- Liquidity constraints
- Market impact

**Q: Can I add my own strategies?**

A: Yes! See `src/strategies/base_strategy.py` for the interface. Implement your strategy as a subclass and it will be automatically available.

**Q: What's the difference between Sharpe and Sortino ratio?**

A: Sharpe penalizes all volatility (up and down). Sortino only penalizes downside volatility. Sortino is more relevant for strategies with asymmetric returns.

**Q: Why is my Sharpe ratio negative?**

A: Negative Sharpe means your strategy lost money (negative mean return). Higher negative values mean worse performance.

**Q: Can I backtest options or futures?**

A: Not currently. BackTestPilot only supports spot cryptocurrency backtesting.

**Q: How is risk-free rate handled?**

A: Default is 0% (common for crypto). Can be adjusted in configuration for traditional assets.

**Q: What's the maximum backtest duration?**

A: Dataset is updated daily and covers historical data through 2025. You can backtest any period with sufficient data.

**Q: Can I export results?**

A: Yes! Results are saved to the experiment database (`experiments/history.db`) and can be exported as JSON, CSV, or PDF reports.

**Q: Is my data secure?**

A: All processing happens locally or in your Cloud Run instance. No backtest data is sent to third parties (except LLM queries to Gemini for parsing/reporting, which don't include sensitive data).

**Q: How much does it cost to run?**

A:
- **Local**: Free (just compute resources)
- **Cloud Run**: Pay-per-use (~$0.10 per 1000 backtests with scaling to zero)
- **Gemini API**: ~$0.01 per request (UserAgent + ReportAgent calls)

**Q: Can I use this for live trading?**

A: BackTestPilot is designed for research and backtesting only. Live trading integration is not included. Always paper trade before going live!

---

## Next Steps

Now that you're familiar with BackTestPilot, try:

1. **Run the demo notebook**: `jupyter notebook notebooks/03_demo.ipynb`
2. **Experiment with different strategies**: Test your own trading ideas
3. **Optimize for your risk tolerance**: Set appropriate targets
4. **Compare across multiple assets**: Find the best opportunities
5. **Build custom strategies**: Extend the system with your own logic

Happy backtesting! 📈

---

## Support

- **Issues**: https://github.com/yourusername/backTestPilot/issues
- **Documentation**: https://github.com/yourusername/backTestPilot/tree/main/docs
- **Email**: your.email@example.com

---

*Last Updated: November 17, 2025*
