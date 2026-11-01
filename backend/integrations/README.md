# External data and AI provider adapters

Status: **TODO — this folder contains instructions only.**

## Code or content to add

Add financial-price and news-provider clients with timeouts, bounded retries, pagination, and normalized results. Preserve source URL, publisher, publication time, ticker, and retrieval time for news. Add an AI-provider adapter if the summary implementation needs one.

Example files: price_provider.py, news_provider.py, ai_provider.py. Existing research price fetching remains in ml/forecasting/marketmind_model.py until deliberately refactored.

## First useful milestone

Provider responses become consistent internal records and failed requests produce useful errors.
