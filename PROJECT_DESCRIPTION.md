# BackTest-Agent

## Overview

BackTest-Agent is a cryptocurrency strategy analysis system built with Google ADK that enables natural language backtesting requests.

## Problem

Testing trading strategies involves repetitive manual work:
- Writing custom code for each strategy variation
- Running multiple backtests to test parameter combinations
- Comparing strategy performance across different cryptocurrencies

## Solution

An ADK agent orchestrates 15 specialized tools to automate the backtesting workflow through natural language queries.

**Example queries:**
- "What cryptocurrencies are available?"
- "Backtest SMA(20,50) on BTC from 2023 to 2025"
- "Compare SMA vs RSI on ETH"
- "Optimize RSI parameters for Sharpe ratio above 1.5"

**Agent workflow:**
1. Parses user intent (symbols, strategies, dates, targets)
2. Validates inputs against available data
3. Selects appropriate tools
4. Executes backtesting pipeline
5. Returns results with natural language explanations

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
- **Interface**: `adk web` (interactive chat)
- **Testing**: pytest (33 tests, 100% pass rate)
- **Deployment**: Google Cloud Run (FastAPI info API)

## Validation

**Tests**: 33 unit and integration tests covering data tools, strategy execution, and risk calculations

**Performance**:
- Parallel data loading (4x speedup)
- Single backtest: 50-100ms
- 50-parameter optimization: 3-5 seconds

## Usage

**Local development:**
```bash
adk web  # Interactive agent at localhost:8000
```

**Cloud deployment:**
- Info API: https://backtest-agent-aj3kkr4xeq-uc.a.run.app/
- Endpoints: `/health`, `/tools`, `/agent-info`, `/docs`

## Capstone Alignment

Demonstrates Enterprise Agents Track concepts:
- Natural language interfaces for domain workflows
- Tool-based architecture with specialized functions
- Automated data analysis and decision support
- Session management and contextual awareness

The system shows how ADK and Gemini can automate repetitive financial analysis tasks through conversation, though production use would require additional validation.
