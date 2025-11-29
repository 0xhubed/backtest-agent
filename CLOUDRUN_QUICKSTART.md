# ☁️ Cloud Run Quick Start

## 5-Minute Deployment

### 1. Install gcloud CLI (if not already)

```bash
# Ubuntu/WSL
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

### 2. Authenticate

```bash
gcloud auth login
gcloud auth application-default login
```

### 3. Deploy!

```bash
# One command to deploy everything
./deployment/deploy_cloudrun.sh YOUR_PROJECT_ID
```

**Done!** Your service will be at: `https://backtest-agent-xxx-uc.a.run.app`

---

## Quick Commands

### Deploy
```bash
./deployment/deploy_cloudrun.sh YOUR_PROJECT_ID
```

### Update
```bash
./deployment/deploy_cloudrun.sh YOUR_PROJECT_ID
```

### Test
```bash
SERVICE_URL=$(gcloud run services describe backtest-agent --region us-central1 --format="value(status.url)")
curl $SERVICE_URL/health
```

### View Logs
```bash
gcloud run services logs read backtest-agent --region us-central1
```

### Delete
```bash
gcloud run services delete backtest-agent --region us-central1
```

---

## Add API Key (After Deploy)

```bash
gcloud run services update backtest-agent \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=YOUR_KEY_HERE
```

Get free API key: https://aistudio.google.com/app/apikey

---

## Test Your Deployment

```bash
# Get your service URL
SERVICE_URL=$(gcloud run services describe backtest-agent --region us-central1 --format="value(status.url)")

# Test health
curl $SERVICE_URL/health

# Test agent info
curl $SERVICE_URL/agent-info

# Test backtest
curl -X POST $SERVICE_URL/backtest \
  -H "Content-Type: application/json" \
  -d '{"query": "What cryptocurrencies are available?"}'

# View API docs
echo "Visit: $SERVICE_URL/docs"
```

---

## Cost

**FREE** within Google Cloud free tier:
- First 2 million requests/month
- Scales to zero when not used
- No credit card required for new accounts ($300 free credit)

---

## Troubleshooting

**"gcloud: command not found"**
→ Install gcloud CLI (see step 1)

**"Permission denied"**
→ Run `gcloud auth login`

**"API not enabled"**
→ Script will auto-enable required APIs

**Service returns 500**
→ Check logs: `gcloud run services logs read backtest-agent --region us-central1`

---

## Full Guide

See [CLOUDRUN_DEPLOYMENT.md](CLOUDRUN_DEPLOYMENT.md) for complete documentation.

---

**Status:** Ready to deploy!
**Time:** 5-10 minutes
**Cost:** FREE (within limits)
