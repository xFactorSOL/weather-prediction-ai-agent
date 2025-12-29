# Deployment Guide for Weather Prediction AI Agent

## Deploying to Render

### Prerequisites
1. GitHub account with this repository
2. Render account (sign up at [render.com](https://render.com))
3. API keys ready:
   - OpenAI API key
   - OpenWeatherMap API key (or WeatherAPI key)

### Step-by-Step Deployment

#### Option 1: Using Render Dashboard (Recommended)

1. **Connect Repository**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select this repository

2. **Configure Service**
   - **Name**: `weather-prediction-agent` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -e ".[dev]"`
   - **Start Command**: `uvicorn scripts.python.server:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Choose Starter (free) or Standard/Pro for production

3. **Set Environment Variables**
   In the Render dashboard, add these environment variables:
   ```
   OPENAI_API_KEY=your_openai_key_here
   OPENWEATHER_API_KEY=your_openweather_key_here
   WEATHERAPI_KEY=your_weatherapi_key_here (optional)
   NEWSAPI_API_KEY=your_newsapi_key_here (optional)
   TAVILY_API_KEY=your_tavily_key_here (optional)
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy
   - Wait for deployment to complete (usually 5-10 minutes)

#### Option 2: Using render.yaml (Auto-deploy)

If you've committed `render.yaml` to your repository:

1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically detect `render.yaml` and configure the service
5. Add environment variables in the dashboard
6. Deploy!

### Post-Deployment

1. **Test the API**
   ```bash
   curl https://your-service-name.onrender.com/health
   ```

2. **Test Weather Forecast**
   ```bash
   curl "https://your-service-name.onrender.com/api/forecast?location=New%20York,NY&days=7"
   ```

3. **View API Documentation**
   Visit: `https://your-service-name.onrender.com/docs`
   - Interactive Swagger UI
   - Full API documentation

### API Endpoints

Once deployed, your service will have these endpoints:

- `GET /` - Health check and API info
- `GET /health` - Health check
- `GET /api/forecast?location=<location>&days=<days>` - Get forecast
- `GET /api/predict?location=<location>&condition=<condition>&days=<days>` - Predict weather
- `GET /api/analyze?location=<location>` - Analyze location
- `GET /api/compare?location=<location>` - Compare forecast sources
- `GET /api/recommendations?location=<location>&activity=<activity>` - Get recommendations
- `POST /api/superforecast` - Superforecaster prediction
- `POST /api/ask` - Ask weather AI

All endpoints also support POST with JSON body.

### Environment Variables

Required:
- `OPENAI_API_KEY` - For LLM predictions
- `OPENWEATHER_API_KEY` - For weather data (or use WEATHERAPI_KEY)

Optional:
- `WEATHERAPI_KEY` - Alternative weather data source
- `NEWSAPI_API_KEY` - For weather news
- `TAVILY_API_KEY` - For web search

### Troubleshooting

1. **Build Fails**
   - Check build logs in Render dashboard
   - Ensure all dependencies are in `pyproject.toml`
   - Verify Python version (3.12+)

2. **Service Crashes**
   - Check logs in Render dashboard
   - Verify all environment variables are set
   - Ensure API keys are valid

3. **Slow Responses**
   - Weather API calls can take time
   - Consider upgrading to Standard/Pro plan for better performance
   - Add caching for frequently requested locations

### Monitoring

- View logs in Render dashboard
- Set up alerts for service health
- Monitor API usage and costs

### Cost Considerations

- **Starter Plan (Free)**: 
  - 750 hours/month
  - Service spins down after 15 minutes of inactivity
  - Good for testing and development

- **Standard/Pro Plans**:
  - Always-on service
  - Better performance
  - Recommended for production

### Custom Domain

1. Go to your service settings in Render
2. Click "Custom Domains"
3. Add your domain
4. Follow DNS configuration instructions

## Alternative Deployments

### Railway

1. Connect GitHub repository
2. Railway auto-detects Python
3. Set environment variables
4. Deploy!

### Heroku

1. Install Heroku CLI
2. `heroku create your-app-name`
3. `git push heroku main`
4. Set environment variables: `heroku config:set OPENAI_API_KEY=...`

### Docker

Build and run locally:
```bash
docker build -t weather-agent .
docker run -p 8000:8000 -e OPENAI_API_KEY=... weather-agent
```

## Support

For issues or questions:
- Check Render logs
- Review API documentation at `/docs`
- Open an issue on GitHub
