# 🚀 Quick Start: Deploy to Render in 5 Minutes

## Step 1: Push to GitHub
```bash
git add .
git commit -m "Weather prediction agent ready for deployment"
git push origin main
```

## Step 2: Deploy on Render

1. **Go to Render**: https://dashboard.render.com
2. **Click**: "New +" → "Web Service"
3. **Connect**: Your GitHub account
4. **Select**: This repository

## Step 3: Configure

**Name**: `weather-prediction-agent`

**Settings**:
- **Environment**: Python 3
- **Build Command**: `pip install -e ".[dev]"`
- **Start Command**: `uvicorn scripts.python.server:app --host 0.0.0.0 --port $PORT`

## Step 4: Add Environment Variables

Click "Environment" tab and add:

```
OPENAI_API_KEY = sk-...
OPENWEATHER_API_KEY = your_key_here
```

(Get OpenWeatherMap key: https://openweathermap.org/api)

## Step 5: Deploy!

Click "Create Web Service" and wait ~5 minutes.

## Step 6: Test

Once deployed, visit:
- **API Docs**: `https://your-app.onrender.com/docs`
- **Health Check**: `https://your-app.onrender.com/health`
- **Test Forecast**: `https://your-app.onrender.com/api/forecast?location=New%20York,NY`

## That's it! 🎉

Your weather prediction AI agent is now live!

### Example API Calls

```bash
# Get forecast
curl "https://your-app.onrender.com/api/forecast?location=London,UK&days=7"

# Predict rain
curl "https://your-app.onrender.com/api/predict?location=Seattle,WA&condition=rain&days=3"

# Ask AI
curl -X POST "https://your-app.onrender.com/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Will it snow tomorrow?", "location": "Denver, CO"}'
```
