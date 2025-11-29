#!/bin/bash
# Deploy BackTestPilot to Google Cloud Run
# Usage: ./deploy_cloudrun.sh [PROJECT_ID]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}BackTestPilot - Cloud Run Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Get project ID from argument or prompt
if [ -z "$1" ]; then
    echo -e "${YELLOW}Enter your Google Cloud Project ID:${NC}"
    read PROJECT_ID
else
    PROJECT_ID=$1
fi

# Configuration
SERVICE_NAME="backtest-agent"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo -e "${GREEN}Configuration:${NC}"
echo "  Project ID: $PROJECT_ID"
echo "  Service Name: $SERVICE_NAME"
echo "  Region: $REGION"
echo "  Image: $IMAGE_NAME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set project
echo -e "${GREEN}Setting project...${NC}"
gcloud config set project $PROJECT_ID

# Check if APIs are enabled
echo -e "${GREEN}Checking required APIs...${NC}"
REQUIRED_APIS=(
    "run.googleapis.com"
    "cloudbuild.googleapis.com"
    "artifactregistry.googleapis.com"
)

for api in "${REQUIRED_APIS[@]}"; do
    if ! gcloud services list --enabled --filter="name:$api" --format="value(name)" | grep -q "$api"; then
        echo -e "${YELLOW}Enabling $api...${NC}"
        gcloud services enable $api
    else
        echo -e "${GREEN}✓ $api is enabled${NC}"
    fi
done

echo ""
echo -e "${GREEN}Building Docker image with Cloud Build...${NC}"
echo -e "${YELLOW}This may take 3-5 minutes...${NC}"
echo ""

# Build the Docker image using Cloud Build
gcloud builds submit \
    --config deployment/cloudbuild-adk.yaml \
    --quiet

echo ""
echo -e "${GREEN}Deploying to Cloud Run...${NC}"
echo ""

# Deploy to Cloud Run using the built image
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME:v2 \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --timeout 300 \
    --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=FALSE" \
    --quiet

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
    --region $REGION \
    --format="value(status.url)")

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${GREEN}Service URL:${NC} $SERVICE_URL"
echo ""
echo -e "${GREEN}Test endpoints:${NC}"
echo "  curl $SERVICE_URL/"
echo "  curl $SERVICE_URL/health"
echo "  curl $SERVICE_URL/tools"
echo "  curl $SERVICE_URL/agent-info"
echo ""
echo -e "${GREEN}API Documentation:${NC}"
echo "  $SERVICE_URL/docs"
echo ""

# Test the deployment
echo -e "${GREEN}Testing deployment...${NC}"
echo ""

echo -e "${YELLOW}Health check:${NC}"
curl -s $SERVICE_URL/health | python3 -m json.tool 2>/dev/null || curl -s $SERVICE_URL/health

echo ""
echo -e "${YELLOW}Agent info:${NC}"
curl -s $SERVICE_URL/agent-info | python3 -m json.tool 2>/dev/null || curl -s $SERVICE_URL/agent-info

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment successful! ✓${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Take a screenshot of the service URL and response"
echo "2. Add deployment evidence to KAGGLE_SUBMISSION.md"
echo "3. Include the service URL in your writeup"
echo ""
echo -e "${GREEN}Deployment Evidence:${NC}"
echo "  Service URL: $SERVICE_URL"
echo "  Region: $REGION"
echo "  Platform: Google Cloud Run"
echo "  Agent: backtest_orchestrator"
echo "  Model: gemini-2.0-flash"
echo "  Tools: 15"
echo ""
