#!/bin/bash
# Test Docker build locally before deploying to Cloud Run

set -e

echo "=== Testing Docker Build Locally ==="
echo ""

# Build the Docker image
echo "Building Docker image..."
docker build -f deployment/Dockerfile.adk -t backtest-agent:test .

echo ""
echo "✓ Docker image built successfully!"
echo ""

# Check image size
echo "Image size:"
docker images backtest-agent:test --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo ""
echo "To test locally, run:"
echo "  docker run -p 8080:8080 --env-file .env backtest-agent:test"
echo ""
echo "Then visit: http://localhost:8080/health"
echo ""
