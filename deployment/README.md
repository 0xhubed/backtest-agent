# Backtest Agent Deployment Guide

This directory contains all deployment configurations for Backtest Agent.

## Files

- **api.py** - FastAPI REST API application
- **Dockerfile** - Container image definition
- **cloudbuild.yaml** - Google Cloud Build configuration
- **service.yaml** - Cloud Run service specification
- **deploy.sh** - Automated deployment script

## Quick Start

### Local Development

```bash
# Run API server locally
uvicorn deployment.api:app --reload --host 0.0.0.0 --port 8000

# Test the API
curl http://localhost:8000/health
```

### Docker Local Testing

```bash
# Build image
docker build -t backtest-agent:latest -f deployment/Dockerfile .

# Run container
docker run -p 8080:8080 --env-file .env backtest-agent:latest

# Test
curl http://localhost:8080/health
```

### Google Cloud Run Deployment

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy (automated)
gcloud builds submit --config deployment/cloudbuild.yaml

# Or use manual deployment
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /backtest` - Submit backtest request
- `GET /experiments/{id}` - Get experiment by ID
- `GET /experiments/best` - Get best experiment
- `GET /experiments` - List experiments
- `GET /metrics` - Prometheus metrics

## Environment Variables

Required environment variables (set in `.env` or Cloud Run):

```env
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_REGION=us-central1
GEMINI_API_KEY=your-api-key
ENVIRONMENT=production
PORT=8080
```

## Monitoring

- **Logs**: `gcloud run services logs read backtest-agent --region us-central1`
- **Metrics**: `GET /metrics` endpoint (Prometheus format)
- **Traces**: Available in Google Cloud Trace

## Scaling Configuration

Current Cloud Run settings:
- **Min instances**: 0 (scale to zero)
- **Max instances**: 10
- **Concurrency**: 80 requests per instance
- **CPU**: 2 vCPU
- **Memory**: 2 GiB
- **Timeout**: 300 seconds

Adjust in `cloudbuild.yaml` or `service.yaml` as needed.

## Troubleshooting

### Container fails to start
- Check logs: `gcloud run services logs read backtest-agent`
- Verify environment variables are set
- Ensure data files are accessible

### API returns 500 errors
- Check application logs for stack traces
- Verify Gemini API credentials
- Ensure database is accessible

### High latency
- Increase CPU/memory allocation
- Increase max instances
- Enable Cloud CDN for static assets

## Security Best Practices

- ✅ Never commit `.env` files
- ✅ Use Secret Manager for sensitive credentials
- ✅ Enable Cloud Armor for DDoS protection
- ✅ Restrict CORS origins in production
- ✅ Use service accounts with minimal permissions
- ✅ Enable Cloud Audit Logs

## Cost Optimization

- Scale to zero when not in use (min-instances=0)
- Use CPU throttling for cost savings
- Set appropriate timeout values
- Monitor and optimize cold start times
- Use Cloud Scheduler to keep instances warm if needed
