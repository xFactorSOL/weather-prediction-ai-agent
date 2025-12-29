from __future__ import annotations
from typing import Optional, Union
from pydantic import BaseModel


class Trade(BaseModel):
    id: int
    taker_order_id: str
    market: str
    asset_id: str
    side: str
    size: str
    fee_rate_bps: str
    price: str
    status: str
    match_time: str
    last_update: str
    outcome: str
    maker_address: str
    owner: str
    transaction_hash: str
    bucket_index: str
    maker_orders: list[str]
    type: str


class SimpleMarket(BaseModel):
    id: int
    question: str
    # start: str
    end: str
    description: str
    active: bool
    # deployed: Optional[bool]
    funded: bool
    # orderMinSize: float
    # orderPriceMinTickSize: float
    rewardsMinSize: float
    rewardsMaxSpread: float
    # volume: Optional[float]
    spread: float
    outcomes: str
    outcome_prices: str
    clob_token_ids: Optional[str]


class ClobReward(BaseModel):
    id: str  # returned as string in api but really an int?
    conditionId: str
    assetAddress: str
    rewardsAmount: float  # only seen 0 but could be float?
    rewardsDailyRate: int  # only seen ints but could be float?
    startDate: str  # yyyy-mm-dd formatted date string
    endDate: str  # yyyy-mm-dd formatted date string


class Tag(BaseModel):
    id: str
    label: Optional[str] = None
    slug: Optional[str] = None
    forceShow: Optional[bool] = None  # missing from current events data
    createdAt: Optional[str] = None  # missing from events data
    updatedAt: Optional[str] = None  # missing from current events data
    _sync: Optional[bool] = None


class PolymarketEvent(BaseModel):
    id: str  # "11421"
    ticker: Optional[str] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    startDate: Optional[str] = None
    creationDate: Optional[str] = (
        None  # fine in market event but missing from events response
    )
    endDate: Optional[str] = None
    image: Optional[str] = None
    icon: Optional[str] = None
    active: Optional[bool] = None
    closed: Optional[bool] = None
    archived: Optional[bool] = None
    new: Optional[bool] = None
    featured: Optional[bool] = None
    restricted: Optional[bool] = None
    liquidity: Optional[float] = None
    volume: Optional[float] = None
    reviewStatus: Optional[str] = None
    createdAt: Optional[str] = None  # 2024-07-08T01:06:23.982796Z,
    updatedAt: Optional[str] = None  # 2024-07-15T17:12:48.601056Z,
    competitive: Optional[float] = None
    volume24hr: Optional[float] = None
    enableOrderBook: Optional[bool] = None
    liquidityClob: Optional[float] = None
    _sync: Optional[bool] = None
    commentCount: Optional[int] = None
    # markets: list[str, 'Market'] # forward reference Market defined below - TODO: double check this works as intended
    markets: Optional[list[Market]] = None
    tags: Optional[list[Tag]] = None
    cyom: Optional[bool] = None
    showAllOutcomes: Optional[bool] = None
    showMarketImages: Optional[bool] = None


