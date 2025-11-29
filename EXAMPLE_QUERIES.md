# BackTestPilot ADK Agent - Example Queries

This file contains example queries that work with the Google ADK-based BackTestPilot agent.

## Data Coverage

**Dataset**: Crypto Prices Historical Data (Updated Daily through 2025)
**Total Cryptocurrencies**: 18
**Latest Data**: November 27, 2025

### Available Cryptocurrencies & Data Ranges

| Symbol | Name | Data Start | Data End | Days |
|--------|------|------------|----------|------|
| BTC | Bitcoin | 2010-07-14 | 2025-11-27 | 5,616 |
| ETH | Ethereum | 2015-08-08 | 2025-11-27 | 3,765 |
| SOL | Solana | 2020-04-11 | 2025-11-27 | 2,057 |
| LTC | Litecoin | Available | 2025-11-27 | ✓ |
| XRP | Ripple | Available | 2025-11-27 | ✓ |
| BNB | Binance Coin | Available | 2025-11-27 | ✓ |
| ADA | Cardano | Available | 2025-11-27 | ✓ |
| DOGE | Dogecoin | Available | 2025-11-27 | ✓ |
| DOT | Polkadot | Available | 2025-11-27 | ✓ |
| SHIB | Shiba Inu | Available | 2025-11-27 | ✓ |
| TRX | Tron | Available | 2025-11-27 | ✓ |
| LEO | UNUS SED LEO | Available | 2025-11-27 | ✓ |
| UNI | Uniswap | Available | 2025-11-27 | ✓ |
| AVAX | Avalanche | Available | 2025-11-27 | ✓ |
| TON | Toncoin | Available | 2025-11-27 | ✓ |
| LINK | Chainlink | Available | 2025-11-27 | ✓ |
| BCH | Bitcoin Cash | Available | 2025-11-27 | ✓ |
| NEAR | NEAR Protocol | Available | 2025-11-27 | ✓ |

**Note**: Strategies need 200+ days for indicator warmup. The agent will suggest valid date ranges if you ask.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1. SIMPLE BACKTESTS

### Basic Strategy Tests
"Backtest SMA(20,50) on BTC from 2024 to 2025"
"Test RSI on ETH from 2023-01-01 to 2025-11-27"
"Run Buy and Hold on BTC from 2022 to 2025"
"Test Bollinger Bands(20,2) on SOL from 2023 to 2025"
"Backtest MACD on LINK from 2024 to 2025"

### Test Recent Market Conditions
"Backtest SMA on BTC for the last year"
"Test RSI on SOL from 2024 to 2025"
"Run MACD on ETH from January 2024 to November 2025"

### Test Different Cryptocurrencies
"Backtest SMA(20,50) on DOGE from 2023 to 2025"
"Test RSI on ADA from 2024 to 2025"
"Run Bollinger Bands on UNI from 2023 to 2025"
"Test MACD on AVAX from 2024 to 2025"

### With Custom Parameters
"Backtest SMA with short period 10 and long period 30 on BTC from 2024 to 2025"
"Test RSI(14,30,70) on ETH from 2023 to 2025"
"Run Bollinger Bands with period 25 and std dev 2.5 on BTC from 2024 to 2025"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 2. DATA QUERIES

### Check Available Data
"What cryptocurrencies are available?"
"What date ranges are available for BTC?"
"Check if SOL data is available"
"What's the recommended date range for LINK backtesting?"
"Show me all 18 cryptocurrencies"

### Understand Data Coverage
"What dates should I use for BTC backtesting?"
"Show me available date ranges for all cryptocurrencies"
"What's the latest data available for ETH?"
"How much data do we have for Solana?"

### Verify Recent Data
"What's the most recent date for BTC data?"
"Check if we have 2025 data for ETH"
"Show me the data coverage for newer coins like SOL and AVAX"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 3. STRATEGY COMPARISONS

