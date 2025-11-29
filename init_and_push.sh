#!/bin/bash

# Git initialization and push script for backtest-agent
# Run this after reviewing the migrated files

REPO_URL="$1"

if [ -z "$REPO_URL" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Git Repository Initialization Script"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Usage: ./init_and_push.sh <repository-url>"
    echo ""
    echo "Examples:"
    echo "  ./init_and_push.sh git@github.com:yourusername/backtest-agent.git"
    echo "  ./init_and_push.sh https://github.com/yourusername/backtest-agent.git"
    echo ""
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Initializing Git Repository"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Repository URL: $REPO_URL"
echo ""

# Step 1: Initialize git
echo "📝 Initializing git repository..."
git init

# Step 2: Configure git (if not already configured globally)
echo "⚙️  Configuring git..."
if [ -z "$(git config user.name)" ]; then
    echo "Enter your name for git commits:"
    read git_name
    git config user.name "$git_name"
fi

if [ -z "$(git config user.email)" ]; then
    echo "Enter your email for git commits:"
    read git_email
    git config user.email "$git_email"
fi

# Step 3: Create initial commit
echo "📦 Creating initial commit..."
git add .
git commit -m "Initial commit: BackTestPilot ADK Agent

- Multi-agent AI system for cryptocurrency backtesting
- Built with Google ADK and Gemini 2.0 Flash
- Supports 5 trading strategies: SMA, RSI, Bollinger Bands, MACD, Buy & Hold
- Includes comprehensive risk analysis and parameter optimization
- Ready for Google Cloud Run deployment

Project for Google AI Agents Intensive Course Capstone"

# Step 4: Set up remote and push
echo "🚀 Pushing to remote repository..."
git branch -M main
git remote add origin "$REPO_URL"
git push -u origin main

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Repository initialized and pushed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "  1. Visit: $(echo $REPO_URL | sed 's/\.git$//' | sed 's/git@github.com:/https:\/\/github.com\//')"
echo "  2. Set up virtual environment: python3.11 -m venv venv"
echo "  3. Activate: source venv/bin/activate"
echo "  4. Install: pip install -r requirements.txt"
echo "  5. Run: adk web"
echo ""