class Market(BaseModel):
    id: int
    question: Optional[str] = None
    conditionId: Optional[str] = None
    slug: Optional[str] = None
    resolutionSource: Optional[str] = None
    endDate: Optional[str] = None
    liquidity: Optional[float] = None
    startDate: Optional[str] = None
    image: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    outcome: Optional[list] = None
    outcomePrices: Optional[list] = None
    volume: Optional[float] = None
    active: Optional[bool] = None
    closed: Optional[bool] = None
    marketMakerAddress: Optional[str] = None
    createdAt: Optional[str] = None  # date type worth enforcing for dates?
    updatedAt: Optional[str] = None
    new: Optional[bool] = None
    featured: Optional[bool] = None
    submitted_by: Optional[str] = None
    archived: Optional[bool] = None
    resolvedBy: Optional[str] = None
    restricted: Optional[bool] = None
    groupItemTitle: Optional[str] = None
    groupItemThreshold: Optional[int] = None
    questionID: Optional[str] = None
    enableOrderBook: Optional[bool] = None
    orderPriceMinTickSize: Optional[float] = None
    orderMinSize: Optional[int] = None
    volumeNum: Optional[float] = None
    liquidityNum: Optional[float] = None
    endDateIso: Optional[str] = None  # iso format date = None
    startDateIso: Optional[str] = None
    hasReviewedDates: Optional[bool] = None
    volume24hr: Optional[float] = None
    clobTokenIds: Optional[list] = None
    umaBond: Optional[int] = None  # returned as string from api?
    umaReward: Optional[int] = None  # returned as string from api?
    volume24hrClob: Optional[float] = None
    volumeClob: Optional[float] = None
    liquidityClob: Optional[float] = None
    acceptingOrders: Optional[bool] = None
    negRisk: Optional[bool] = None
    commentCount: Optional[int] = None
    _sync: Optional[bool] = None
    events: Optional[list[PolymarketEvent]] = None
    ready: Optional[bool] = None
    deployed: Optional[bool] = None
    funded: Optional[bool] = None
    deployedTimestamp: Optional[str] = None  # utc z datetime string
    acceptingOrdersTimestamp: Optional[str] = None  # utc z datetime string,
    cyom: Optional[bool] = None
    competitive: Optional[float] = None
    pagerDutyNotificationEnabled: Optional[bool] = None
    reviewStatus: Optional[str] = None  # deployed, draft, etc.
    approved: Optional[bool] = None
    clobRewards: Optional[list[ClobReward]] = None
    rewardsMinSize: Optional[int] = (
        None  # would make sense to allow float but we'll see
    )
    rewardsMaxSpread: Optional[float] = None
    spread: Optional[float] = None


class ComplexMarket(BaseModel):
    id: int
    condition_id: str
    question_id: str
    tokens: Union[str, str]
    rewards: str
    minimum_order_size: str
    minimum_tick_size: str
    description: str
    category: str
    end_date_iso: str
    game_start_time: str
    question: str
    market_slug: str
    min_incentive_size: str
    max_incentive_spread: str
    active: bool
    closed: bool
    seconds_delay: int
    icon: str
    fpmm: str
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class SimpleEvent(BaseModel):
    id: int
    ticker: str
    slug: str
    title: str
    description: str
    end: str
    active: bool
    closed: bool
    archived: bool
    restricted: bool
    new: bool
    featured: bool
    restricted: bool
    markets: str


class Source(BaseModel):
    id: Optional[str]
    name: Optional[str]


class Article(BaseModel):
    source: Optional[Source]
    author: Optional[str]
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    urlToImage: Optional[str]
    publishedAt: Optional[str]
    content: Optional[str]


# Weather-specific models
class WeatherCondition(BaseModel):
    """Represents a weather condition at a specific time"""
    temperature: float
    feels_like: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    visibility: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    cloudiness: Optional[float] = None
    precipitation: Optional[float] = None
    description: Optional[str] = None
    main_condition: Optional[str] = None  # e.g., "Rain", "Clear", "Clouds"
    icon: Optional[str] = None
    timestamp: Optional[str] = None


class WeatherLocation(BaseModel):
    """Represents a geographic location for weather queries"""
    name: str
    country: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None
    elevation: Optional[float] = None


class WeatherForecast(BaseModel):
    """Represents a weather forecast for a location"""
    location: WeatherLocation
    current: Optional[WeatherCondition] = None
    forecasts: list[WeatherCondition] = []  # Hourly or daily forecasts
    forecast_type: str = "daily"  # "hourly" or "daily"
    source: Optional[str] = None  # "openweather", "weatherapi", etc.
    created_at: Optional[str] = None
    confidence: Optional[float] = None  # Prediction confidence score


class WeatherEvent(BaseModel):
    """Represents a significant weather event (storm, heatwave, etc.)"""
    id: str
    title: str
    description: str
    location: WeatherLocation
    event_type: str  # "hurricane", "tornado", "heatwave", "blizzard", etc.
    severity: Optional[str] = None  # "low", "moderate", "high", "extreme"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    active: bool = True
    alerts: list[str] = []
    impact_areas: list[str] = []


class SimpleWeatherForecast(BaseModel):
    """Simplified weather forecast model for RAG and filtering"""
    id: str
    location_name: str
    question: str  # e.g., "Will it rain tomorrow?"
    description: str
    forecast_date: str
    end_date: Optional[str] = None
    active: bool = True
    temperature_range: str  # e.g., "20-25°C"
    conditions: str  # e.g., "Rain, Cloudy"
    confidence: float  # 0.0 to 1.0
    source: str
