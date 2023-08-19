# functions related to reading from AHTx0 device

from globals.const import *

try:
    import adafruit_ahtx0
    import board

except ImportError:
    print("This script requires Adafruit packages to read temperatures, install them with:")
    print("pip install Adafruit_Blinka adafruit-circuitpython-ahtx0")
    exit(1)

except NotImplementedError:
    print("WARNING: This device does not support adafruit libraries")

def get_weather_ahtx0():
    # get current weather reading
    weather = {}

    # poll device for temperature and humidity
    sensor = adafruit_ahtx0.AHTx0(board.I2C())
    
    # make dictionary to return
    weather[WEATHER_READING_TEMPERATURE] = sensor.temperature
    weather[WEATHER_READING_HUMIDITY] = sensor.relative_humidity

    return weather
