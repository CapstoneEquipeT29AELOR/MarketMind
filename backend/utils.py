import requests
import os
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
