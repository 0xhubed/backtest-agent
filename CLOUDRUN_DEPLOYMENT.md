# ☁️ Cloud Run Deployment Guide

Deploy your BackTest Agent to Google Cloud Run in minutes!

## 📋 Prerequisites

### 1. Google Cloud Account
- Sign up at: https://cloud.google.com/
- New accounts get $300 free credit

### 2. Install Google Cloud SDK

**On Ubuntu/WSL:**
```bash
# Add Cloud SDK repo
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Install
sudo apt-get update && sudo apt-get install google-cloud-cli
```

**Verify installation:**
```bash
gcloud --version
```

### 3. Authenticate

```bash
# Login to Google Cloud
gcloud auth login

# Set up application default credentials
gcloud auth application-default login
```

---

## 🚀 Quick Deploy (1-Command)

```bash
# Run the automated deployment script
./deployment/deploy_cloudrun.sh YOUR_PROJECT_ID
```

**That's it!** The script will:
1. ✅ Enable required APIs
2. ✅ Build Docker image
3. ✅ Deploy to Cloud Run
4. ✅ Test the deployment
5. ✅ Show you the service URL

---

## 📝 Step-by-Step Manual Deployment

### Step 1: Create/Select a Project

```bash
# Create new project (or use existing)
gcloud projects create backtest-agent-123 --name="BackTest Agent"

# Set as active project
gcloud config set project backtest-agent-123
```

### Step 2: Enable Required APIs

```bash
# Enable Cloud Run
gcloud services enable run.googleapis.com

# Enable Cloud Build
gcloud services enable cloudbuild.googleapis.com

# Enable Artifact Registry
gcloud services enable artifactregistry.googleapis.com
```

### Step 3: Build and Deploy

**Option A: Using the deploy script (recommended)**
```bash
./deployment/deploy_cloudrun.sh backtest-agent-123
```

**Option B: Using gcloud directly**
```bash
gcloud run deploy backtest-agent \
  --source . \
  --dockerfile deployment/Dockerfile.adk \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300
```

**Option C: Using Cloud Build**
```bash
gcloud builds submit --config deployment/cloudbuild-adk.yaml
```

### Step 4: Get Your Service URL

```bash
gcloud run services describe backtest-agent \
  --region us-central1 \
  --format="value(status.url)"
```

---

## 🧪 Test Your Deployment

```bash
# Set your service URL
SERVICE_URL="https://backtest-agent-xxx-uc.a.run.app"

# Test health endpoint
curl $SERVICE_URL/health

# Get agent info
curl $SERVICE_URL/agent-info

# List available tools
curl $SERVICE_URL/tools

# Run a backtest
curl -X POST $SERVICE_URL/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What cryptocurrencies are available?"
  }'
```

---

## 🔑 Setting Up Gemini API Key

For the agent to work fully, you need to set the Gemini API key as an environment variable:

### Get Your API Key
1. Visit: https://aistudio.google.com/app/apikey
2. Create an API key
3. Copy it

### Add to Cloud Run

```bash
gcloud run services update backtest-agent \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=YOUR_API_KEY_HERE
```

Or update via Cloud Console:
1. Go to Cloud Run in Google Cloud Console
2. Click on `backtest-agent` service
3. Click "Edit & Deploy New Revision"
4. Under "Variables & Secrets" → "Environment Variables"
5. Add: `GEMINI_API_KEY` = `your-api-key`
6. Click "Deploy"

---

## 📊 Available API Endpoints

Once deployed, your service will have:

### GET /
Service information
```bash
curl https://your-service-url.run.app/
```

### GET /health
Health check
```bash
curl https://your-service-url.run.app/health
```

### GET /tools
List all 15 agent tools
```bash
curl https://your-service-url.run.app/tools
```

### GET /agent-info
Detailed agent configuration
```bash
curl https://your-service-url.run.app/agent-info
```

### POST /backtest
Submit a backtesting query
```bash
curl -X POST https://your-service-url.run.app/backtest \
  -H "Content-Type: application/json" \
  -d '{"query": "Backtest SMA on BTC from 2024 to 2025"}'
```

### GET /docs
Interactive API documentation (Swagger UI)
```
https://your-service-url.run.app/docs
```

---

## 💰 Cost Estimate

Cloud Run pricing (as of 2025):

**Free Tier (per month):**
- 2 million requests
- 360,000 vCPU-seconds
- 180,000 GiB-seconds of memory

