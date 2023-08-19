# environment variable functions

import os

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

def read_env_file(path):
    # get environment variables
    env_data = None
    
    # env file resides in parent directory
    script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(script_directory, path)

    with open(full_path, 'r') as file:
        env_data = file.read()

    if env_data == None:
        print("No .env file present with necessary parameters")
        exit()

    # split the data by lines and extract the key-value pairs
    env_vars = {}
    for line in env_data.splitlines():
        key, value = line.strip().split('=', 1)
        env_vars[key] = value

    return env_vars