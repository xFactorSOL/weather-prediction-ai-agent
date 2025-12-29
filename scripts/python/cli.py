import logging
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.pretty import pprint

from agents.polymarket.polymarket import Polymarket
from agents.connectors.chroma import PolymarketRAG
from agents.connectors.news import News
from agents.application.trade import Trader
from agents.application.executor import Executor
from agents.application.creator import Creator
from agents.application.weather_predictor import WeatherPredictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = typer.Typer(help="Weather Prediction AI Agent CLI")
console = Console()

# Initialize clients lazily to avoid import-time errors
_polymarket: Optional[Polymarket] = None
_newsapi_client: Optional[News] = None
_polymarket_rag: Optional[PolymarketRAG] = None


def get_polymarket() -> Polymarket:
    global _polymarket
    if _polymarket is None:
        _polymarket = Polymarket()
    return _polymarket


def get_news() -> News:
    global _newsapi_client
    if _newsapi_client is None:
        _newsapi_client = News()
    return _newsapi_client


def get_rag() -> PolymarketRAG:
    global _polymarket_rag
    if _polymarket_rag is None:
        _polymarket_rag = PolymarketRAG()
    return _polymarket_rag
@app.command()
def get_all_markets(limit: int = 5, sort_by: str = "spread") -> None:
    """
    Query Polymarket's markets
    """
    console.print(f"[cyan]Fetching {limit} markets, sorted by {sort_by}[/cyan]")
    pm = get_polymarket()
    markets = pm.get_all_markets()
    markets = pm.filter_markets_for_trading(markets)
    if sort_by == "spread":
        markets = sorted(markets, key=lambda x: x.spread, reverse=True)
    markets = markets[:limit]
    console.print("[green]Markets:[/green]")
    pprint(markets)


@app.command()
def get_trending_markets(limit: int = 10) -> None:
    """
    Get trending markets sorted by 24-hour volume
    """
    console.print(f"[cyan]Fetching {limit} trending markets (sorted by 24h volume)[/cyan]")
    pm = get_polymarket()
    markets = pm.get_trending_markets(limit=limit)
    console.print(f"[green]Found {len(markets)} trending markets:[/green]")
    pprint(markets)


@app.command()
def get_relevant_news(keywords: str) -> None:
    """
    Use NewsAPI to query the internet
    """
    console.print(f"[cyan]Fetching news for keywords: {keywords}[/cyan]")
    news = get_news()
    articles = news.get_articles_for_cli_keywords(keywords)
    console.print(f"[green]Found {len(articles)} articles:[/green]")
    pprint(articles)


@app.command()
def get_all_events(limit: int = 5, sort_by: str = "number_of_markets") -> None:
    """
    Query Polymarket's events
    """
    console.print(f"[cyan]Fetching {limit} events, sorted by {sort_by}[/cyan]")
    pm = get_polymarket()
    events = pm.get_all_events()
    events = pm.filter_events_for_trading(events)
    if sort_by == "number_of_markets":
        events = sorted(events, key=lambda x: len(x.markets.split(",")), reverse=True)
    events = events[:limit]
    console.print(f"[green]Found {len(events)} events:[/green]")
    pprint(events)


@app.command()
def create_local_markets_rag(local_directory: str) -> None:
    """
    Create a local markets database for RAG
    """
    console.print(f"[cyan]Creating local RAG database in {local_directory}[/cyan]")
    rag = get_rag()
    rag.create_local_markets_rag(local_directory=local_directory)
    console.print("[green]RAG database created successfully![/green]")


@app.command()
def query_local_markets_rag(vector_db_directory: str, query: str) -> None:
    """
    RAG over a local database of Polymarket's events
    """
    console.print(f"[cyan]Querying RAG database: {query}[/cyan]")
    rag = get_rag()
    response = rag.query_local_markets_rag(
        local_directory=vector_db_directory, query=query
    )
    console.print("[green]RAG Results:[/green]")
    pprint(response)


@app.command()
def ask_superforecaster(event_title: str, market_question: str, outcome: str) -> None:
    """
    Ask a superforecaster about a trade
    """
    console.print(f"[cyan]Event: {event_title}[/cyan]")
    console.print(f"[cyan]Question: {market_question}[/cyan]")
    console.print(f"[cyan]Outcome: {outcome}[/cyan]")
    executor = Executor()
    response = executor.get_superforecast(
        event_title=event_title, market_question=market_question, outcome=outcome
    )
    console.print("[green]Superforecaster Response:[/green]")
    console.print(response)


