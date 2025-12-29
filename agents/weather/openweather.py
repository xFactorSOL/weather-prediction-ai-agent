"""
OpenWeatherMap API connector for weather data
Replaces PolyMarket API connector with weather-specific functionality
"""
import os
import httpx
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dotenv import load_dotenv

from agents.utils.objects import WeatherForecast, WeatherLocation, WeatherCondition

load_dotenv()
logger = logging.getLogger(__name__)


class OpenWeatherClient:
    """Client for OpenWeatherMap API"""
    
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        if not self.api_key:
            logger.warning("OPENWEATHER_API_KEY not found in environment")
    
    def get_current_weather(self, location: str, units: str = "metric") -> Dict[str, Any]:
        """Get current weather for a location"""
        url = f"{self.base_url}/weather"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": units
        }
        try:
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching current weather: {e}")
            raise
    
    def get_forecast(self, location: str, days: int = 5, units: str = "metric") -> Dict[str, Any]:
        """Get weather forecast for a location"""
        url = f"{self.base_url}/forecast"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": units,
            "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
        }
        try:
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching forecast: {e}")
            raise
    
    def get_historical_weather(
        self, 
        location: str, 
        date: datetime,
        units: str = "metric"
    ) -> Dict[str, Any]:
        """Get historical weather data (requires One Call API 3.0 subscription)"""
        # Note: Historical data requires paid subscription
        # This is a placeholder for the structure
        url = f"{self.base_url}/onecall/timemachine"
        params = {
            "lat": None,  # Would need geocoding
            "lon": None,
            "dt": int(date.timestamp()),
            "appid": self.api_key,
            "units": units
        }
        logger.warning("Historical weather requires One Call API subscription")
        return {}
    
    def geocode_location(self, location: str) -> Dict[str, Any]:
        """Get coordinates for a location name"""
        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": location,
            "limit": 1,
            "appid": self.api_key
        }
        try:
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0]
            return {}
        except Exception as e:
            logger.error(f"Error geocoding location: {e}")
            return {}
    
    def get_weather_alerts(self, location: str) -> List[Dict[str, Any]]:
        """Get weather alerts for a location"""
        # Requires One Call API 3.0
        logger.warning("Weather alerts require One Call API subscription")
        return []


class WeatherAPI:
    """Alternative weather API connector (WeatherAPI.com)"""
    
    def __init__(self) -> None:
        self.api_key = os.getenv("WEATHERAPI_KEY")
        self.base_url = "https://api.weatherapi.com/v1"
        if not self.api_key:
            logger.warning("WEATHERAPI_KEY not found in environment")
    
    def get_current_weather(self, location: str) -> Dict[str, Any]:
        """Get current weather"""
        url = f"{self.base_url}/current.json"
        params = {
            "key": self.api_key,
            "q": location
        }
        try:
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching current weather: {e}")
            raise
    
    def get_forecast(self, location: str, days: int = 7) -> Dict[str, Any]:
        """Get weather forecast"""
        url = f"{self.base_url}/forecast.json"
        params = {
            "key": self.api_key,
            "q": location,
            "days": days,
            "alerts": "yes"
        }
        try:
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching forecast: {e}")
            raise
    
    def get_historical_weather(
        self, 
        location: str, 
        date: datetime
    ) -> Dict[str, Any]:
        """Get historical weather data"""
        url = f"{self.base_url}/history.json"
        params = {
            "key": self.api_key,
            "q": location,
            "dt": date.strftime("%Y-%m-%d")
        }
        try:
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching historical weather: {e}")
            raise
    
    def get_astronomy(self, location: str, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get astronomy data (sunrise, sunset, moon phase)"""
        url = f"{self.base_url}/astronomy.json"
        params = {
            "key": self.api_key,
            "q": location
        }
        if date:
            params["dt"] = date.strftime("%Y-%m-%d")
        try:
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching astronomy data: {e}")
            raise


class WeatherDataClient:
    """Unified weather data client that can use multiple sources"""
    
    def __init__(self, primary_source: str = "openweather") -> None:
        self.openweather = OpenWeatherClient()
        self.weatherapi = WeatherAPI()
        self.primary_source = primary_source
    
    def get_current_weather(self, location: str) -> Dict[str, Any]:
        """Get current weather from primary source"""
        if self.primary_source == "openweather":
            return self.openweather.get_current_weather(location)
        else:
            return self.weatherapi.get_current_weather(location)
    
    def get_forecast(self, location: str, days: int = 7) -> Dict[str, Any]:
        """Get forecast from primary source"""
        if self.primary_source == "openweather":
            return self.openweather.get_forecast(location, days)
        else:
            return self.weatherapi.get_forecast(location, days)
    
    def get_all_forecasts(self, location: str) -> List[Dict[str, Any]]:
        """Get forecasts from all available sources for comparison"""
        forecasts = []
        try:
            ow_forecast = self.openweather.get_forecast(location)
            forecasts.append({"source": "openweather", "data": ow_forecast})
        except Exception as e:
            logger.warning(f"OpenWeather forecast failed: {e}")
        
        try:
            wa_forecast = self.weatherapi.get_forecast(location)
            forecasts.append({"source": "weatherapi", "data": wa_forecast})
        except Exception as e:
            logger.warning(f"WeatherAPI forecast failed: {e}")
        
        return forecasts
