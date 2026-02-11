import pytest
from unittest.mock import MagicMock, patch
from src.engine import TradingEngine
from src.market_data import MarketDataProvider
from src.account import AccountManager
from src.strategy import StrategyModule

@pytest.fixture
def mock_market_data():
    return MagicMock(spec=MarketDataProvider)

@pytest.fixture
def mock_account():
    return MagicMock(spec=AccountManager)

@pytest.fixture
def mock_strategy():
    return MagicMock(spec=StrategyModule)

@pytest.fixture
def engine(mock_market_data, mock_account, mock_strategy):
    return TradingEngine(mock_market_data, mock_account, mock_strategy)

def test_run_step_buy(engine, mock_market_data, mock_strategy, mock_account):
    mock_market_data.get_current_price.return_value = 7.0
    mock_strategy.on_tick.return_value = "BUY"

    engine.run_step()

    mock_market_data.get_current_price.assert_called_with("CNY=X")
    mock_strategy.on_tick.assert_called_with(7.0)
    mock_account.buy_usd.assert_called_with(100.0, 7.0)

def test_run_step_sell(engine, mock_market_data, mock_strategy, mock_account):
    mock_market_data.get_current_price.return_value = 7.2
    mock_strategy.on_tick.return_value = "SELL"

    engine.run_step()

    mock_account.sell_usd.assert_called_with(100.0, 7.2)

def test_run_step_hold(engine, mock_market_data, mock_strategy, mock_account):
    mock_market_data.get_current_price.return_value = 7.1
    mock_strategy.on_tick.return_value = "HOLD"

    engine.run_step()

    mock_account.buy_usd.assert_not_called()
    mock_account.sell_usd.assert_not_called()

def test_run_step_error_fetching_price(engine, mock_market_data):
    mock_market_data.get_current_price.side_effect = RuntimeError("API Error")

    # run_step should catch the exception and log error, not crash
    engine.run_step()

    # Verify no trade attempted (implicit)

def test_run_step_buy_error(engine, mock_market_data, mock_strategy, mock_account):
    mock_market_data.get_current_price.return_value = 7.0
    mock_strategy.on_tick.return_value = "BUY"
    mock_account.buy_usd.side_effect = ValueError("Insufficient Funds")

    engine.run_step()

    # Should catch and continue (logging error)

def test_run_step_sell_error(engine, mock_market_data, mock_strategy, mock_account):
    mock_market_data.get_current_price.return_value = 7.0
    mock_strategy.on_tick.return_value = "SELL"
    mock_account.sell_usd.side_effect = ValueError("Insufficient Funds")

    engine.run_step()

    # Should catch and continue (logging error)

def test_run_loop(engine):
    # Mock run_step to avoid infinite loop or actual logic execution
    with patch.object(engine, 'run_step', side_effect=[None, KeyboardInterrupt]) as mock_run_step:
        # Also mock sleep to speed up test
        with patch('time.sleep'):
            engine.run(interval=1)
            assert mock_run_step.call_count == 2
            assert engine.is_running is False