@app.command()
def create_market() -> None:
    """
    Format a request to create a market on Polymarket
    """
    console.print("[cyan]Generating market idea...[/cyan]")
    c = Creator()
    market_description = c.one_best_market()
    console.print("[green]Market Description:[/green]")
    console.print(market_description)


@app.command()
def ask_llm(user_input: str) -> None:
    """
    Ask a question to the LLM and get a response.
    """
    console.print(f"[cyan]Querying LLM: {user_input}[/cyan]")
    executor = Executor()
    response = executor.get_llm_response(user_input)
    console.print("[green]LLM Response:[/green]")
    console.print(response)


@app.command()
def ask_polymarket_llm(user_input: str) -> None:
    """
    What types of markets do you want trade?
    """
    console.print(f"[cyan]Querying Polymarket LLM: {user_input}[/cyan]")
    executor = Executor()
    response = executor.get_polymarket_llm(user_input=user_input)
    console.print("[green]LLM + current markets&events response:[/green]")
    console.print(response)


@app.command()
def run_autonomous_trader() -> None:
    """
    Let an autonomous system trade for you.
    """
    console.print("[yellow]⚠️  Starting autonomous trader...[/yellow]")
    console.print("[yellow]⚠️  Please review Terms of Service: https://polymarket.com/tos[/yellow]")
    trader = Trader()
    trader.one_best_trade()
    console.print("[green]Autonomous trading completed![/green]")


# Weather-specific commands
@app.command()
def get_forecast(location: str, days: int = 7) -> None:
    """
    Get weather forecast for a location
    """
    console.print(f"[cyan]Fetching {days}-day forecast for {location}...[/cyan]")
    predictor = WeatherPredictor()
    forecast = predictor.get_best_forecast(location)
    console.print("[green]Weather Forecast:[/green]")
    console.print(forecast)


@app.command()
def predict_weather(location: str, condition: str, days: int = 3) -> None:
    """
    Predict a specific weather condition (e.g., rain, snow, heatwave)
    """
    console.print(f"[cyan]Predicting {condition} for {location}...[/cyan]")
    predictor = WeatherPredictor()
    prediction = predictor.predict_weather_event(
        location=location,
        event_type=condition,
        time_horizon=f"{days} days"
    )
    console.print("[green]Weather Prediction:[/green]")
    console.print(prediction)


@app.command()
def analyze_location(location: str) -> None:
    """
    Comprehensive weather analysis for a location
    """
    console.print(f"[cyan]Analyzing weather for {location}...[/cyan]")
    predictor = WeatherPredictor()
    analysis = predictor.analyze_location_weather(location)
    console.print("[green]Weather Analysis:[/green]")
    pprint(analysis)


@app.command()
def compare_forecasts(location: str) -> None:
    """
    Compare forecasts from multiple weather sources
    """
    console.print(f"[cyan]Comparing forecast sources for {location}...[/cyan]")
    predictor = WeatherPredictor()
    comparison = predictor.compare_forecast_sources(location)
    console.print("[green]Forecast Comparison:[/green]")
    pprint(comparison)


@app.command()
def weather_recommendations(location: str, activity: str = "") -> None:
    """
    Get weather-based recommendations for activities or planning
    """
    console.print(f"[cyan]Getting recommendations for {location}...[/cyan]")
    predictor = WeatherPredictor()
    recommendations = predictor.get_weather_recommendations(location, activity)
    console.print("[green]Weather Recommendations:[/green]")
    console.print(recommendations)


@app.command()
def ask_weather_llm(question: str, location: str = "") -> None:
    """
    Ask the weather AI any weather-related question
    """
    console.print(f"[cyan]Querying Weather AI: {question}[/cyan]")
    executor = Executor()
    if location:
        response = executor.get_weather_forecast_llm(question, location)
    else:
        response = executor.get_weather_llm_response(question)
    console.print("[green]Weather AI Response:[/green]")
    console.print(response)


@app.command()
def ask_weather_superforecaster(
    location: str, 
    question: str, 
    condition: str
) -> None:
    """
    Get superforecaster prediction for a specific weather condition
    """
    console.print(f"[cyan]Location: {location}[/cyan]")
    console.print(f"[cyan]Question: {question}[/cyan]")
    console.print(f"[cyan]Condition: {condition}[/cyan]")
    executor = Executor()
    response = executor.get_weather_superforecast(
        location=location,
        question=question,
        condition=condition
    )
    console.print("[green]Superforecaster Response:[/green]")
    console.print(response)


if __name__ == "__main__":
    app()
