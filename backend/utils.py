import requests
import yfinance
import os
import json
from datetime import datetime

def query_news_api(query: str, from_date: str) -> object:
    parsed_date = datetime.strptime(from_date, "%Y-%m-%d")
    res = requests.get(
        "https://newsapi.org/v2/everything",
        params={
            "q": query,
            "from": from_date,
            "sortBy": "popularity",
            "apiKey": os.getenv("NEWS_API_KEY"),
        },
    )
    res.raise_for_status()
    return res.json()

def get_stock_price_json(symbol: str, period: str) -> object:
    df = yfinance.download(symbol, period=period)
    data = json.loads(df["Close"].to_json())
    parsed = {}
    kv = data[symbol].items()
    for k,v in kv:
        ts = int(k)
        dt_obj = datetime.fromtimestamp(ts//1000)
        dt_str = dt_obj.strftime("%Y-%m-%d")
        parsed[dt_str] = data[symbol][k]
    return parsed
