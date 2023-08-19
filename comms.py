# functions to communicate with weather-server

import json
import requests

from urllib.parse import urljoin

from globals.env import *
from globals.const import *

def get_server_url(env_vars, endpoint):
    # get url to send readings to
    url = urljoin(
        base=f"{env_vars.get(ENV_SERVER_URL)}:{env_vars.get(ENV_SERVER_PORT)}",
        url=endpoint
        )

    return url

def submit_readings_to_server(env_vars, weather_readings):
    # send the current cache of readings to the server

    device_id = env_vars.get(ENV_CLIENT_DEVICEID)
    location_id = env_vars.get(ENV_CLIENT_LOCATIONID)

    # map readings into payload format
    payload_data_measurements = [
        {
            "dateTime": weather_reading[WEATHER_READING_TIMEUTC].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "humidity": weather_reading[WEATHER_READING_HUMIDITY],
            "temperature": weather_reading[WEATHER_READING_TEMPERATURE],
        }
        for weather_reading in weather_readings
    ]

    # build main payload
    payload_data = {
        "deviceId": device_id,
        "locationId": location_id,
        "measurements": payload_data_measurements
    }

    # prepare request
    payload_json = json.dumps(payload_data)
    headers = {
        "Content-Type": "application/json",
        "x-api-key": env_vars.get("SERVER_APIKEY")
    }

    # get URL to send message to
    url = get_server_url(env_vars, "weather")
    readings_count = len(weather_readings)
    print(f"Submitting {readings_count} reading{'s' if readings_count != 1 else ''} to {url}...")

    try:
        # post request to the server
        response = requests.post(url, data=payload_json, headers=headers)

        # raise an error for any bad non-successful HTTP status
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        # connection error
        print("ConnectionError: Could not establish a connection.")
        return False

    except requests.exceptions.HTTPError as http_err:
        # bad HTTP status code
        print("HTTPError:", http_err)
        return False

    except Exception as e:
        # some other error
        print("An error occurred:", e)
        return False
    
    # submitted successfully
    print("Response OK:", response.json().get("message"))
    return True
