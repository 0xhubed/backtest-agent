# Dataset Update Guide

## What Changed

The project has been updated to use a newer, actively maintained cryptocurrency dataset from Kaggle.

### Old Dataset
- **Source**: Cryptocurrency Historical Prices by sudalairajkumar
- **Last Update**: 2021-07-06
- **Symbols**: 4 cryptocurrencies (BTC, ETH, LTC, XRP)
- **File Names**: `coin_Bitcoin.csv`, `coin_Ethereum.csv`, etc.

### New Dataset
- **Source**: [Crypto Prices Historical Data by paveljurke](https://www.kaggle.com/datasets/paveljurke/crypto-prices-historical-data)
- **Last Update**: Daily updates through 2025 (last: Nov 28, 2025)
- **Symbols**: 18+ cryptocurrencies (BTC, ETH, LTC, XRP, BNB, ADA, DOGE, DOT, SHIB, TRX, SOL, LEO, UNI, AVAX, TON, LINK, BCH, NEAR)
- **File Names**: `BTC.csv`, `ETH.csv`, etc.

## How to Update

### Step 1: Download New Dataset

```bash
# Using Kaggle CLI (recommended)
pip install kaggle
kaggle datasets download -d paveljurke/crypto-prices-historical-data
unzip crypto-prices-historical-data.zip -d data/raw/

# Or download manually from:
# https://www.kaggle.com/datasets/paveljurke/crypto-prices-historical-data
```

### Step 2: Remove Old Data (Optional)

```bash
# Backup old data first
mv data/raw data/raw_old

# Create new directory
mkdir -p data/raw

# Then download new dataset to data/raw
```

### Step 3: Clear Cache

```bash
# Remove old cached data
rm -rf data/processed/*
```

### Step 4: Update Your Code

The project code has already been updated. If you have custom scripts, update:

**Old file names:**
```python
SUPPORTED_SYMBOLS = {
    "BTC": "coin_Bitcoin.csv",
    "ETH": "coin_Ethereum.csv",
}
```

**New file names:**
```python
SUPPORTED_SYMBOLS = {
    "BTC": "BTC.csv",
    "ETH": "ETH.csv",
}
```

## New Cryptocurrencies Available

You can now backtest on these additional cryptocurrencies:
- **BNB** - Binance Coin
- **ADA** - Cardano
- **DOGE** - Dogecoin
- **DOT** - Polkadot
- **SHIB** - Shiba Inu
- **TRX** - Tron
- **SOL** - Solana
- **LEO** - UNUS SED LEO
- **UNI** - Uniswap
- **AVAX** - Avalanche
- **TON** - Toncoin
- **LINK** - Chainlink
- **BCH** - Bitcoin Cash
- **NEAR** - NEAR Protocol

## Updated Date Ranges

### Old Examples (2021 data)
```bash
# These won't work anymore
"Backtest SMA on BTC from 2021 to 2024"
"Compare strategies from 2020 to 2021"
```

### New Examples (2025 data)
```bash
# Use current dates
"Backtest SMA on BTC from 2023 to 2025"
"Compare SMA vs RSI on SOL from 2022 to 2025"
"Optimize Bollinger Bands on ETH from Jan 2024 to Nov 2025"
```

## Benefits

1. **Current Data**: Test strategies on recent market conditions (2022-2025)
2. **More Assets**: 18+ cryptocurrencies vs 4
3. **Active Maintenance**: Daily updates vs static 2021 dataset
4. **Recent Events**: Includes major market events like:
   - 2022 crypto winter
   - 2024 Bitcoin halving
   - 2024 ETF approvals
   - 2025 market trends

## Testing

After updating, verify everything works:

```bash
# Test data loading
adk web

# In the web UI, try:
# "What cryptocurrencies are available?"
# "Backtest SMA(20,50) on SOL from 2024 to 2025"
```

## Troubleshooting

### Error: "Data file not found"
- Make sure you downloaded the new dataset to `data/raw/`
- Check that CSV files are named correctly (e.g., `BTC.csv` not `coin_Bitcoin.csv`)

### Error: "No data for requested date range"
- The new dataset has different start dates for each cryptocurrency
- Use `get_recommended_date_ranges()` to check available dates
- Or ask the agent: "What date ranges are available for SOL?"

### Old cache conflicts
- Clear the cache: `rm -rf data/processed/*`
- The system will rebuild cache with new data

## Questions?

Check the updated documentation:
- [README.md](README.md) - Installation and usage
- [docs/user_guide.md](docs/user_guide.md) - Detailed examples
- [backtest_agent/agent.py](backtest_agent/agent.py) - Agent instructions

---

**Last Updated**: November 29, 2025
