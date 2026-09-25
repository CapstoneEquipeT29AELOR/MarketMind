# this script uses simple moving average to trigger BUY or SELL signals
# this is just a simple PoC that we can build on

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Get data
prices = yf.download("NVDA", start="2020-01-01")

print(prices)

# Compute indicators
prices["sma_fast"] = prices["Close"].rolling(20).mean()
prices["sma_slow"] = prices["Close"].rolling(50).mean()

# Generate signals
prices["signal"] = np.where(prices["sma_fast"] > prices["sma_slow"], 1, 0)

# Detect changes (crossovers)
prices["trade"] = prices["signal"].diff()
# trade == 1 -> buy, trade == -1 -> sell, hold == 0 -> hold

buys = prices[prices["trade"] == 1]
sells = prices[prices["trade"] == -1]

plt.plot(prices.index, prices["Close"], label="close price", color="black")
plt.plot(prices.index, prices["sma_fast"], label="sma fast", color="orange")
plt.plot(prices.index, prices["sma_slow"], label="sma slow", color="blue")
plt.scatter(buys.index, buys["Close"], label="BUY", color="green", s=100)
plt.scatter(sells.index, sells["Close"], label="SELL", color="red", s=100)
plt.legend()
plt.show()
