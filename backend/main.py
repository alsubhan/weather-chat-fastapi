from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
import requests
import urllib.request
import json
import os
import ssl

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.


@app.get("/weather/{city}")
async def get_weather(city: str):
    
    api_key = "2702cf74634b8ad3ed73ae91e1f2fa52"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as ex:
        return {"error": str(ex)}
        
    data = response.json()
    
    DEFAULT_SYSTEM_PROMPT = """\
        You are a helpful, respectful and honest weather assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""
    DEFAULT_USER_PROMPT = f"In your response, first say, Currently the temperature in {city}: {data['main']['temp']} celsius with {data['weather'][0]['description']}, provide amusing summary of the weather and then suggest the activites and outfit"

    prompt = {
        "input_data": {
            "input_string": [
                {
                    "role": "user",
                    "content": DEFAULT_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": DEFAULT_USER_PROMPT
                }
            ],
            "parameters": {
                                "temperature": 0.6,
                                "top_p": 0.9,
                                "do_sample": True,
                                "max_new_tokens": 1000
                            }
                }
             }

    body = str.encode(json.dumps(prompt))
    url = 'https://llama-2-7b-chat.eastus2.inference.ml.azure.com/score'
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key2 = 'mNXqOYDyxGrTYsCdL4kDbRQeHpcVDqUF'

    if not api_key2:
        raise Exception("A key should be provided to invoke the endpoint")

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key2), 'azureml-model-deployment': 'llama-2-7b-chat-14' }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

    return {
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "generation": result
    }