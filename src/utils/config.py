"""
Configuration management for Backtest Agent.

This module loads environment variables and provides configuration constants
for the entire application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Google Cloud & Gemini Configuration
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "")
GOOGLE_REGION = os.getenv("GOOGLE_REGION", "us-central1")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Data Configuration
DATA_DIR = PROJECT_ROOT / os.getenv("DATA_DIR", "data/raw")
CACHE_DIR = PROJECT_ROOT / os.getenv("CACHE_DIR", "data/processed")

# Ensure data directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Database Configuration
DB_PATH = PROJECT_ROOT / os.getenv("DB_PATH", "experiments/history.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8080"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Financial Constants
RISK_FREE_RATE = float(os.getenv("RISK_FREE_RATE", "0.02"))  # 2% annual
TRADING_DAYS_PER_YEAR = 252

# Supported cryptocurrency symbols
# New dataset: Crypto Prices Historical Data (Updated daily)
# https://www.kaggle.com/datasets/paveljurke/crypto-prices-historical-data
SUPPORTED_SYMBOLS = {
    "BTC": "BTC.csv",
    "ETH": "ETH.csv",
    "LTC": "LTC.csv",
    "XRP": "XRP.csv",
    "BNB": "BNB.csv",
    "ADA": "ADA.csv",
    "DOGE": "DOGE.csv",
    "DOT": "DOT.csv",
    "SHIB": "SHIB.csv",
    "TRX": "TRX.csv",
    "SOL": "SOL.csv",
    "LEO": "LEO.csv",
    "UNI": "UNI.csv",
    "AVAX": "AVAX.csv",
    "TON": "TON.csv",
    "LINK": "LINK.csv",
    "BCH": "BCH.csv",
    "NEAR": "NEAR.csv"
}

# Backtest Configuration
DEFAULT_INITIAL_CAPITAL = 10000.0
DEFAULT_COMMISSION = 0.001  # 0.1% per trade

# Optimization Configuration
MAX_OPTIMIZATION_ITERATIONS = 5
OPTIMIZATION_TIMEOUT_SECONDS = 300  # 5 minutes
