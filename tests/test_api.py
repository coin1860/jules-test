from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from backend.app.main import app

client = TestClient(app)

# We need to ensure engine is mocked for these tests,
# as the startup event might not run or might try to connect to real API if not mocked.

def test_status_endpoint_no_engine():
    # Force engine to be None
    with patch("backend.app.main.engine", None):
        response = client.get("/status")
        assert response.status_code == 503

def test_status_endpoint_success():
    mock_engine = MagicMock()
    mock_engine.get_status.return_value = {"running": True}
    with patch("backend.app.main.engine", mock_engine):
        response = client.get("/status")
        assert response.status_code == 200
        assert response.json() == {"running": True}

def test_start_endpoint():
    mock_engine = MagicMock()
    with patch("backend.app.main.engine", mock_engine):
        response = client.post("/start")
        assert response.status_code == 200
        mock_engine.start.assert_called()

def test_stop_endpoint():
    mock_engine = MagicMock()
    with patch("backend.app.main.engine", mock_engine):
        response = client.post("/stop")
        assert response.status_code == 200
        mock_engine.stop.assert_called()

def test_config_endpoint():
    mock_engine = MagicMock()
    with patch("backend.app.main.engine", mock_engine):
        response = client.post("/config", json={"short_window": 10, "long_window": 30})
        assert response.status_code == 200
        mock_engine.update_strategy_parameters.assert_called_with(10, 30)

def test_config_endpoint_invalid():
    mock_engine = MagicMock()
    mock_engine.update_strategy_parameters.side_effect = ValueError("Invalid")
    with patch("backend.app.main.engine", mock_engine):
        response = client.post("/config", json={"short_window": -1, "long_window": 30})
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid"

def test_history_endpoint():
    mock_engine = MagicMock()
    mock_engine.account.get_history.return_value = [{"id": 1}]
    with patch("backend.app.main.engine", mock_engine):
        response = client.get("/history")
        assert response.status_code == 200
        assert response.json() == [{"id": 1}]
