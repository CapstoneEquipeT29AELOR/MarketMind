# Application services

Status: **TODO — this folder contains instructions only.**

## Code or content to add

Add the code that combines provider data, database results, and AI output into dashboard responses. Centralize ticker validation, data freshness rules, caching policy, and error translation.

Example files: market_service.py, news_service.py, summary_service.py. Delegate provider calls to ../integrations/ and database queries to ../database/.

## First useful milestone

Services can be tested using fake providers without network access.
