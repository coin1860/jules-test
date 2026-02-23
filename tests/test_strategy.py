import pytest
from backend.app.strategy import StrategyModule

def test_initialization():
    strategy = StrategyModule(short_window=5, long_window=20)
    assert strategy.short_window == 5
    assert strategy.long_window == 20
    assert strategy.prices == []

def test_initialization_invalid():
    with pytest.raises(ValueError):
        StrategyModule(short_window=-1, long_window=20)
    with pytest.raises(ValueError):
        StrategyModule(short_window=5, long_window=5) # Equal not allowed
    with pytest.raises(ValueError):
        StrategyModule(short_window=20, long_window=5) # Short > Long

def test_on_tick_insufficient_data():
    strategy = StrategyModule(short_window=2, long_window=4)
    # Need 5 points to start.
    assert strategy.on_tick(10.0) == "HOLD" # 1
    assert strategy.on_tick(10.0) == "HOLD" # 2
    assert strategy.on_tick(10.0) == "HOLD" # 3
    assert strategy.on_tick(10.0) == "HOLD" # 4

def test_on_tick_buy_signal():
    strategy = StrategyModule(short_window=2, long_window=4)
    # Feed initial 4 points (10, 10, 10, 10)
    for _ in range(4):
        strategy.on_tick(10.0)

    # 5th point: Price jumps to 12.
    # Prev: S=10, L=10.
    # Curr: S=11, L=10.5.
    # Cross: 10<=10 and 11>10.5 -> BUY
    assert strategy.on_tick(12.0) == "BUY"

def test_on_tick_hold_signal():
    strategy = StrategyModule(short_window=2, long_window=4)
    # Setup BUY
    for _ in range(4): strategy.on_tick(10.0)
    strategy.on_tick(12.0) # BUY

    # 6th point: Price 14.
    # Prev: S=11, L=10.5.
    # Curr: S=13, L=11.5.
    # S > L continues -> HOLD
    assert strategy.on_tick(14.0) == "HOLD"

def test_on_tick_sell_signal():
    strategy = StrategyModule(short_window=2, long_window=4)
    # Setup BUY & Trend
    for _ in range(4): strategy.on_tick(10.0)
    strategy.on_tick(12.0) # BUY
    strategy.on_tick(14.0) # HOLD
    strategy.on_tick(10.0) # HOLD (S=12, L=11.5)

    # 8th point: Price 8.
    # Prev: S=12, L=11.5.
    # Curr: S=9, L=11.
    # Cross: 12>=11.5 and 9<11 -> SELL
    assert strategy.on_tick(8.0) == "SELL"

def test_on_tick_invalid_price():
    strategy = StrategyModule()
    with pytest.raises(ValueError):
        strategy.on_tick(-10.0)