### Compare 2 Strategies
"Compare SMA vs RSI on BTC from 2024 to 2025"
"Compare Bollinger Bands vs MACD on ETH from 2023 to 2025"
"Compare Buy and Hold vs SMA on SOL from 2022 to 2025"

### Compare Multiple Strategies
"Compare SMA vs RSI vs Bollinger Bands on BTC from 2024 to 2025"
"Compare all strategies on ETH from 2023 to 2025"
"Test SMA, RSI, MACD, and Buy and Hold on LINK from 2024 to 2025"

### Multi-Asset Comparisons
"Compare SMA performance on BTC vs ETH vs SOL from 2024 to 2025"
"Test RSI on BTC, ETH, and LINK from 2023 to 2025"
"Compare MACD on all major cryptocurrencies from 2024 to 2025"
"Test SMA(20,50) on BTC, ETH, SOL, ADA, and DOGE from 2024 to 2025"

### Test Across Market Conditions
"Compare strategies on BTC during 2022 bear market vs 2024 recovery"
"Test RSI on SOL from 2023 to 2025 to see how it handles volatility"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 4. PARAMETER OPTIMIZATION

### Optimize for High Returns
"Find the best SMA parameters for BTC from 2024 to 2025"
"Optimize RSI on ETH for maximum Sharpe ratio from 2023 to 2025"
"Find optimal Bollinger Bands parameters for SOL from 2024 to 2025"

### Optimize with Specific Targets
"Find SMA parameters for BTC with Sharpe ratio > 1.5"
"Optimize RSI on ETH for max drawdown < 15%"
"Find Bollinger Bands parameters for LINK with Sharpe > 1.0"

### Optimize for Risk Management
"Find RSI parameters for BTC that minimize max drawdown from 2024 to 2025"
"Optimize SMA on ETH for lowest volatility from 2023 to 2025"
"Find MACD parameters for SOL with best risk-adjusted returns"

### Test on Different Coins
"Optimize SMA on DOGE from 2023 to 2025"
"Find best RSI parameters for ADA from 2024 to 2025"
"Optimize Bollinger Bands on UNI from 2023 to 2025"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 5. NATURAL LANGUAGE QUERIES

### Beginner-Friendly
"What's the best strategy for BTC?"
"Show me how SMA works on Bitcoin"
"Test a simple moving average strategy on BTC from 2024 to 2025"
"I want to backtest Solana"
"How does RSI perform on Ethereum?"

### More Complex
"I want to see how a 20-day and 50-day moving average crossover strategy would perform on Bitcoin from 2023 to 2025"
"Find me the best RSI settings to trade Ethereum with minimal risk"
"Compare trend-following strategies vs mean reversion on BTC from 2024 to 2025"
"Test if Bollinger Bands work better on volatile coins like SOL vs stable ones like BTC"

### Explore New Cryptocurrencies
"Test SMA on newer cryptocurrencies like SOL, AVAX, and UNI"
"Compare performance of the same strategy on established coins like BTC vs newer coins like TON"
"How does RSI work on meme coins like DOGE and SHIB?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 6. ADVANCED WORKFLOWS

### Optimization Then Testing
First: "Find the best SMA parameters for BTC from 2024-01-01 to 2024-12-31"
Then: "Now test those parameters on ETH for the same period"

### Compare Optimized vs Default
First: "Backtest SMA with default parameters on BTC from 2024 to 2025"
Then: "Now optimize SMA parameters for the same period and compare"

### Multiple Assets, Same Strategy
"Test SMA(20,50) on BTC, ETH, SOL, and LINK from 2024 to 2025"
"Compare MACD performance across all 18 cryptocurrencies from 2024 to 2025"
"Run RSI on the top 5 cryptocurrencies from 2023 to 2025"

### Cross-Asset Strategy Testing
"Test if SMA parameters optimized for BTC work well on ETH"
"Compare how the same RSI(14,30,70) performs on BTC vs SOL vs DOGE"
"Find one Bollinger Bands configuration that works across BTC, ETH, and SOL"

