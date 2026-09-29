#To run : .\.venv\Scripts\python.exe -m pip config debug

from fastapi import FastAPI
import sqlite3

app = FastAPI(
    title="MarketMind API",
    description="Backend for MarketMind's news and market analysis.",
    version="0.1.0",
)

@app.on_event("startup")
def on_startup():
    # initializing the DB schema
    conn = sqlite3.connect("marketmind.db")
    cursor = conn.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        password TEXT NOT NULL
    )
    """) # change the statement to update the DB schema

@app.get("/")
def root():
    return {"message": "Welcome to the MarketMind API"}

@app.get("/health")
def health():
    return {"status": "ok"}

