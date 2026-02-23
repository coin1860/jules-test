import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from backend.app.market_data import YFinanceProvider

@pytest.fixture
def provider():
    return YFinanceProvider()

def test_get_current_price_success(provider):
    mock_ticker = MagicMock()
    # Mock return value of history()
    mock_df = pd.DataFrame({"Close": [7.25]}, index=pd.date_range("2023-01-01", periods=1))
    mock_ticker.history.return_value = mock_df

    with patch("yfinance.Ticker", return_value=mock_ticker):
        price = provider.get_current_price("CNY=X")
        assert price == 7.25
        mock_ticker.history.assert_called()

def test_get_current_price_fallback(provider):
    mock_ticker = MagicMock()
    # First call returns empty (1m data unavailable)
    # Second call returns valid data (fallback to 1d)

    mock_df_empty = pd.DataFrame()
    mock_df_valid = pd.DataFrame({"Close": [7.20]}, index=pd.date_range("2023-01-01", periods=1))

    mock_ticker.history.side_effect = [mock_df_empty, mock_df_valid]

    with patch("yfinance.Ticker", return_value=mock_ticker):
        price = provider.get_current_price("CNY=X")
        assert price == 7.20
        assert mock_ticker.history.call_count == 2

def test_get_current_price_no_data(provider):
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = pd.DataFrame()

    with patch("yfinance.Ticker", return_value=mock_ticker):
        with pytest.raises(RuntimeError) as exc:
            provider.get_current_price("INVALID")
        assert "Error fetching price" in str(exc.value)

def test_get_historical_prices_success(provider):
    mock_ticker = MagicMock()
    mock_df = pd.DataFrame({"Close": [7.10, 7.15, 7.20]}, index=pd.date_range("2023-01-01", periods=3))
    mock_ticker.history.return_value = mock_df

    with patch("yfinance.Ticker", return_value=mock_ticker):
        series = provider.get_historical_prices("CNY=X")
        assert len(series) == 3
        assert series.iloc[-1] == 7.20

def test_get_historical_prices_error(provider):
    with patch("yfinance.Ticker", side_effect=Exception("API Error")):
        with pytest.raises(RuntimeError) as exc:
            provider.get_historical_prices("CNY=X")
        assert "Error fetching history" in str(exc.value)

def test_get_historical_prices_no_data(provider):
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = pd.DataFrame()

    with patch("yfinance.Ticker", return_value=mock_ticker):
        with pytest.raises(RuntimeError) as exc:
            provider.get_historical_prices("CNY=X")
        # It raises ValueError internally, caught and re-raised as RuntimeError
        assert "Error fetching history" in str(exc.value)
