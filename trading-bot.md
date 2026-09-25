**Stage 1: Data Ingestion**

**Function:** Fetch historical and real-time price data for your chosen stocks or ETFs.

**What it does:** Your bot needs to know what the price of an asset is right now and what it has been in the past. You connect to a data provider (like Alpaca, Yahoo Finance, or Polygon) and pull this data into your system.

**Stage 2: Strategy Engine (The Brain)**

**Function:** Apply your trading logic to the incoming data to generate a signal.

**What it does:** This is where you define your rules. A simple starting point is a "moving average crossover." 

- The bot calculates a fast moving average and a slow moving average. If the fast one crosses *above* the slow one, it generates a **BUY** signal. If it crosses *below*, it generates a **SELL** signal.
- To incorporate the news:
    
    ```python
    # After you detect a crossover...
    if BUY: # A BUY signal
        
        # 1. Fetch the latest news for the symbol
        news_headlines = fetch_latest_news("SPY")
        
        # 2. Analyze the sentiment (using VADER or a simple keyword check)
        sentiment_score = analyze_sentiment(news_headlines)
        
        # 3. The Filter: Only buy if sentiment isn't strongly bearish
        if sentiment_score > -0.2: # Adjust this threshold
            execute_buy_order("SPY")
            print(f"Bought SPY. Sentiment was {sentiment_score}")
        else:
            print(f"Skipped BUY. Sentiment was too negative ({sentiment_score})")
    ```
    
    - Good sentiment analysis models for financial news:
        - https://github.com/cjhutto/vadersentiment
        - https://finbert.org/
- This can be heavily modified as we construct a better performing algorithm.

**Stage 3: Risk Management & Sizing**

**Function:** Decide *how much* to trade based on your rules.

**What it does:** Just getting a "BUY" signal isn't enough. You need to tell the bot how much money to allocate. This stage checks your current cash balance and position size to determine the number of shares to buy. It also prevents the bot from making reckless trades (e.g., "Never risk more than 2% of my portfolio on one trade").

- e.g., `shares_to_buy = (portfolio_value * 0.02) / current_price`

**Stage 4: Execution**

**Function:** Send the order to the broker.

**What it does:** This stage takes the action decided in Stage 3 (e.g., "Buy 10 shares of SPY") and sends it to your brokerage's API. The broker executes the trade in the real (or simulated) market.

**Tools:** Alpaca

**Stage 5: Logging & Monitoring (important)**

**Function:** Record everything that happens for review.

**What it does:** An autonomous bot runs while you sleep. If it crashes or makes a bad trade, you need to know *why*. This stage writes a log file recording every signal, order submission, fill confirmation, and error message. This creates an "audit trail" that is essential for debugging and improving your strategy.
