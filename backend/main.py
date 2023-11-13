from config import OPENWEATHER_API_KEY, LLM_API_KEY
from api.weather import get_weather_data 
from api.llm import construct_prompt, get_generate_summary
from models.summary import Summary
from typing import List
from starlette.responses import HTMLResponse
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.staticfiles import StaticFiles  
from fastapi.templating import Jinja2Templates

import ssl
import os

summaries: List[Summary] = []

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
# app title
app.title = "Weather FastAPI"

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", include_in_schema=False)
async def root():
    template = templates.get_template('home/index.html')
    return HTMLResponse(template.render())

# Function to allow self-signed SSL certificates
def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context
    
# this line is needed if you use self-signed certificate in your scoring service.
allowSelfSignedHttps(True)  

# Weather API endpoint 
@app.get("/weather/{city}", tags=["Weather"])
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
        "temperature": round(weather_data["main"]["temp"],0),
        "description": weather_data["weather"][0]["description"],
        "generation": weather_summary
    }


@app.post("/summaries/", response_model=Summary, tags=["CRUD"]) 
async def create_summary(summary: Summary):
    summaries.append(summary)
    return summary

@app.get("/summaries/", response_model=List[Summary], tags=["CRUD"])
async def read_summaries():
    return summaries

@app.get("/summaries/{summary_id}", response_model=Summary, tags=["CRUD"])
async def read_summary(summary_id: int):
    for summary in summaries:
        if summary.id == summary_id:
            return summary
    raise HTTPException(status_code=404, detail="Summary not found")

@app.put("/summaries/{summary_id}", response_model=Summary, tags=["CRUD"])
async def update_summary(summary_id: int, summary: Summary):
    for index, saved_summary in enumerate(summaries):
        if saved_summary.id == summary_id:
            summaries[index] = summary
            return summary
    raise HTTPException(status_code=404, detail="Summary not found")

@app.delete("/summaries/{summary_id}", tags=["CRUD"])
async def delete_summary(summary_id: int):
    for index, saved_summary in enumerate(summaries):
        if saved_summary.id == summary_id:
            del summaries[index]
            return {"message": "Summary deleted successfully"}
    raise HTTPException(status_code=404, detail="Summary not found")
