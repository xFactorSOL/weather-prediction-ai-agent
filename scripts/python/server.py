"""
FastAPI server for Weather Prediction AI Agent
Deployable on Render, Railway, or any cloud platform
"""
from typing import Union, Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Weather Prediction AI Agent",
    description="AI-powered weather prediction using superforecasting methodologies",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy initialization - only import and initialize when needed
_weather_predictor = None
_executor = None

def get_weather_predictor():
    """Lazy initialization of WeatherPredictor - imports only when needed"""
    global _weather_predictor
    if _weather_predictor is None:
        try:
            # Import only when needed to avoid import chain issues
            from agents.application.weather_predictor import WeatherPredictor
            _weather_predictor = WeatherPredictor()
        except Exception as e:
            logger.error(f"Failed to initialize WeatherPredictor: {e}", exc_info=True)
            raise HTTPException(
                status_code=503, 
                detail=f"Weather prediction service unavailable: {str(e)}"
            )
    return _weather_predictor

def get_executor():
    """Lazy initialization of Executor - imports only when needed"""
    global _executor
    if _executor is None:
        try:
            # Import only when needed to avoid import chain issues
            from agents.application.executor import Executor
            _executor = Executor()
        except Exception as e:
            logger.error(f"Failed to initialize Executor: {e}", exc_info=True)
            raise HTTPException(
                status_code=503, 
                detail=f"Executor service unavailable: {str(e)}"
            )
    return _executor


# Request/Response models
class ForecastRequest(BaseModel):
    location: str
    days: Optional[int] = 7


class PredictionRequest(BaseModel):
    location: str
    condition: str
    days: Optional[int] = 3


class SuperforecastRequest(BaseModel):
    location: str
    question: str
    condition: str


class RecommendationRequest(BaseModel):
    location: str
    activity: Optional[str] = ""


