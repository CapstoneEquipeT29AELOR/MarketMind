from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv

from utils import get_market_news, get_stock_analysis, get_stock_price_json, get_stock_lookup
from models import StockLookupParams, StockChartParams, NewsParams, AnalysisParams

load_dotenv()
app = FastAPI(title="MarketMind API", version="0.1.0")


# Errors use the contract's {"error": "..."} shape instead of FastAPI's {"detail": ...}
@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": str(exc.detail)})


@app.post("/api/stocks/search")
async def search_stocks(params: StockLookupParams):
   return get_stock_lookup(params.query) 


@app.post("/api/stocks/chart")
async def get_stock_chart(params: StockChartParams):
    return get_stock_price_json(params.symbol, params.timeline)


@app.post("/api/stocks/news")
def get_news(params: NewsParams):
    return get_market_news(params.symbol, params.limit)


@app.post("/api/stocks/analysis")
def get_analysis(params: AnalysisParams):
    result = get_stock_analysis(params.symbol)
    if result is None:
        raise HTTPException(status_code=404, detail="Stock symbol not found")
    return result

# Run with: uvicorn main:app --reload --port 8080
