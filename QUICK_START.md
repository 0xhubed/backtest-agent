# BackTest Agent - Quick Start Guide

## 🚀 Run in 3 Steps

```bash
# 1. Activate Python 3.11 environment
source venv311/bin/activate

# 2. Start ADK web interface
adk web

# 3. Open http://localhost:8000 in browser
```

Or just run: `./run_adk.sh`

---

## 💬 Try These First

**Check what's available:**
```
What cryptocurrencies are available?
```

**Simple backtest:**
```
Backtest SMA(20,50) on BTC from 2024 to 2025
```

**Compare strategies:**
```
Compare SMA vs RSI on ETH from 2023 to 2025
```

**Optimize parameters:**
```
Find best SMA parameters for SOL with Sharpe > 1.5
```

---

## 📊 18 Cryptocurrencies Available

**Major:** BTC, ETH, BNB, LTC, XRP
**DeFi:** SOL, LINK, UNI, AVAX, DOT
**Others:** ADA, DOGE, SHIB, TRX, TON, LEO, BCH, NEAR

**Data Range:** Through November 27, 2025 (updated daily)

---

## 🎯 5 Trading Strategies

1. **SMA Crossover** - Trend following
2. **RSI Mean Reversion** - Oversold/overbought
3. **Bollinger Bands** - Volatility breakout
4. **MACD** - Momentum
5. **Buy & Hold** - Baseline

---

## 📁 Key Files

- `EXAMPLE_QUERIES.md` - 50+ example queries
- `READY_TO_RUN.md` - Complete guide
- `run_adk.sh` - Quick start script

---

## ⚙️ Environment

- **Python:** 3.11.13
- **Google ADK:** 1.19.0
- **Data:** 18 cryptocurrencies, 2010-2025
- **Status:** 🟢 Ready!
