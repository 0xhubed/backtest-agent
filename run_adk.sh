#!/bin/bash
# Quick script to activate Python 3.11 venv and run ADK web

echo "=== BackTest Agent - ADK Web Interface ==="
echo "Activating Python 3.11 virtual environment..."
source venv311/bin/activate

echo "Starting ADK web interface..."
echo "Open http://localhost:8000 in your browser"
echo ""

adk web
