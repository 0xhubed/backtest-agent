#!/bin/bash
# Install Python 3.10 on Ubuntu 20.04

echo "=== Installing Python 3.10 on Ubuntu 20.04 ==="

# Add deadsnakes PPA
echo "Adding deadsnakes PPA..."
sudo add-apt-repository ppa:deadsnakes/ppa -y

# Update package list
echo "Updating package list..."
sudo apt update

# Install Python 3.10
echo "Installing Python 3.10..."
sudo apt install python3.10 python3.10-venv python3.10-dev -y

# Verify installation
echo ""
echo "=== Python 3.10 Installation Complete ==="
python3.10 --version

echo ""
echo "Next steps:"
echo "1. Create virtual environment: python3.10 -m venv venv310"
echo "2. Activate it: source venv310/bin/activate"
echo "3. Install requirements: pip install -r requirements.txt"
