from enum import Enum
from typing import Dict, List

from fastapi import APIRouter, FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="MarketMind API",
    version="0.1.0",
    description=(
        "Minimal backend contract for the MarketMind frontend. This includes "
        "only the data and endpoints currently required by the app UI."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix="/api")


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ChartRange(str, Enum):
    ONE_DAY = "1D"
    ONE_WEEK = "1W"
    ONE_MONTH = "1M"
    THREE_MONTHS = "3M"
    ONE_YEAR = "1Y"
    FIVE_YEARS = "5Y"


class Tone(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class FactorImpact(str, Enum):
    positive = "positive"
    caution = "caution"
    negative = "negative"


class Language(str, Enum):
    en = "en"
    fr = "fr"


class Theme(str, Enum):
    light = "light"
    dark = "dark"
    system = "system"


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ErrorResponse(BaseModel):
    error: str = Field(..., examples=["Stock symbol not found"])


class Stock(BaseModel):
    symbol: str = Field(..., examples=["NVDA"])
    name: str = Field(..., examples=["NVIDIA Corporation"])
    exchange: str = Field(..., examples=["NASDAQ"])
    price: float = Field(..., examples=[118.42])
    change: float = Field(..., examples=[2.68])
    changePercent: float = Field(..., examples=[2.31])
    marketCap: str = Field(..., examples=["$2.90T"])
    volume: str = Field(..., examples=["42.8M"])
    dayHigh: float = Field(..., examples=[119.87])
    dayLow: float = Field(..., examples=[115.24])
    chart: Dict[str, List[float]] = Field(
        ...,
        examples=[{"1D": [115.8, 116.1, 116.4, 118.42], "1M": [108.6, 112.3, 116.5, 118.42]}],
    )


class ChartResponse(BaseModel):
    symbol: str = Field(..., examples=["NVDA"])
    range: str = Field(..., examples=["1M"])
    points: List[float] = Field(..., examples=[[108.6, 110.4, 109.8, 112.3, 118.42]])


class NewsItem(BaseModel):
    source: str = Field(..., examples=["Reuters"])
    time: str = Field(..., examples=["12 min ago"])
    category: str = Field(..., examples=["Technology"])
    headline: str
    summary: str
    symbols: List[str] = Field(..., examples=[["NVDA", "AMD"]])
    tone: Tone


class AnalysisFactor(BaseModel):
    label: str = Field(..., examples=["Data-center demand"])
    detail: str
    impact: FactorImpact


class StockAnalysis(BaseModel):
    sentiment: str = Field(..., examples=["Bullish"])
    score: int = Field(..., ge=0, le=100, examples=[78])
    confidence: int = Field(..., ge=0, le=100, examples=[84])
    summary: str
    factors: List[AnalysisFactor]


class NotificationPreferences(BaseModel):
    priceAlerts: bool
    marketNews: bool
    dailySummary: bool


class UserPreferences(BaseModel):
    language: Language
    theme: Theme
    timeZone: str = Field(..., examples=["America/New_York"])
    region: str = Field(..., examples=["US"])
    currency: str = Field(..., examples=["USD"])
    chartPeriod: ChartRange
    notifications: NotificationPreferences


# ---------------------------------------------------------------------------
# Endpoints (empty stubs)
# ---------------------------------------------------------------------------

@api.get(
    "/stocks",
    response_model=List[Stock],
    operation_id="listStocks",
    summary="Get the list of tracked stocks for the dashboard and stock selector",
)
async def list_stocks():
    # TODO: implement
    ...


@api.get(
    "/stocks/{symbol}/chart",
    response_model=ChartResponse,
    operation_id="getStockChart",
    summary="Get historical chart values for a stock",
    responses={404: {"model": ErrorResponse}},
)
async def get_stock_chart(
    symbol: str = Path(..., examples=["NVDA"]),
    range: ChartRange = Query(ChartRange.ONE_MONTH),
):
    # TODO: implement (raise HTTPException(404) if symbol is unknown)
    ...


@api.get(
    "/news",
    response_model=List[NewsItem],
    operation_id="getNews",
    summary="Get the market news feed",
)
async def get_news():
    # TODO: implement
    ...


@api.get(
    "/analysis/{symbol}",
    response_model=StockAnalysis,
    operation_id="getAnalysis",
    summary="Get AI sentiment analysis for a stock",
    responses={404: {"model": ErrorResponse}},
)
async def get_analysis(symbol: str = Path(..., examples=["NVDA"])):
    # TODO: implement (raise HTTPException(404) if symbol is unknown)
    ...


@api.get(
    "/preferences",
    response_model=UserPreferences,
    operation_id="getPreferences",
    summary="Get saved user preferences",
)
async def get_preferences():
    # TODO: implement
    ...


@api.put(
    "/preferences",
    response_model=UserPreferences,
    operation_id="updatePreferences",
    summary="Update saved user preferences",
    responses={400: {"model": ErrorResponse}},
)
async def update_preferences(preferences: UserPreferences):
    # TODO: implement
    ...


app.include_router(api)

# Run with: uvicorn main:app --reload --port 8080
