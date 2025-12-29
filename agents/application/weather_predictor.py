"""
Weather Predictor - Main orchestration class for weather prediction workflows
Replaces Trader/Creator classes with weather-specific functionality
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from agents.application.executor import Executor as Agent
from agents.weather.openweather import WeatherDataClient
from agents.utils.objects import WeatherForecast, WeatherLocation, SimpleWeatherForecast

logger = logging.getLogger(__name__)


class WeatherPredictor:
    """Main class for weather prediction workflows"""
    
    def __init__(self):
        self.weather_client = WeatherDataClient()
        self.agent = Agent()
    
    def get_best_forecast(self, location: str, question: str = "") -> str:
        """
        Get the best weather forecast for a location using all available data sources
        and AI analysis.
        
        Args:
            location: Location name (e.g., "New York, NY" or "London, UK")
            question: Optional specific question about the weather
        
        Returns:
            Comprehensive weather forecast with predictions
        """
        try:
            logger.info(f"1. FETCHING WEATHER DATA FOR {location}")
            
            # Get forecasts from multiple sources
            all_forecasts = self.weather_client.get_all_forecasts(location)
            logger.info(f"2. RETRIEVED {len(all_forecasts)} FORECAST SOURCES")
            
            # Get current weather
            current_weather = self.weather_client.get_current_weather(location)
            logger.info(f"3. RETRIEVED CURRENT WEATHER")
            
            # Generate comprehensive forecast using LLM
            if question:
                forecast = self.agent.get_weather_superforecast(
                    location=location,
                    question=question,
                    condition="weather conditions",
                    weather_data=str({"current": current_weather, "forecasts": all_forecasts})
                )
            else:
                # Use current weather and first forecast for comprehensive analysis
                forecast_data = all_forecasts[0]["data"] if all_forecasts else {}
                forecast = self.agent.generate_comprehensive_forecast(
                    location=location,
                    time_horizon="7 days"
                )
            
            logger.info(f"4. GENERATED COMPREHENSIVE FORECAST")
            return forecast
            
        except Exception as e:
            logger.error(f"Error in get_best_forecast: {e}", exc_info=True)
            logger.info("Retrying...")
            return self.get_best_forecast(location, question)
    
    def predict_weather_event(
        self, 
        location: str, 
        event_type: str,
        time_horizon: str = "3 days"
    ) -> str:
        """
        Predict a specific weather event (e.g., rain, snow, heatwave)
        
        Args:
            location: Location name
            event_type: Type of weather event to predict (e.g., "rain", "snow", "heatwave")
            time_horizon: Time period for prediction (e.g., "3 days", "1 week")
        
        Returns:
            Prediction with probability and details
        """
        try:
            logger.info(f"Predicting {event_type} for {location}")
            
            # Get weather data
            current_weather = self.weather_client.get_current_weather(location)
            forecast = self.weather_client.get_forecast(location)
            
            question = f"Will there be {event_type} in {location} within {time_horizon}?"
            
            prediction = self.agent.get_weather_superforecast(
                location=location,
                question=question,
                condition=event_type,
                weather_data=str({"current": current_weather, "forecast": forecast})
            )
            
            logger.info(f"Generated prediction for {event_type}")
            return prediction
            
        except Exception as e:
            logger.error(f"Error in predict_weather_event: {e}", exc_info=True)
            return f"Error generating prediction: {str(e)}"
    
    def analyze_location_weather(self, location: str) -> Dict[str, Any]:
        """
        Comprehensive weather analysis for a location
        
        Args:
            location: Location name
        
        Returns:
            Dictionary with current conditions, forecast, and analysis
        """
        try:
            logger.info(f"Analyzing weather for {location}")
            
            # Get all available data
            current_weather = self.weather_client.get_current_weather(location)
            forecast = self.weather_client.get_forecast(location)
            
            # Generate analysis
            analysis = self.agent.get_weather_forecast_llm(
                user_input=f"Provide a comprehensive weather analysis for {location}",
                location=location
            )
            
            return {
                "location": location,
                "current_weather": current_weather,
                "forecast": forecast,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in analyze_location_weather: {e}", exc_info=True)
            return {"error": str(e)}
    
    def compare_forecast_sources(self, location: str) -> Dict[str, Any]:
        """
        Compare forecasts from multiple sources to identify consensus and differences
        
        Args:
            location: Location name
        
        Returns:
            Comparison of forecasts from different sources
        """
        try:
            logger.info(f"Comparing forecast sources for {location}")
            
            all_forecasts = self.weather_client.get_all_forecasts(location)
            
            comparison_prompt = f"""
            Compare the following weather forecasts for {location}:
            {all_forecasts}
            
            Identify:
            1. Consensus areas (where forecasts agree)
            2. Disagreements (where forecasts differ)
            3. Confidence levels for each prediction
            4. Recommended forecast based on source reliability
            """
            
            comparison = self.agent.get_weather_llm_response(comparison_prompt)
            
            return {
                "location": location,
                "forecasts": all_forecasts,
                "comparison": comparison,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in compare_forecast_sources: {e}", exc_info=True)
            return {"error": str(e)}
    
    def get_weather_recommendations(self, location: str, activity: str = "") -> str:
        """
        Get weather-based recommendations for activities or planning
        
        Args:
            location: Location name
            activity: Optional specific activity (e.g., "outdoor wedding", "hiking")
        
        Returns:
            Recommendations based on weather forecast
        """
        try:
            forecast = self.weather_client.get_forecast(location)
            current = self.weather_client.get_current_weather(location)
            
            prompt = f"""
            Based on the following weather data for {location}:
            Current: {current}
            Forecast: {forecast}
            
            Provide recommendations for:
            {"- " + activity if activity else "- General planning and activities"}
            - Best times for outdoor activities
            - Weather-related precautions
            - Clothing recommendations
            - Travel considerations
            """
            
            recommendations = self.agent.get_weather_llm_response(prompt)
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in get_weather_recommendations: {e}", exc_info=True)
            return f"Error generating recommendations: {str(e)}"
    
    def monitor_weather_conditions(
        self, 
        locations: List[str],
        conditions: List[str]
    ) -> Dict[str, Any]:
        """
        Monitor multiple locations for specific weather conditions
        
        Args:
            locations: List of location names
            conditions: List of conditions to monitor (e.g., ["rain", "high_temperature"])
        
        Returns:
            Monitoring results for each location
        """
        results = {}
        
        for location in locations:
            try:
                current = self.weather_client.get_current_weather(location)
                forecast = self.weather_client.get_forecast(location)
                
                location_results = {}
                for condition in conditions:
                    prediction = self.predict_weather_event(
                        location=location,
                        event_type=condition,
                        time_horizon="24 hours"
                    )
                    location_results[condition] = prediction
                
                results[location] = {
                    "current": current,
                    "forecast": forecast,
                    "conditions": location_results
                }
                
            except Exception as e:
                logger.error(f"Error monitoring {location}: {e}")
                results[location] = {"error": str(e)}
        
        return results


if __name__ == "__main__":
    predictor = WeatherPredictor()
    forecast = predictor.get_best_forecast("New York, NY")
    print(forecast)
