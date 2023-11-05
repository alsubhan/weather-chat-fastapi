from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import requests
from transformers import pipeline
from database import Session, Engine, Recommendation, get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database session
def get_db_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# HuggingFace for funny weather  
generator = pipeline('text-generation', model='distilgpt2')

@app.get("/weather/{city}")
async def get_weather(city: str, db: Session = Depends(get_db_session)):
    api_key = "weather_api_key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    response = requests.get(url)
    data = response.json()

    prompt = f"Provide a funny description of the weather in {city} based on: {data['weather'][0]['description']} "
    synopsis = generator(prompt)[0]["generated_text"]
    
    return {
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "funny_synopsis": synopsis
    }

# Recommendations CRUD
@app.post("/recommendations", response_model=Recommendation) 
def create_recommendation(rec: Recommendation, db: Session = Depends(get_db_session)):
    db_rec = store_in_db(db, rec)
    return db_rec

@app.get("/recommendations", response_model=list[Recommendation])
def get_recommendations(db: Session = Depends(get_db_session)):
    recs = load_recommendations_from_db(db)
    return recs

@app.put("/recommendations/{id}")
def update_recommendation(id: int, rec: Recommendation, db: Session = Depends(get_db_session)):
    updated = update_in_db(db, id, rec)
    return updated

@app.delete("/recommendations/{id}")
def delete_recommendation(id: int, db: Session = Depends(get_db_session)):
    deleted = delete_from_db(db, id)
    return {"deleted": deleted}