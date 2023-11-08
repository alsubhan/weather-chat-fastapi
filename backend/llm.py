import json
import urllib.request

def construct_prompt(weather_data, city):
  temp = round(weather_data['main']['temp'],0)
  desc = weather_data['weather'][0]['description']

  # Construct prompt for LLM 
  DEFAULT_SYSTEM_PROMPT = """\\ 
  You are a helpful, respectful and honest weather assistant. 
  Always answer as helpfully as possible, while being safe. 
  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
  Please ensure that your responses are socially unbiased and positive in nature. 
  If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. 
  If you don't know the answer to a question, please don't share false information."""

  DEFAULT_USER_PROMPT = f"In your response, first you must say, Currently the temperature in {city}: {temp} celsius with {desc}, provide amusing summary of the weather and then suggest the activites and outfit"
  
  prompt = {
      "input_data": {
          "input_string": [
              {"role": "user", "content": DEFAULT_SYSTEM_PROMPT}, 
              {"role": "user", "content": DEFAULT_USER_PROMPT}
          ],
          "parameters": {
              "temperature": 0.6, 
              "top_p": 0.9,
              "do_sample": True,
              "max_new_tokens": 1000
          }
      }
  }
  return prompt
    

def get_generate_summary(prompt, api_key):
    # Call LLM API 
    body = str.encode(json.dumps(prompt))
    url = 'https://llama-2-7b-chat.eastus2.inference.ml.azure.com/score'

    # Set headers
    headers = {'Content-Type':'application/json', 
                'Authorization':('Bearer '+ api_key),
                'azureml-model-deployment': 'llama-2-7b-chat'
                }
  

    # Make request
    req = urllib.request.Request(url, body, headers)
    
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(result)
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
