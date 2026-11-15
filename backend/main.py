from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv

from utils import get_market_news, get_stock_analysis, get_stock_price_json

load_dotenv()
app = FastAPI(title="MarketMind API", version="0.1.0")


# Errors use the contract's {"error": "..."} shape instead of FastAPI's {"detail": ...}
@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": str(exc.detail)})


@app.get("/api/stocks")
async def list_stocks():
    pass


@app.get("/api/stocks/{symbol}/chart")
async def get_stock_chart(symbol: str, range_: str = "1mo"):
    # TODO: add parameter validation
    return get_stock_price_json(symbol, range_)


@app.get("/api/news")
def get_news(symbol: str | None = None, limit: int = Query(20, ge=1, le=50)):
    """example use: Invoke-RestMethod "http://localhost:8080/api/news"  """
    return get_market_news(symbol, limit)


@app.get("/api/analysis/{symbol}")
def get_analysis(symbol: str):
    """example use: Invoke-RestMethod "http://localhost:8080/api/analysis/NVDA" """
    result = get_stock_analysis(symbol)
    if result is None:
        raise HTTPException(status_code=404, detail="Stock symbol not found")
    return result


@app.get("/api/preferences")
async def get_preferences():
    pass


@app.put("/api/preferences")
async def update_preferences(preferences: dict):
    pass

# Run with: uvicorn main:app --reload --port 8080