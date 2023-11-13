import pytest
from fastapi.testclient import TestClient
import httpx

from main import app 

# Fixtures

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def httpx_client():
    return httpx.Client()

# Tests  

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    
def test_weather_missing_key(client):
    response = client.get("/weather/London")
    assert response.status_code == 500

    
@pytest.mark.httpx(httpx_client)
def test_weather_success(httpx_client, monkeypatch):

    api_keys = {"OPENWEATHER_API_KEY": "foo", "LLM_API_KEY": "bar"}

    monkeypatch.setattr(app, "OPENWEATHER_API_KEY", api_keys["OPENWEATHER_API_KEY"])
    monkeypatch.setattr(app, "LLM_API_KEY", api_keys["LLM_API_KEY"])

    response = client.get("/weather/London")  
    assert response.status_code == 200


def test_create_summary(client):
    response = client.post("/summaries/", json={"id": 1, "text":"example"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "text": "example"}

    
def test_read_summaries(client):
    response = client.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == []

    
def test_read_summary_not_found(client):
    response = client.get("/summaries/1") 
    assert response.status_code == 404


def test_update_summary(client):
    client.post("/summaries/", json={"id": 1, "text": "example"})
    response = client.put("/summaries/1", json={"id": 1, "text": "updated"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "text": "updated"}


def test_delete_summary(client):
    client.post("/summaries/", json={"id": 1, "text": "example"})
    response = client.delete("/summaries/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Summary deleted successfully"}