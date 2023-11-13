import pytest
from backend.api.llm import construct_prompt, get_generate_summary

@pytest.fixture 
def weather_data():
    return {
        "main": {
            "temp": 25.5  
        },
        "weather": [
            {
                "description": "sunny"
            }
        ]
    }

def test_construct_prompt(weather_data):
    prompt = construct_prompt(weather_data, "London")
    
    assert prompt["input_data"]["input_string"][1]["content"].startswith("In your response, first you must say, Currently the temperature in London:")
    
def test_get_generate_summary(requests_mock, weather_data):

    api_key = "testkey"
    prompt = construct_prompt(weather_data, "London")
    mock_result = "Test summary"
    
    requests_mock.post("https://llama-2-7b-chat.eastus2.inference.ml.azure.com/score", text=mock_result)

    result = get_generate_summary(prompt, api_key)

    assert result == mock_result

def test_get_generate_summary_error(requests_mock, weather_data):

    api_key = "testkey"
    prompt = construct_prompt(weather_data, "London")
    
    requests_mock.post("https://llama-2-7b-chat.eastus2.inference.ml.azure.com/score", status_code=400)

    with pytest.raises(urllib.error.HTTPError) as excinfo:
        get_generate_summary(prompt, api_key)
    
    assert excinfo.value.code == 400