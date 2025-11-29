# 🎉 BackTest Agent - Ready to Run!

## ✅ Setup Complete

Everything is installed and ready to use!

### What's Installed
- ✅ **Python 3.11.13** (upgraded from 3.8.10)
- ✅ **Google ADK 1.19.0** with CLI
- ✅ **18 Cryptocurrencies** with data through Nov 27, 2025
- ✅ **All dependencies** in Python 3.11 virtual environment
- ✅ **Kaggle CLI** configured

---

## 🚀 How to Run

### Option 1: Quick Start (Recommended)

```bash
./run_adk.sh
```

This will:
1. Activate the Python 3.11 virtual environment
2. Start the ADK web interface
3. Open at http://localhost:8000

### Option 2: Manual Start

```bash
# Activate Python 3.11 environment
source venv311/bin/activate

# Start ADK web
adk web
```

Then open http://localhost:8000 in your browser.

---

## 📝 Example Queries to Try

Once the web interface is open, try these queries:

```
What cryptocurrencies are available?
```

```
What date ranges are available for BTC?
```

```
Backtest SMA(20,50) on BTC from 2024 to 2025
```

```
Compare SMA vs RSI on SOL from 2023 to 2025
```

```
Optimize Bollinger Bands on ETH targeting Sharpe > 1.5
```

```
Backtest MACD on LINK from 2022 to 2025
```

---

## 📊 Available Data

### Cryptocurrencies (18 total)

| Symbol | Name | Data Range | Days |
|--------|------|------------|------|
| BTC | Bitcoin | 2010-07-14 to 2025-11-27 | 5,616 |
| ETH | Ethereum | 2015-08-08 to 2025-11-27 | 3,765 |
| SOL | Solana | 2020-04-11 to 2025-11-27 | 2,057 |
| LINK | Chainlink | Available | ✓ |
| ADA | Cardano | Available | ✓ |
| DOGE | Dogecoin | Available | ✓ |
| BNB | Binance Coin | Available | ✓ |
| DOT | Polkadot | Available | ✓ |
| SHIB | Shiba Inu | Available | ✓ |
| TRX | Tron | Available | ✓ |
| LTC | Litecoin | Available | ✓ |
| XRP | Ripple | Available | ✓ |
| LEO | UNUS SED LEO | Available | ✓ |
| UNI | Uniswap | Available | ✓ |
| AVAX | Avalanche | Available | ✓ |
| TON | Toncoin | Available | ✓ |
| BCH | Bitcoin Cash | Available | ✓ |
| NEAR | NEAR Protocol | Available | ✓ |

### Trading Strategies

- **SMA Crossover** - Moving average crossover signals
- **RSI Mean Reversion** - Overbought/oversold oscillator
- **Bollinger Bands** - Volatility-based breakout strategy
- **MACD** - Moving Average Convergence Divergence
- **Buy & Hold** - Baseline benchmark

---

## 🔧 Troubleshooting

### "adk: command not found"
Make sure you activated the venv:
```bash
source venv311/bin/activate
```

### Port already in use
If port 8000 is busy:
```bash
adk web --port 8080
```

### Need to update data
The dataset auto-updates daily. To manually refresh:
```bash
source venv311/bin/activate
kaggle datasets download -d paveljurke/crypto-prices-historical-data
unzip -o crypto-prices-historical-data.zip -d data/raw/
rm crypto-prices-historical-data.zip
```

---

## 📚 Documentation

- [SETUP_COMPLETE.md](SETUP_COMPLETE.md) - Full setup details
- [DATASET_UPDATE.md](DATASET_UPDATE.md) - Dataset migration guide
- [README.md](README.md) - Complete documentation
- [docs/user_guide.md](docs/user_guide.md) - Detailed usage examples

---

## 🎯 Next Steps

1. **Set up Gemini API Key** (required for AI features):
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

2. **Run the agent**:
   ```bash
   ./run_adk.sh
   ```

3. **Start backtesting!**

---

**Environment**: Python 3.11.13 | Google ADK 1.19.0 | Ubuntu 20.04 WSL2
**Status**: 🟢 Ready to use!
**Last Updated**: November 29, 2025
