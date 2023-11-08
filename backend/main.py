from config import OPENWEATHER_API_KEY, LLM_API_KEY
from weather import get_weather_data 
from llm import construct_prompt, get_generate_summary
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
import ssl
import os

# Create FastAPI app instance 
app = FastAPI()  

# Enable CORS on all routes
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to allow self-signed SSL certificates
def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context
    
# this line is needed if you use self-signed certificate in your scoring service.
allowSelfSignedHttps(True)  

# Weather API endpoint 
@app.get("/weather/{city}")
async def get_weather(city: str):

    if not OPENWEATHER_API_KEY:
        raise Exception("A key should be provided to invoke the endpoint.")
    # Call weather data from OpenWeatherMap
    weather_data = get_weather_data(city, OPENWEATHER_API_KEY)

    if not LLM_API_KEY:
        raise Exception("A key should be provided to invoke the endpoint.")
    # Call LLM API
    prompt = construct_prompt(weather_data, city)
    weather_summary = get_generate_summary(prompt, LLM_API_KEY)
        
    return {
        "temperature": weather_data["main"]["temp"],
        "description": weather_data["weather"][0]["description"],
        "generation": weather_summary
    }