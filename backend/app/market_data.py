from abc import ABC, abstractmethod
import yfinance as yf
import pandas as pd
from typing import Optional

class MarketDataProvider(ABC):
    @abstractmethod
    def get_current_price(self, symbol: str) -> float:
        """Fetches the current price for the given symbol."""
        pass

    @abstractmethod
    def get_historical_prices(self, symbol: str, period: str = "1mo", interval: str = "1d") -> pd.Series:
        """Fetches historical close prices."""
        pass

class YFinanceProvider(MarketDataProvider):
    def get_current_price(self, symbol: str) -> float:
        try:
            ticker = yf.Ticker(symbol)
            # yfinance often returns 'regularMarketPrice' or 'currentPrice' in info
            # but for FX, it might be in history.
            # Let's try fetching the last 1 minute of data for the most accurate recent price
            df = ticker.history(period="1d", interval="1m")
            if df.empty:
                 # Fallback for when market is closed or 1m data unavailable
                df = ticker.history(period="1d")

            if df.empty:
                raise ValueError(f"No data found for {symbol}")

            return float(df["Close"].iloc[-1])
        except Exception as e:
            raise RuntimeError(f"Error fetching price for {symbol}: {e}")

    def get_historical_prices(self, symbol: str, period: str = "1mo", interval: str = "1d") -> pd.Series:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            if df.empty:
                 raise ValueError(f"No historical data found for {symbol}")
            return df["Close"]
        except Exception as e:
            raise RuntimeError(f"Error fetching history for {symbol}: {e}")
