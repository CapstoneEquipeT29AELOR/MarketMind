from fastapi import FastAPI

app = FastAPI(
    title="MarketMind API",
    description="Backend for MarketMind's news and market analysis.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to the MarketMind API"}


@app.get("/health")
def health():
    return {"status": "ok"}