### Market Cycle Analysis
"Test Buy and Hold on BTC from 2022 to 2025 to see the full market cycle"
"Compare SMA vs RSI performance during 2024 bull market on multiple coins"
"Test strategies on SOL from 2023 to 2025 to capture its volatility"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## AVAILABLE STRATEGIES

1. **SMA Crossover** - Trend following with moving average crossovers
   Parameters: short_period (default: 20), long_period (default: 50)

2. **RSI Mean Reversion** - Oversold/overbought momentum strategy
   Parameters: period (default: 14), lower_threshold (default: 30), upper_threshold (default: 70)

3. **Bollinger Bands** - Mean reversion with volatility bands
   Parameters: period (default: 20), std_dev (default: 2.0)

4. **MACD** - Trend following momentum indicator
   Parameters: fast_period (default: 12), slow_period (default: 26), signal_period (default: 9)

5. **Buy & Hold** - Passive baseline strategy
   Parameters: None (just buy and hold)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## TIPS FOR EFFECTIVE QUERIES

1. **Use current date ranges**: Data goes through November 27, 2025
   ✅ "from 2024 to 2025"
   ✅ "from 2023-01-01 to 2025-11-27"
   ✅ "from 2022 to 2025"
   ❌ "from 2026 to 2027" (future dates!)

2. **Use natural language**: The AI understands many phrasings
   ✅ "Backtest SMA on BTC"
   ✅ "Test a moving average strategy on Bitcoin"
   ✅ "Run SMA crossover for BTC"

3. **For comparisons, use "vs"**:
   ✅ "Compare SMA vs RSI vs Bollinger Bands"
   ✅ "Test SMA versus Buy and Hold"
   ✅ "Compare BTC vs ETH vs SOL"

4. **For optimization, state your goals**:
   ✅ "Find SMA with Sharpe > 1.5"
   ✅ "Optimize for lowest drawdown"
   ✅ "Find best parameters for high returns"

5. **Ask for date ranges if unsure**:
   "What date ranges are available for BTC?"
   "What dates should I use for SOL backtesting?"
   "Show me recommended date ranges for LINK"

6. **Explore all 18 cryptocurrencies**:
   ✅ Test on established coins: BTC, ETH, LTC, XRP
   ✅ Test on DeFi tokens: UNI, LINK, AVAX
   ✅ Test on newer coins: SOL, TON, NEAR
   ✅ Test on meme coins: DOGE, SHIB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## METRICS EXPLAINED

When you run a backtest, you'll see these metrics:

- **Total Return %**: Total profit/loss as a percentage
- **Sharpe Ratio**: Risk-adjusted returns (higher is better, >1 is good, >2 is excellent)
- **Max Drawdown**: Largest peak-to-trough decline (lower is better)
- **Sortino Ratio**: Like Sharpe but only penalizes downside volatility
- **Calmar Ratio**: Return divided by max drawdown
- **Volatility**: Annualized standard deviation of returns
- **Win Rate**: Percentage of profitable periods
- **Profit Factor**: Gross profit / gross loss
- **Trades**: Number of trades executed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SAMPLE QUERY WORKFLOW

Here's a complete workflow example:

```
1. "What cryptocurrencies are available?"
   → See all 18 available cryptocurrencies

2. "What date ranges are available for SOL?"
   → Get recommended date ranges for Solana

3. "Backtest SMA(20,50) on SOL from 2023 to 2025"
   → Run initial backtest with default parameters

4. "Compare SMA vs RSI vs MACD on SOL from 2023 to 2025"
   → See which strategy performs best

5. "Optimize the best strategy for SOL with Sharpe > 1.5"
   → Fine-tune parameters for better performance

6. "Test the optimized parameters on BTC and ETH for the same period"
   → Validate if the strategy works across different coins
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Last Updated**: November 29, 2025
**Dataset Version**: Daily updates through 2025-11-27
**Agent**: BackTestPilot using Google ADK 1.19.0 with Gemini 2.0 Flash
**Total Tools**: 15 (6 data, 6 backtest, 3 optimization)
**Total Cryptocurrencies**: 18
