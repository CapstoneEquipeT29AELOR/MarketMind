from fastapi import FastAPI, Request
from dotenv import load_dotenv

from utils import query_news_api

load_dotenv()
app = FastAPI(title="MarketMind API", version="0.1.0")


@app.get("/api/stocks")
async def list_stocks():
    pass


@app.get("/api/stocks/{symbol}/chart")
async def get_stock_chart(symbol: str, range: str = "1M"):
    pass


@app.get("/api/news")
async def get_news(query: str, from_date: str = None):
    news = query_news_api(query, from_date)
    return news, 200


@app.get("/api/analysis/{symbol}")
async def get_analysis(symbol: str):
    # algorithm will be ran from here. If a BUY or SELL signal is produced for the day, return the signal to the user. 
    pass


@app.get("/api/preferences")
async def get_preferences():
    pass


@app.put("/api/preferences")
async def update_preferences(preferences: dict):
    pass

# Run with: uvicorn main:app --reload --port 8080

