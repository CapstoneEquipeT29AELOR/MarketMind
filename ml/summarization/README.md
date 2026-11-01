# Source-backed news summaries

Status: **TODO — this folder contains instructions only.**

## Code or content to add

Add the summarization module that receives article records and returns a concise summary with references to the input sources. Keep article IDs/URLs in the result and handle missing or conflicting evidence.

Example files: summarize_news.py and prompts.md. A possible interface is summarize_articles(articles). FinBERT sentiment scores are not article summaries.

## First useful milestone

Each returned summary includes traceable source references and handles an empty article list.
