import requests

def get_weather_data(city, api_key):
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

  try:
    response = requests.get(url)
    response.raise_for_status()
  except Exception as ex:
    print(f"Error getting weather data: {ex}")
    raise
  
  return response.json()