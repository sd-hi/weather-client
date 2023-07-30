import adafruit_ahtx0
import board
import json
import os
import random
import requests
import time
from datetime import datetime, timezone

ENV_PATH=".env"

def read_env_file(path):
    # Get environment variables
    env_data = None
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_directory, path)

    with open(full_path, 'r') as file:
        env_data = file.read()

    if env_data == None:
        print("No .env file present with necessary parameters")
        exit()

    # Split the data by lines and extract the key-value pairs
    env_vars = {}
    for line in env_data.splitlines():
        key, value = line.strip().split('=', 1)
        env_vars[key] = value

    return env_vars

def get_weather():
    # Get current weather
    
    # Poll device for temperature and humidity
    sensor = adafruit_ahtx0.AHTx0(board.I2C())

    # Prepare data
    sensor_id = env_vars.get("CLIENT_SENSORID")
    location_id = env_vars.get("CLIENT_LOCATIONID")
    current_utc_timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    temperature = sensor.temperature
    humidity = sensor.relative_humidity

    print(f"{current_utc_timestamp}\tTemp: {temperature}\tHumid: {humidity}")

    weather = {
        'deviceId': sensor_id,
        'locationId': location_id,
        'dateTime': current_utc_timestamp,
        'temperature': temperature,
        'humidity': humidity
    }
    print(weather)

    return weather

def update(env_vars):
    # Get current time and send it to server
    weather_entry = get_weather()

    # Prepare request
    json_data = json.dumps(weather_entry)
    headers = {
        "Content-Type": "application/json",
        "x-api-key": env_vars.get("SERVER_APIKEY")
    }

    # POST it to the server
    url = env_vars.get("SERVER_URL") + ":" + env_vars.get("SERVER_PORT") + "/weather"
    response = requests.post(url, data=json_data, headers=headers)

    # Handle the response
    if response.status_code == 200:
        print("Response OK:", response.json())
    else:
        print("POST request failed! Status Code:", response.status_code)
        print("Error message:", response.text)

# Set up application
env_vars = read_env_file(ENV_PATH)

# Announce start
update_interval = float(env_vars.get("UPDATE_INTERVAL"))
sensor_id = env_vars.get("CLIENT_SENSORID")
url = env_vars.get("SERVER_URL") + ":" + env_vars.get("SERVER_PORT") + "/weather"
print(f"Sensor '{sensor_id}' started (interval {update_interval} seconds)...")
print(url)

# Start update loop
while True:
    update(env_vars)
    time.sleep(update_interval)