class WeatherQuery(BaseModel):
    question: str
    location: Optional[str] = ""


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Weather Prediction AI Agent",
        "version": "1.0.0",
        "endpoints": {
            "forecast": "/api/forecast",
            "predict": "/api/predict",
            "analyze": "/api/analyze",
            "compare": "/api/compare",
            "recommendations": "/api/recommendations",
            "superforecast": "/api/superforecast",
            "ask": "/api/ask"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/forecast")
def get_forecast(request: ForecastRequest):
    """Get comprehensive weather forecast for a location"""
    try:
        logger.info(f"Forecast request for {request.location}")
        predictor = get_weather_predictor()
        forecast = predictor.get_best_forecast(
            location=request.location
        )
        return {
            "location": request.location,
            "forecast": forecast,
            "days": request.days
        }
    except Exception as e:
        logger.error(f"Error in forecast: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/forecast")
def get_forecast_get(
    location: str = Query(..., description="Location name (e.g., 'New York, NY')"),
    days: int = Query(7, description="Number of days to forecast")
):
    """Get comprehensive weather forecast for a location (GET)"""
    try:
        logger.info(f"Forecast request for {location}")
        predictor = get_weather_predictor()
        forecast = predictor.get_best_forecast(location=location)
        return {
            "location": location,
            "forecast": forecast,
            "days": days
        }
    except Exception as e:
        logger.error(f"Error in forecast: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict")
def predict_weather(request: PredictionRequest):
    """Predict a specific weather condition"""
    try:
        logger.info(f"Prediction request: {request.condition} for {request.location}")
        predictor = get_weather_predictor()
        prediction = predictor.predict_weather_event(
            location=request.location,
            event_type=request.condition,
            time_horizon=f"{request.days} days"
        )
        return {
            "location": request.location,
            "condition": request.condition,
            "prediction": prediction,
            "time_horizon": f"{request.days} days"
        }
    except Exception as e:
        logger.error(f"Error in prediction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/predict")
def predict_weather_get(
    location: str = Query(..., description="Location name"),
    condition: str = Query(..., description="Weather condition (e.g., 'rain', 'snow')"),
    days: int = Query(3, description="Time horizon in days")
):
    """Predict a specific weather condition (GET)"""
    try:
        logger.info(f"Prediction request: {condition} for {location}")
        predictor = get_weather_predictor()
        prediction = predictor.predict_weather_event(
            location=location,
            event_type=condition,
            time_horizon=f"{days} days"
        )
        return {
            "location": location,
            "condition": condition,
            "prediction": prediction,
            "time_horizon": f"{days} days"
        }
    except Exception as e:
        logger.error(f"Error in prediction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analyze")
def analyze_location(
    location: str = Query(..., description="Location name")
):
    """Comprehensive weather analysis for a location"""
    try:
        logger.info(f"Analysis request for {location}")
        predictor = get_weather_predictor()
        analysis = predictor.analyze_location_weather(location)
        return analysis
    except Exception as e:
        logger.error(f"Error in analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/compare")
def compare_forecasts(
    location: str = Query(..., description="Location name")
):
    """Compare forecasts from multiple weather sources"""
    try:
        logger.info(f"Comparison request for {location}")
        predictor = get_weather_predictor()
        comparison = predictor.compare_forecast_sources(location)
        return comparison
    except Exception as e:
        logger.error(f"Error in comparison: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recommendations")
def get_recommendations(request: RecommendationRequest):
    """Get weather-based recommendations"""
    try:
        logger.info(f"Recommendations request for {request.location}")
        predictor = get_weather_predictor()
        recommendations = predictor.get_weather_recommendations(
            location=request.location,
            activity=request.activity
        )
        return {
            "location": request.location,
            "activity": request.activity,
            "recommendations": recommendations
        }
    except Exception as e:
        logger.error(f"Error in recommendations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recommendations")
def get_recommendations_get(
    location: str = Query(..., description="Location name"),
    activity: str = Query("", description="Specific activity (optional)")
):
    """Get weather-based recommendations (GET)"""
    try:
        logger.info(f"Recommendations request for {location}")
        predictor = get_weather_predictor()
        recommendations = predictor.get_weather_recommendations(
            location=location,
            activity=activity
        )
        return {
            "location": location,
            "activity": activity,
            "recommendations": recommendations
        }
    except Exception as e:
        logger.error(f"Error in recommendations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/superforecast")
def get_superforecast(request: SuperforecastRequest):
    """Get superforecaster prediction for a specific weather condition"""
    try:
        logger.info(f"Superforecast request: {request.question} for {request.location}")
        exec = get_executor()
        prediction = exec.get_weather_superforecast(
            location=request.location,
            question=request.question,
            condition=request.condition
        )
        return {
            "location": request.location,
            "question": request.question,
            "condition": request.condition,
            "prediction": prediction
        }
    except Exception as e:
        logger.error(f"Error in superforecast: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ask")
def ask_weather_ai(request: WeatherQuery):
    """Ask the weather AI any weather-related question"""
    try:
        logger.info(f"Weather AI query: {request.question}")
        exec = get_executor()
        if request.location:
            response = exec.get_weather_forecast_llm(
                user_input=request.question,
                location=request.location
            )
        else:
            response = exec.get_weather_llm_response(request.question)
        return {
            "question": request.question,
            "location": request.location,
            "response": response
        }
    except Exception as e:
        logger.error(f"Error in weather AI query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ask")
def ask_weather_ai_get(
    question: str = Query(..., description="Weather-related question"),
    location: str = Query("", description="Location (optional)")
):
    """Ask the weather AI any weather-related question (GET)"""
    try:
        logger.info(f"Weather AI query: {question}")
        exec = get_executor()
        if location:
            response = exec.get_weather_forecast_llm(
                user_input=question,
                location=location
            )
        else:
            response = exec.get_weather_llm_response(question)
        return {
            "question": question,
            "location": location,
            "response": response
        }
    except Exception as e:
        logger.error(f"Error in weather AI query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
