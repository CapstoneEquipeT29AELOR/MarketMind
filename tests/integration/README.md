# Integration tests

Status: **TODO — this folder contains instructions only.**

## Code or content to add

Add tests for API-to-service-to-database flows and summary source references. Use a temporary database and controlled provider responses.

Example files: test_news_pipeline.py, test_market_api.py. Keep optional live-provider tests explicitly separate from the normal offline suite.

## First useful milestone

A known fixture can be imported, retrieved through the API, and cleaned up without touching real user data.
