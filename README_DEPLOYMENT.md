# 🚀 Deployment Ready: Weather Prediction AI Agent

Your weather prediction agent is **ready to deploy to Render**!

## ✅ What's Been Set Up

1. **FastAPI Server** (`scripts/python/server.py`)
   - Full REST API with weather endpoints
   - Interactive API docs at `/docs`
   - Health check at `/health`

2. **Render Configuration** (`render.yaml`)
   - Auto-detects and configures service
   - Environment variables template
   - Health check path configured

3. **Docker Support** (`Dockerfile`)
   - Updated to run FastAPI server
   - Ready for containerized deployment

4. **Deployment Files**
   - `Procfile` - For Heroku/Railway compatibility
   - `.renderignore` - Excludes unnecessary files
   - `DEPLOY.md` - Full deployment guide
   - `RENDER_QUICKSTART.md` - 5-minute quick start

## 🎯 Quick Deploy Steps

### Option A: Render Dashboard (Easiest)

1. Push to GitHub:
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push
   ```

2. Go to https://dashboard.render.com
3. New → Web Service → Connect GitHub repo
4. Use these settings:
   - **Build**: `pip install -e ".[dev]"`
   - **Start**: `uvicorn scripts.python.server:app --host 0.0.0.0 --port $PORT`
5. Add env vars: `OPENAI_API_KEY` and `OPENWEATHER_API_KEY`
6. Deploy!

### Option B: Auto-deploy with render.yaml

1. Push `render.yaml` to GitHub
2. Render Dashboard → New → Blueprint
3. Connect repo (auto-detects render.yaml)
4. Add environment variables
5. Deploy!

## 📡 API Endpoints

Once deployed, your API will have:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info & health |
| `/health` | GET | Health check |
| `/api/forecast` | GET/POST | Get weather forecast |
| `/api/predict` | GET/POST | Predict specific condition |
| `/api/analyze` | GET | Analyze location weather |
| `/api/compare` | GET | Compare forecast sources |
| `/api/recommendations` | GET/POST | Get recommendations |
| `/api/superforecast` | POST | Superforecaster prediction |
| `/api/ask` | GET/POST | Ask weather AI |
| `/docs` | GET | Interactive API docs |

## 🔑 Required Environment Variables

**Minimum Required**:
- `OPENAI_API_KEY` - For AI predictions
- `OPENWEATHER_API_KEY` - For weather data

**Optional**:
- `WEATHERAPI_KEY` - Alternative weather source
- `NEWSAPI_API_KEY` - Weather news
- `TAVILY_API_KEY` - Web search

## 🧪 Test Locally First

```bash
# Install dependencies
pip install -e ".[dev]"

# Set environment variables
export OPENAI_API_KEY="your_key"
export OPENWEATHER_API_KEY="your_key"

# Run server
uvicorn scripts.python.server:app --reload

# Test
curl http://localhost:8000/health
curl "http://localhost:8000/api/forecast?location=New%20York,NY"
```

## 📊 Example API Calls

### Get Forecast
```bash
curl "https://your-app.onrender.com/api/forecast?location=London,UK&days=7"
```

### Predict Rain
```bash
curl "https://your-app.onrender.com/api/predict?location=Seattle,WA&condition=rain&days=3"
```

### Ask AI
```bash
curl -X POST "https://your-app.onrender.com/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Will it snow tomorrow?", "location": "Denver, CO"}'
```

### Superforecast
```bash
curl -X POST "https://your-app.onrender.com/api/superforecast" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Miami, FL",
    "question": "Will there be a hurricane this week?",
    "condition": "hurricane"
  }'
```

## 🎨 Interactive API Documentation

Once deployed, visit:
- **Swagger UI**: `https://your-app.onrender.com/docs`
- **ReDoc**: `https://your-app.onrender.com/redoc`

## 💰 Render Pricing

- **Starter (Free)**: 750 hours/month, spins down after 15min inactivity
- **Standard ($7/mo)**: Always on, better performance
- **Pro ($25/mo)**: Production-ready with auto-scaling

## 🐛 Troubleshooting

**Build fails?**
- Check logs in Render dashboard
- Verify Python 3.12+ compatibility
- Ensure all dependencies in `pyproject.toml`

**Service crashes?**
- Check environment variables are set
- Verify API keys are valid
- Review logs for error messages

**Slow responses?**
- Weather APIs can be slow
- Consider caching for frequent locations
- Upgrade to Standard/Pro plan

## 📚 Documentation

- **Full Guide**: See `DEPLOY.md`
- **Quick Start**: See `RENDER_QUICKSTART.md`
- **API Docs**: Visit `/docs` after deployment

## 🎉 You're Ready!

Everything is configured. Just push to GitHub and deploy on Render!

```bash
git add .
git commit -m "Weather prediction agent - ready for Render"
git push origin main
```

Then follow the steps above to deploy! 🚀
