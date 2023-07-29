import json
import random
import requests
import time
from datetime import datetime, timezone

ENV_PATH=".env"

def read_env_file(path):
    # Get environment variables
    with open(path, 'r') as file:
        env_data = file.read()

    # Split the data by lines and extract the key-value pairs
    env_vars = {}
    for line in env_data.splitlines():
        key, value = line.strip().split('=', 1)
        env_vars[key] = value

    return env_vars

def get_weather():
    # Get current weather
    current_utc_timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    print(current_utc_timestamp)

    weather = {
        'datetime': current_utc_timestamp,
        'temperature': random.uniform(20,39),
        'humidity': random.uniform(0.7,0.9)
    }

    return weather

def update(env_vars):
    # Get current time and send it to server
    weather_entry = get_weather()

    # Prepare request
    json_data = json.dumps(weather_entry)
    headers = {
        "Content-Type": "application/json"
    }

    # POST it to the server
    url = env_vars.get("SERVER_URL") + ":" + env_vars.get("SERVER_PORT") + "/weather"
    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:
        print("POST request successful!")
        print("Response:", response.json())
    else:
        print("POST request failed! Status Code:", response.status_code)
        print("Error message:", response.text)

# Set up application
env_vars = read_env_file(ENV_PATH)

# Start update loop
while True:
    update(env_vars)
    time.sleep(float(env_vars.get("UPDATE_INTERVAL")))
