# simulated sensor returning random readings

import random

from globals.const import *

TEMP_MIN=16
TEMP_MAX=25

HUMID_MIN=30
HUMID_MAX=60

def get_weather_test():
    # generate a random weather reading

    weather = {}
    
    weather[WEATHER_READING_TEMPERATURE] = random.uniform(TEMP_MIN, TEMP_MAX)
    weather[WEATHER_READING_HUMIDITY] = random.uniform(HUMID_MIN, HUMID_MAX)

    return weather
