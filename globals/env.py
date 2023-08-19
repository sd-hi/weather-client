# environment variable functions

import os

from globals.const import *

# supported environment variables
ENV_SERVER_URL="SERVER_URL" # base URL of server to send readings to
ENV_SERVER_PORT="SERVER_PORT" # port of server to send readings to
ENV_SERVER_APIKEY="SERVER_APIKEY" # api key for the server

ENV_CLIENT_DEVICEID="CLIENT_DEVICEID" # unique identifier for this device
ENV_CLIENT_LOCATIONID="CLIENT_LOCATIONID" # unique identifier for the location of this device

ENV_POLL_INTERVAL="POLL_INTERVAL" # how often (in seconds) we should poll for a weather reading
ENV_SUBMIT_INTERVAL="SUBMIT_INTERVAL" # how often (in seconds) we should post our readings to the server
ENV_SENSOR_TYPE="SENSOR_TYPE" # the type of this sensor

# validation constants for evironment variables
SUPPORTED_SENSOR_TYPES=["AHTx0","TEST"] # supported sensor types

class ValidationError(Exception):
    # exception class for validation erorrs
    pass

def validate_environment_variables(env_vars):
    # validate environment variables

    if env_vars[ENV_SERVER_URL] == "":
        raise ValidationError("URL missing")

    if env_vars[ENV_SERVER_APIKEY] == "":
        raise ValidationError("API key missing")

    if env_vars[ENV_CLIENT_DEVICEID] == "":
        raise ValidationError("Device ID not specified")
    
    if env_vars[ENV_CLIENT_LOCATIONID] == "":
        raise ValidationError("Location ID not specified")
       
    try:
        poll_interval = float(env_vars[ENV_POLL_INTERVAL])
    except:
        raise ValidationError("Poll interval must be a number in seconds")
    if poll_interval <= 0:
        raise ValidationError("Poll interval not set")
    
    try:
        submit_interval = float(env_vars[ENV_SUBMIT_INTERVAL])
    except:
        raise ValidationError("Submit interval must be a number in seconds")
    if submit_interval <= 0:
        raise ValidationError("Submit interval not set")
    
    if env_vars[ENV_SENSOR_TYPE] not in SUPPORTED_SENSOR_TYPES:
        raise ValidationError(f"Sensor type '{env_vars[ENV_SENSOR_TYPE]}' is not supported, expected one of {SUPPORTED_SENSOR_TYPES}")

    return True
        

def read_environment_variables(path):
    # get environment variables
    env_data = None
    
    # env file resides in parent directory
    script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(script_directory, path)

    with open(full_path, 'r') as file:
        env_data = file.read()

    if env_data == None:
        print("No .env file present with necessary parameters")
        exit(1)

    # split the data by lines and extract the key-value pairs
    env_vars = {}
    for line in env_data.splitlines():
        key, value = line.strip().split('=', 1)
        env_vars[key] = value

    # validate the environment variables
    try:
        validate_environment_variables(env_vars)
    except ValidationError as error:
        print(f"{path} settings incorrect. {error}")
        exit(1)

    return env_vars