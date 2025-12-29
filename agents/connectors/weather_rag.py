"""
Weather RAG connector for storing and querying historical weather data and patterns
Adapted from PolymarketRAG for weather-specific use cases
"""
import json
import os
import time
from typing import List, Dict, Any, Optional

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores.chroma import Chroma

from agents.utils.objects import WeatherForecast, WeatherLocation, SimpleWeatherForecast
from agents.weather.openweather import WeatherDataClient


class WeatherRAG:
    """RAG system for weather data and forecasts"""
    
    def __init__(self, local_db_directory: Optional[str] = None, embedding_function=None) -> None:
        self.weather_client = WeatherDataClient()
        self.local_db_directory = local_db_directory
        self.embedding_function = embedding_function
    
    def load_weather_json_from_local(
        self, 
        json_file_path: Optional[str] = None, 
        vector_db_directory: str = "./local_db_weather"
    ) -> None:
        """Load weather data from local JSON file into vector database"""
        loader = JSONLoader(
            file_path=json_file_path, 
            jq_schema=".[].description", 
            text_content=False
        )
        loaded_docs = loader.load()
        
        embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        Chroma.from_documents(
            loaded_docs, 
            embedding_function, 
            persist_directory=vector_db_directory
        )
    
    def create_local_weather_rag(
        self, 
        locations: List[str],
        local_directory: str = "./local_db_weather"
    ) -> None:
        """Create local RAG database from weather forecasts for multiple locations"""
        all_forecasts = []
        
        for location in locations:
            try:
                forecast = self.weather_client.get_forecast(location)
                current = self.weather_client.get_current_weather(location)
                
                forecast_data = {
                    "location": location,
                    "current": current,
                    "forecast": forecast,
                    "timestamp": time.time()
                }
                all_forecasts.append(forecast_data)
            except Exception as e:
                print(f"Error fetching weather for {location}: {e}")
                continue
        
        if not os.path.isdir(local_directory):
            os.mkdir(local_directory)
        
        local_file_path = f"{local_directory}/weather_forecasts_{time.time()}.json"
        
        with open(local_file_path, "w+") as output_file:
            json.dump(all_forecasts, output_file)
        
        self.load_weather_json_from_local(
            json_file_path=local_file_path, 
            vector_db_directory=local_directory
        )
    
    def query_local_weather_rag(
        self, 
        local_directory: Optional[str] = None, 
        query: Optional[str] = None
    ) -> List[tuple]:
        """Query local weather RAG database"""
        if not local_directory:
            local_directory = "./local_db_weather"
        
        embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        local_db = Chroma(
            persist_directory=local_directory, 
            embedding_function=embedding_function
        )
        response_docs = local_db.similarity_search_with_score(query=query)
        return response_docs
    
    def weather_forecasts(
        self, 
        forecasts: List[SimpleWeatherForecast], 
        prompt: str
    ) -> List[tuple]:
        """Create vector database from weather forecasts and query it"""
        local_forecasts_directory: str = "./local_db_weather_forecasts"
        if not os.path.isdir(local_forecasts_directory):
            os.mkdir(local_forecasts_directory)
        
        local_file_path = f"{local_forecasts_directory}/forecasts.json"
        dict_forecasts = [x.dict() if hasattr(x, 'dict') else x for x in forecasts]
        
        with open(local_file_path, "w+") as output_file:
            json.dump(dict_forecasts, output_file)
        
        # Create vector db
        def metadata_func(record: dict, metadata: dict) -> dict:
            metadata["id"] = record.get("id")
            metadata["location_name"] = record.get("location_name")
            metadata["forecast_date"] = record.get("forecast_date")
            metadata["confidence"] = record.get("confidence")
            metadata["source"] = record.get("source")
            return metadata
        
        loader = JSONLoader(
            file_path=local_file_path,
            jq_schema=".[]",
            content_key="description",
            text_content=False,
            metadata_func=metadata_func,
        )
        loaded_docs = loader.load()
        embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        vector_db_directory = f"{local_forecasts_directory}/chroma"
        local_db = Chroma.from_documents(
            loaded_docs, 
            embedding_function, 
            persist_directory=vector_db_directory
        )
        
        # Query
        return local_db.similarity_search_with_score(query=prompt)
    
    def weather_locations(
        self, 
        locations: List[WeatherLocation], 
        prompt: str
    ) -> List[tuple]:
        """Create vector database from weather locations and query it"""
        local_locations_directory: str = "./local_db_weather_locations"
        if not os.path.isdir(local_locations_directory):
            os.mkdir(local_locations_directory)
        
        local_file_path = f"{local_locations_directory}/locations.json"
        dict_locations = [x.dict() if hasattr(x, 'dict') else x for x in locations]
        
        with open(local_file_path, "w+") as output_file:
            json.dump(dict_locations, output_file)
        
        # Create vector db
        def metadata_func(record: dict, metadata: dict) -> dict:
            metadata["name"] = record.get("name")
            metadata["country"] = record.get("country")
            metadata["state"] = record.get("state")
            metadata["latitude"] = record.get("latitude")
            metadata["longitude"] = record.get("longitude")
            return metadata
        
        loader = JSONLoader(
            file_path=local_file_path,
            jq_schema=".[]",
            content_key="name",
            text_content=False,
            metadata_func=metadata_func,
        )
        loaded_docs = loader.load()
        embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        vector_db_directory = f"{local_locations_directory}/chroma"
        local_db = Chroma.from_documents(
            loaded_docs, 
            embedding_function, 
            persist_directory=vector_db_directory
        )
        
        # Query
        return local_db.similarity_search_with_score(query=prompt)
    
    def store_historical_pattern(
        self,
        location: str,
        pattern_data: Dict[str, Any],
        local_directory: str = "./local_db_weather_patterns"
    ) -> None:
        """Store historical weather patterns for analysis"""
        if not os.path.isdir(local_directory):
            os.mkdir(local_directory)
        
        pattern_data["location"] = location
        pattern_data["timestamp"] = time.time()
        
        local_file_path = f"{local_directory}/pattern_{location}_{time.time()}.json"
        
        with open(local_file_path, "w+") as output_file:
            json.dump(pattern_data, output_file)
        
        # Add to vector database
        loader = JSONLoader(
            file_path=local_file_path,
            jq_schema=".",
            text_content=False
        )
        loaded_docs = loader.load()
        embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Check if vector DB exists, if not create it
        vector_db_path = f"{local_directory}/chroma"
        if os.path.exists(vector_db_path):
            local_db = Chroma(
                persist_directory=vector_db_path,
                embedding_function=embedding_function
            )
            # Add new documents
            local_db.add_documents(loaded_docs)
        else:
            Chroma.from_documents(
                loaded_docs,
                embedding_function,
                persist_directory=vector_db_path
            )
