# weather-client
# polls data from temperature sensor and POSTs readings to server

# standard packages
import time
from datetime import datetime, timezone

from comms import submit_readings_to_server
from globals.env import *
from globals.const import *
from sensors.ahtx0 import get_weather_ahtx0
from sensors.test import get_weather_test

ENV_PATH=".env" # path to environment variable file

def get_weather_reading(env_vars):
    # obtain a weather reading from the configured device
    
    sensor_type = env_vars.get("SENSOR_TYPE")
    if sensor_type == "AHTx0":
        # pull weather reading from AHTx0 sensor
        weather_reading = get_weather_ahtx0()
    
    elif sensor_type == "TEST":
        # simulate a sensor with random numbers
        weather_reading = get_weather_test()

    else:
        print(f"Sensor type '{sensor_type}' is not supported, expected one of {SUPPORTED_SENSOR_TYPES}")
        exit(1)

    # set time on the reading
    weather_reading[WEATHER_READING_TIMEUTC] = datetime.now(timezone.utc)

    return weather_reading 

def main():
    weather_readings = [] # cache of collected weather readings
    time_last_submitted = None # the last time readings were submitted
    
    # Set up application
    env_vars = read_env_file(ENV_PATH)

    # Announce start
    poll_interval = float(env_vars.get(ENV_POLL_INTERVAL))
    submit_interval = float(env_vars.get(ENV_SUBMIT_INTERVAL))
    device_id = env_vars.get(ENV_CLIENT_DEVICEID)
    url = env_vars.get(ENV_SERVER_URL) + ":" + env_vars.get(ENV_SERVER_PORT) + "/weather"
    print(f"Sensor device '{device_id}' started (polling every {poll_interval} seconds)...")
    print(url)

    # Start update loop
    while True:

        # get current weather reading and add it to the cache
        weather_reading = get_weather_reading(env_vars)
        print(f"Time: {weather_reading[WEATHER_READING_TIMEUTC]}\tTemp: {weather_reading[WEATHER_READING_TEMPERATURE]}\tHumid: {weather_reading[WEATHER_READING_HUMIDITY]}")
        weather_readings.append(weather_reading)

        time_current = datetime.now()
        submit_now = False
        if not time_last_submitted:
            # submit first reading to server as a test
            submit_now = True
            
        elif (time_current - time_last_submitted).seconds > submit_interval:
            # enough time has passed that we should submit to server now
            submit_now = True

        if submit_now:
            if submit_readings_to_server(env_vars,weather_readings):
                # submission was successful, readings cache can be reset
                weather_readings = []

            # always reset time last submitted, to avoid spamming server with request on failure
            time_last_submitted = time_current

        # sleep until time to take next reading
        time.sleep(poll_interval)

if __name__ == "__main__":
    main()