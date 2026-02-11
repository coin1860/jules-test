from typing import List, Optional
import pandas as pd

class StrategyModule:
    def __init__(self, short_window: int = 5, long_window: int = 20):
        if short_window <= 0 or long_window <= 0:
            raise ValueError("Windows must be positive")
        if short_window >= long_window:
            raise ValueError("Short window must be less than long window")

        self.short_window = short_window
        self.long_window = long_window
        self.prices: List[float] = []

    def on_tick(self, price: float) -> str:
        """
        Ingests a new price and returns a signal: 'BUY', 'SELL', or 'HOLD'.
        """
        if price <= 0:
            raise ValueError("Price must be positive")

        self.prices.append(price)

        # Need enough data for the long window
        if len(self.prices) < self.long_window:
            return "HOLD"

        # Calculate SMAs
        # We need at least long_window + 1 data points to detect a crossover
        # (current and previous)
        # But wait, if we just arrived at long_window, we have 1 point of SMA.
        # To detect crossover, we compare SMA(t) and SMA(t-1).

        if len(self.prices) < self.long_window + 1:
             return "HOLD"

        series = pd.Series(self.prices)
        short_sma = series.rolling(window=self.short_window).mean()
        long_sma = series.rolling(window=self.long_window).mean()

        curr_short = short_sma.iloc[-1]
        curr_long = long_sma.iloc[-1]

        prev_short = short_sma.iloc[-2]
        prev_long = long_sma.iloc[-2]

        # Golden Cross: Short crosses above Long
        if prev_short <= prev_long and curr_short > curr_long:
            return "BUY"

        # Death Cross: Short crosses below Long
        if prev_short >= prev_long and curr_short < curr_long:
            return "SELL"

        return "HOLD"
