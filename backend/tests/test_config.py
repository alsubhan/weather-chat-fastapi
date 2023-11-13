import os
from dotenv import load_dotenv
import pytest

def test_load_api_keys(monkeypatch):
    # Mock os.getenv to return fake keys
    monkeypatch.setattr(os, "getenv", lambda x: "fakekey")
    
    load_dotenv()

    assert OPENWEATHER_API_KEY == "fakekey"
    assert LLM_API_KEY == "fakekey"
    
def test_load_api_keys_missing(monkeypatch):
    # Make os.getenv return None
    monkeypatch.setattr(os, "getenv", lambda x: None)
    
    with pytest.raises(Exception) as excinfo:
        load_dotenv()
    
    assert "key should be provided" in str(excinfo.value)