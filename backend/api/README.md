# HTTP routes and application entrypoint

Status: **TODO — this folder contains instructions only.**

## Code or content to add

Add a Python web application entrypoint and route handlers. Start with health, supported stocks, prices, and news; then add summaries. Call backend services instead of downloading or training inside route handlers.

Example files: main.py, stocks.py, prices.py, news.py, summaries.py. Suggested routes: GET /health, /stocks, /stocks/{ticker}/prices, /stocks/{ticker}/news, /stocks/{ticker}/summary. These routes do not exist yet.

## First useful milestone

A local request returns validated JSON with predictable error responses.
