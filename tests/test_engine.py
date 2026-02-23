import pytest
import time
from unittest.mock import MagicMock, patch
from backend.app.engine import TradingEngine
from backend.app.market_data import MarketDataProvider
from backend.app.account import AccountManager
from backend.app.strategy import StrategyModule

@pytest.fixture
def mock_market_data():
    return MagicMock(spec=MarketDataProvider)

@pytest.fixture
def mock_account():
    # Need to mock attributes accessed directly
    account = MagicMock(spec=AccountManager)
    account.balance_cny = 10000.0
    account.balance_usd = 1000.0
    account.get_balances.return_value = {"cny": 10000.0, "usd": 1000.0}
    return account

@pytest.fixture
def mock_strategy():
    strategy = MagicMock(spec=StrategyModule)
    strategy.short_window = 5
    strategy.long_window = 20
    return strategy

@pytest.fixture
def engine(mock_market_data, mock_account, mock_strategy):
    # Set interval to 0.1s for fast testing
    return TradingEngine(mock_market_data, mock_account, mock_strategy, interval=0.1)

def test_start_stop(engine):
    assert not engine.is_running
    engine.start()
    assert engine.is_running
    # Wait for loop to run at least once
    time.sleep(0.2)
    engine.stop()
    assert not engine.is_running

def test_run_step_buy(engine, mock_market_data, mock_strategy, mock_account):
    mock_market_data.get_current_price.return_value = 7.0
    mock_strategy.on_tick.return_value = "BUY"

    # We call _run_step directly to test logic synchronously
    engine._run_step()

    mock_market_data.get_current_price.assert_called_with("CNY=X")
    mock_strategy.on_tick.assert_called_with(7.0)
    mock_account.buy_usd.assert_called_with(100.0, 7.0)

def test_run_step_sell(engine, mock_market_data, mock_strategy, mock_account):
    mock_market_data.get_current_price.return_value = 7.2
    mock_strategy.on_tick.return_value = "SELL"

    engine._run_step()

    mock_account.sell_usd.assert_called_with(100.0, 7.2)

def test_get_status(engine, mock_account):
    engine.last_price = 7.0
    engine.last_signal = "HOLD"
    mock_account.get_equity_cny.return_value = 17000.0

    status = engine.get_status()
    assert status["running"] == False
    assert status["price"] == 7.0
    assert status["signal"] == "HOLD"
    assert status["equity_cny"] == 17000.0
    assert status["strategy"]["short_window"] == 5

def test_update_strategy(engine, mock_strategy):
    engine.update_strategy_parameters(10, 30)
    mock_strategy.update_parameters.assert_called_with(10, 30)
