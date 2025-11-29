# 🚀 Deployment Options for BackTest Agent

You have 3 ways to run your BackTest Agent:

---

## Option 1: Local Development (ADK Web) ⭐ RECOMMENDED FOR TESTING

**Best for:** Local testing, development, learning

### How to Run:
```bash
./run_adk.sh
```

### Pros:
- ✅ Instant startup
- ✅ No cloud costs
- ✅ Easy debugging
- ✅ Full access to agent features
- ✅ Fast iteration

### Cons:
- ❌ Only accessible on localhost
- ❌ Doesn't work as public API
- ❌ Not production-ready

### Perfect For:
- Testing queries
- Developing strategies
- Learning how the agent works
- Rapid prototyping

**Guide:** [READY_TO_RUN.md](READY_TO_RUN.md)

---

## Option 2: Local API (FastAPI) 🔧 GOOD FOR LOCAL TESTING

**Best for:** Testing the REST API locally before cloud deployment

### How to Run:
```bash
source venv311/bin/activate
python deployment/api_adk.py
```

Then visit: http://localhost:8080/docs

### Pros:
- ✅ REST API interface
- ✅ Swagger documentation
- ✅ Same API as Cloud Run
- ✅ No cloud costs
- ✅ Easy to test

### Cons:
- ❌ Only accessible on localhost
- ❌ Not publicly available
- ❌ Requires keeping terminal open

### Perfect For:
- Testing API endpoints
- Developing integrations
- Validating before cloud deploy

**Guide:** [README.md](README.md)

---

## Option 3: Cloud Run (Production) ☁️ BEST FOR DEPLOYMENT

**Best for:** Public deployment, production use, Kaggle submission

### How to Run:
```bash
./deployment/deploy_cloudrun.sh YOUR_PROJECT_ID
```

### Pros:
- ✅ Publicly accessible URL
- ✅ Auto-scaling (0 to 1000s of instances)
- ✅ FREE tier available
- ✅ Built-in load balancing
- ✅ HTTPS by default
- ✅ Production-ready
- ✅ Perfect for Kaggle submission proof

### Cons:
- ❌ Requires Google Cloud account
- ❌ 5-10 min deployment time
- ❌ May incur costs (beyond free tier)
- ❌ Cold start latency

### Perfect For:
- **Kaggle competition submission** ⭐
- Public demo
- Production deployment
- Sharing with others
- Portfolio projects

**Guides:**
- Quick: [CLOUDRUN_QUICKSTART.md](CLOUDRUN_QUICKSTART.md)
- Full: [CLOUDRUN_DEPLOYMENT.md](CLOUDRUN_DEPLOYMENT.md)

---

## Comparison Table

| Feature | Local ADK | Local API | Cloud Run |
|---------|-----------|-----------|-----------|
| **Startup Time** | Instant | Instant | 5-10 min |
| **Cost** | FREE | FREE | FREE* |
| **Public Access** | ❌ | ❌ | ✅ |
| **HTTPS** | ❌ | ❌ | ✅ |
| **Scaling** | Single | Single | Auto |
| **For Kaggle** | ❌ | ❌ | ✅ |
| **API Docs** | ❌ | ✅ | ✅ |
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |

*Within free tier limits

---

## Recommended Workflow

### 1. Development Phase
```bash
# Start local ADK for testing
./run_adk.sh
```

Test queries:
- "What cryptocurrencies are available?"
- "Backtest SMA on BTC from 2024 to 2025"

### 2. API Testing Phase
```bash
# Test the REST API locally
source venv311/bin/activate
python deployment/api_adk.py
```

Visit: http://localhost:8080/docs

### 3. Production Deployment
```bash
# Deploy to Cloud Run for public access
./deployment/deploy_cloudrun.sh YOUR_PROJECT_ID
```

Get public URL and share!

---

## For Kaggle Submission ⭐

**IMPORTANT:** For the Kaggle competition, you need **Option 3 (Cloud Run)**

### Why?
- ✅ Provides public URL as deployment evidence
- ✅ Shows production-ready deployment
- ✅ Demonstrates cloud integration
- ✅ Easy to screenshot and document

### Steps:
1. Deploy to Cloud Run
2. Get service URL
3. Test endpoints and take screenshots:
   - `GET /health`
   - `GET /agent-info`
   - `GET /tools`
   - `POST /backtest`
4. Include in your submission

---

## Quick Decision Guide

**"I just want to test the agent"**
→ Use **Local ADK** (`./run_adk.sh`)

**"I want to test the API"**
→ Use **Local API** (`python deployment/api_adk.py`)

**"I need a public URL"**
→ Use **Cloud Run** (`./deployment/deploy_cloudrun.sh`)

**"I'm submitting to Kaggle"**
→ Use **Cloud Run** (required for deployment evidence)

**"I want to add this to my portfolio"**
→ Use **Cloud Run** (impressive + shareable)

---

## Next Steps

### For Local Testing:
1. Read [READY_TO_RUN.md](READY_TO_RUN.md)
2. Run `./run_adk.sh`
3. Try example queries from [EXAMPLE_QUERIES.md](EXAMPLE_QUERIES.md)

### For Cloud Deployment:
1. Read [CLOUDRUN_QUICKSTART.md](CLOUDRUN_QUICKSTART.md)
2. Install gcloud CLI
3. Run `./deployment/deploy_cloudrun.sh YOUR_PROJECT_ID`
4. Get your public URL!

---

**All three options are fully configured and ready to use!**

Choose the one that fits your needs. 🚀
