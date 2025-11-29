# BackTest Agent - Documentation Index

Welcome! Here's where to find everything.

## 🚀 Getting Started

1. **[QUICK_START.md](QUICK_START.md)** - Run in 3 steps
2. **[READY_TO_RUN.md](READY_TO_RUN.md)** - Complete setup guide
3. **[EXAMPLE_QUERIES.md](EXAMPLE_QUERIES.md)** - 50+ query examples

## 📚 Main Documentation

- **[README.md](README.md)** - Project overview & full documentation
- **[PROJECT_DESCRIPTION.md](PROJECT_DESCRIPTION.md)** - Technical details
- **[DEPLOYMENT_OPTIONS.md](DEPLOYMENT_OPTIONS.md)** - Compare all deployment options ⭐
- **[CLOUDRUN_DEPLOYMENT.md](CLOUDRUN_DEPLOYMENT.md)** - Complete Cloud Run guide
- **[CLOUDRUN_QUICKSTART.md](CLOUDRUN_QUICKSTART.md)** - 5-minute deployment

## 🔧 Setup & Configuration

- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - What's installed
- **[API_KEY_SETUP.md](API_KEY_SETUP.md)** - Get Gemini API key
- **[DATASET_UPDATE.md](DATASET_UPDATE.md)** - Dataset migration guide
- **[PYTHON38_WORKAROUND.md](PYTHON38_WORKAROUND.md)** - Python version info
- **[.env.example](.env.example)** - Environment variables template

## 📖 Detailed Guides

- **[docs/user_guide.md](docs/user_guide.md)** - Usage examples
- **[docs/architecture.md](docs/architecture.md)** - System design
- **[docs/api_reference.md](docs/api_reference.md)** - API documentation
- **[docs/evaluation.md](docs/evaluation.md)** - Performance metrics

## 🛠️ Scripts

- **[run_adk.sh](run_adk.sh)** - Quick start script (local)
- **[install_python310.sh](install_python310.sh)** - Python upgrade helper
- **[test_docker_build.sh](test_docker_build.sh)** - Test Docker locally
- **[deployment/deploy_cloudrun.sh](deployment/deploy_cloudrun.sh)** - Deploy to Cloud Run

## 📊 Data

- **Location:** `data/raw/` - 18 cryptocurrency CSV files
- **Dataset:** Kaggle Crypto Prices Historical Data
- **Updated:** Daily through November 27, 2025
- **Size:** 4.3 MB (18 cryptocurrencies)

## 🧪 Testing

- **[tests/](tests/)** - Unit and integration tests
- **[pytest.ini](pytest.ini)** - Test configuration

## 🚢 Deployment

- **[deployment/](deployment/)** - Cloud deployment files
  - `api_adk.py` - FastAPI REST API
  - `Dockerfile.adk` - Docker image
  - `cloudbuild-adk.yaml` - Cloud Build config

## 💻 Source Code

- **[backtest_agent/](backtest_agent/)** - Main ADK agent
- **[src/strategies/](src/strategies/)** - Trading strategies
- **[src/tools/](src/tools/)** - ADK tools
- **[src/utils/](src/utils/)** - Utilities

---

## Quick Reference

**Start the agent:**
```bash
./run_adk.sh
```

**First query to try:**
```
What cryptocurrencies are available?
```

**Example backtest:**
```
Backtest SMA(20,50) on BTC from 2024 to 2025
```

---

**Status:** 🟢 Ready to use
**Version:** 1.0.0
**Last Updated:** November 29, 2025
