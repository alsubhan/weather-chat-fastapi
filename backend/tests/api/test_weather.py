import pytest
import requests
from backend.api.weather import get_weather_data

def test_get_weather_data(monkeypatch):

    # Mock response from requests.get
    mock_response = requests.models.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"temp": 25.5}'
    monkeypatch.setattr(requests, "get", lambda url: mock_response)

    result = get_weather_data("London", "dummykey")

    assert result["temp"] == 25.5

def test_get_weather_data_error(monkeypatch):

    # Make requests.get raise an exception
    monkeypatch.setattr(requests, "get", lambda url: Exception("Network error"))

    with pytest.raises(Exception) as excinfo:
        get_weather_data("London", "dummykey")
    
    assert "Error getting weather data" in str(excinfo.value)