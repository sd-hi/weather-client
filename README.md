# weather-client
This application monitors the temperature and humidity of a DHT20 sensor connected to a Raspberry Pi, and regularly relays the data to an instance of the `weather-server`

This client HTTP POSTs data to the weather server for storage and display.
# Prerequisites
## Weather server
First set up an instance of `weather-server` to serve as the receiver and database for the collected temperature information.
*See https://github.com/sd-hi/weather-server for more information.*
## Weather clients
For each instance of the client you want to set up, you will need:
- Raspberry Pi with [Raspberry Pi OS](https://www.raspberrypi.com/software/) installed (this documentation uses a Raspberry Pi 3B v1.2)
- [DHT20 Temperature sensor](https://www.adafruit.com/product/5183))
- [4x female-female jumper wires](https://www.adafruit.com/product/1951)
# Wiring
![Pasted image 20230824200948](https://github.com/sd-hi/weather-client/assets/96883126/78854679-588b-4c22-9582-4867e840bc4b)
Connect the DHT20 temperature sensor to the relevant Raspberry Pi pins:
1. Pi 2 - 5V
2. Pi 3 - GPIO2
3. Pi 9 - GND
4. Pi 5 - GPIO3

For guidance on the pin numbering on your device, use command
```bash
pinout
```
To see a diagram (more info can be seen in the [GPIO Zero documentation](https://gpiozero.readthedocs.io/en/stable/cli_tools.html))
# Setup
## Set correct timezone
For data consistency between sensors, set the timezone on the Raspberry Pi consistent with its location. For reference, the temperatures are sent to the server in [UTC](https://en.wikipedia.org/wiki/Coordinated_Universal_Time).
The following command will set the device to the New York timezone.
```bash
sudo timedatectl set-timezone America/New_York
```
To see a full list of timezones, use command `timedatectl list-timezones`. This can be filtered with `grep`, for example `timedatectl list-timezones | grep "America"`
## Enable I2C on Pi
For the Raspberry Pi to read data via the pins, it is necessary to enable I2C interface on the device, this can be by altering the `/boot/config.txt file`:
```bash
sudo nano /boot/config.txt
```
Uncomment the following line by removing the preceding `#`
```
dtparam=i2c_arm=on
```
A reboot is required for this setting to take effect
```bash
sudo reboot
```
## Install Python prerequisites
For Python to interact and read data from the DHT20 sensor, install the supporting Adafruit packages for AHTx0 sensors:
```bash
python3 -m pip install Adafruit_Blinka adafruit-circuitpython-ahtx0
```
## Clone repository
Download the `weather-client` script into the device's home directory:
```bash
cd ~
git clone https://github.com/sd-hi/weather-client.git
```
This creates a `~/weather-client` directory
## Set environment variables
Create the `.env` file by copying the `.env.example` file:
```bash
cd weather-client
cp .env.example .env
nano .env
```
Set the appropriate environment variables:
-`CLIENT_DEVICEID` - A unique ID for this device, for instance `sensor1`
- `CLIENT_LOCATIONID` - A unique ID to signify this device's location e.g. `bedroom1`
- `SERVER_URL` - The URL for the `weather-server` instance
- `SERVER_PORT` - Port the `weather-server` is exposed on
- `SERVER_APIKEY` - API key for the `weather-server` instance (consistent with its `API_KEY` environment variable)
- `POLL_INTERVAL` - How often (in seconds) a temperature reading should be taken
- `SENSOR_TYPE` - Sensor type
	- Leave as `AHTx0` to read from DHT20 sensor
	- Setting to `TEST` will avoid reading from the sensor and will feed temperature and humidity values for testing purposes
- `SUBMIT_INTERVAL` - How often (in seconds) the server should submit collected readings
### Caching of readings
If the device loses network connectivity, it will continue to collect readings every `POLL_INTERVAL` seconds. When connection is restored all cached readings will be submitted in a single payload. Loss of power to the device will lose any cached readings not yet submitted to the `weather-server`.
## Add weather client to boot
Creating a service ensures that temperatures will continue to be collected and submitted following device reboot, without intervention from the user.
### Create service
Create a `weather-client.service` service to be run by systemd
```bash
sudo nano /etc/systemd/system/weather-client.service
```
Use the following, assuming weather client is in `/home/pi/weather-client/` folder
```bash
[Unit]
Description=weather-client Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/weather-client
ExecStartPre=/bin/sleep 10
ExecStart=/usr/bin/python3 /home/pi/weather-client/weather-client.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Refresh systemd and enable the service
```bash
sudo systemctl enable weather-client.service
sudo systemctl daemon-reload
sudo systemctl start weather-client.service
```
Upon start of the service, the device should begin to submit readings to the `weather-server`!
### Controlling the service
If you need to stop service, use
```bash
sudo systemctl stop weather-client.service
```
To check status of service run
```bash
sudo systemctl status weather-client.service
```
To get log of service run
```bash
sudo journalctl -u weather-client.service
```
