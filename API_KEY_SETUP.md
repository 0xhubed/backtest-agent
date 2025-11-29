# 🔑 Gemini API Key Setup Guide

## What's the Issue?

You're seeing this error:
```
429 RESOURCE_EXHAUSTED
```

This means you've hit the rate limit for the free Gemini API without authentication.

---

## Solution: Get a Free Gemini API Key

### Step 1: Get Your API Key

1. **Go to Google AI Studio:**
   https://aistudio.google.com/app/apikey

2. **Sign in** with your Google account

3. **Click "Get API key"** or "Create API key"

4. **Copy the key** (starts with `AIza...`)

### Step 2: Add Key to Your Project

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file
nano .env
# Or use any text editor you prefer
```

Replace this line:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

With your actual key:
```
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXX
```

**Save and close the file.**

### Step 3: Restart the Agent

```bash
# Press Ctrl+C to stop the current server

# Restart it
source venv311/bin/activate
adk web
```

---

## Alternative: Use Vertex AI (Higher Limits)

If you need higher rate limits, use Vertex AI instead:

### 1. Set Up Google Cloud Project

```bash
# Install gcloud CLI if not installed
# Then authenticate:
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

### 2. Update .env

```env
GOOGLE_PROJECT_ID=your-actual-project-id
GOOGLE_REGION=us-central1
# Remove or comment out GEMINI_API_KEY
```

### 3. Update Agent to Use Vertex AI

Edit `backtest_agent/agent.py` line 47:

Change from:
```python
model="gemini-2.0-flash",
```

To:
```python
model="gemini-2.0-flash",
model_platform="vertex",  # Use Vertex AI instead
```

---

## Rate Limits Explained

### Free Gemini API (No Key)
- Very limited requests
- Good for quick tests only

### Gemini API (With Free Key)
- **15 requests per minute**
- **1,500 requests per day**
- **1 million tokens per day**
- Perfect for development!

### Vertex AI (Requires GCP Project)
- Much higher limits
- Pay-as-you-go pricing
- Production ready

---

## Quick Test After Setup

Once you've added your API key:

```bash
# Restart the agent
source venv311/bin/activate
adk web
```

Try this simple query:
```
What cryptocurrencies are available?
```

If it works without errors, you're all set! 🎉

---

## Troubleshooting

### Still Getting 429 Error?

1. **Check .env file exists:**
   ```bash
   ls -la .env
   ```

2. **Verify key is correct:**
   ```bash
   grep GEMINI_API_KEY .env
   ```
   (Should show your actual key, not "your-gemini-api-key-here")

3. **Restart the agent:**
   Must restart after changing .env file

### Error: "Invalid API Key"

- Double-check you copied the entire key
- Make sure there are no spaces before/after the key
- Verify the key is active in Google AI Studio

### Want to Check Your Quota?

Visit: https://aistudio.google.com/app/apikey

---

## Resources

- **Get API Key:** https://aistudio.google.com/app/apikey
- **Vertex AI Setup:** https://cloud.google.com/vertex-ai/docs/start/cloud-environment
- **ADK Rate Limit Docs:** https://google.github.io/adk-docs/agents/models/#error-code-429-resource_exhausted

---

**Once you add your API key, you'll be able to:**
- ✅ Run unlimited backtests (within daily quota)
- ✅ Test all 18 cryptocurrencies
- ✅ Compare multiple strategies
- ✅ Optimize parameters
- ✅ Get full AI-powered insights

**Get your free key now:** https://aistudio.google.com/app/apikey
