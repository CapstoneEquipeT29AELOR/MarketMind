# Database access and schema

Status: **TODO — this folder contains instructions only.**

## Code or content to add

Add connection management, a schema for stocks/prices/news/summaries, and query functions. Include identifiers, source references, UTC timestamps, and uniqueness rules so repeated ingestion does not duplicate records.

Example files: connection.py, schema.sql, news_repository.py, prices_repository.py. Choose the database and migration tool before adding framework-specific code. Put schema migrations in migrations/.

## First useful milestone

A fresh local database can store and retrieve a small price/news sample reproducibly.