**Our Configuration:**
- Memory: 1 GiB
- CPU: 1 vCPU
- Timeout: 300 seconds

**Estimated Cost:**
- **Light usage** (100 requests/day): **FREE**
- **Medium usage** (1,000 requests/day): **~$5-10/month**
- **Heavy usage** (10,000 requests/day): **~$30-50/month**

**Tips to minimize costs:**
- Set `--min-instances 0` (scale to zero when not in use)
- Use `--max-instances 10` (prevent runaway costs)
- Set appropriate `--timeout` values

---

## 🔧 Configuration Options

### Scale to Zero (Save $$$)
```bash
gcloud run services update backtest-agent \
  --region us-central1 \
  --min-instances 0
```

### Increase Resources
```bash
gcloud run services update backtest-agent \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2
```

### Add Custom Domain
```bash
gcloud run domain-mappings create \
  --service backtest-agent \
  --domain backtest.yourdomain.com \
  --region us-central1
```

### Enable Authentication
```bash
gcloud run services update backtest-agent \
  --region us-central1 \
  --no-allow-unauthenticated
```

---

## 📈 Monitoring

### View Logs
```bash
gcloud run services logs read backtest-agent \
  --region us-central1 \
  --limit 50
```

### Monitor Metrics
1. Go to Cloud Console: https://console.cloud.google.com/run
2. Click on `backtest-agent` service
3. Click "Metrics" tab

You'll see:
- Request count
- Request latency
- Container instance count
- Memory & CPU utilization

---

## 🐛 Troubleshooting

### Deployment Failed

**Check build logs:**
```bash
gcloud builds list --limit 5
gcloud builds log BUILD_ID
```

**Common issues:**
- API not enabled → Run `gcloud services enable run.googleapis.com`
- Insufficient permissions → Make sure you're project owner/editor
- Dockerfile errors → Test locally first with `docker build`

### Service Returns 500 Error

**Check service logs:**
```bash
gcloud run services logs read backtest-agent --region us-central1
```

**Common causes:**
- Missing environment variables
- Data files not copied in Docker image
- Import errors in Python code

### Cold Start Slow

**Solutions:**
- Set minimum instances: `--min-instances 1`
- Optimize Docker image size
- Use Cloud CDN for static assets

---

## 🔄 Update Deployment

To deploy updates:

```bash
# Quick update using deploy script
./deployment/deploy_cloudrun.sh YOUR_PROJECT_ID

# Or manually
gcloud run deploy backtest-agent \
  --source . \
  --dockerfile deployment/Dockerfile.adk \
  --region us-central1
```

---

## 🗑️ Delete Deployment

To remove the service and save costs:

```bash
# Delete Cloud Run service
gcloud run services delete backtest-agent --region us-central1

# Delete Docker images (optional)
gcloud container images delete gcr.io/YOUR_PROJECT_ID/backtest-agent
```

---

## 📸 Deployment Evidence (For Kaggle Submission)

After deployment, capture:

1. **Service URL**
   ```bash
   gcloud run services describe backtest-agent \
     --region us-central1 \
     --format="value(status.url)"
   ```

2. **Test Output**
   ```bash
   curl YOUR_SERVICE_URL/agent-info | python -m json.tool
   ```

3. **Screenshots:**
   - Cloud Run service dashboard
   - API documentation (/docs)
   - Successful health check
   - Sample backtest response

---

## 📚 Resources

- **Cloud Run Docs:** https://cloud.google.com/run/docs
- **Cloud Build Docs:** https://cloud.google.com/build/docs
- **Pricing Calculator:** https://cloud.google.com/products/calculator
- **Free Tier:** https://cloud.google.com/free

---

## ✅ Deployment Checklist

- [ ] Google Cloud account created
- [ ] gcloud CLI installed
- [ ] Authenticated with `gcloud auth login`
- [ ] Project created and set
- [ ] Required APIs enabled
- [ ] Code updated with correct dataset
- [ ] Gemini API key obtained
- [ ] Deployment script run successfully
- [ ] Service URL obtained
- [ ] Health check passed
- [ ] API key set as environment variable
- [ ] Test queries working
- [ ] Screenshots taken
- [ ] Deployment evidence documented

---

**Next Steps:**
1. Run: `./deployment/deploy_cloudrun.sh YOUR_PROJECT_ID`
2. Get your service URL
3. Test with: `curl YOUR_URL/health`
4. Add Gemini API key
5. Start using your deployed agent!

**Estimated Time:** 5-10 minutes
**Cost:** FREE (within free tier limits)
