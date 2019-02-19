import busio
import board
import adafruit_si7021
from datetime import datetime

# Classes to read from Temperature and Humidity sensors

class TemperatureSensor:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_si7021.SI7021(i2c)

    def read(self):
        # the sensor temperature in degrees celsius
        # round to 2dp
        temp = round(self.sensor.temperature,2)
        return temp

class HumiditySensor:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_si7021.SI7021(i2c)

    def read(self):
        # the percentage humidity as a value from 0 to 100%
        # round to 2dp
        humid = round(self.sensor.relative_humidity,2)
        return humid


if __name__ == "__main__":

    temperature_sensor = TemperatureSensor()
    print(temperature_sensor.read())

    humidity_sensor = HumiditySensor()
    print(humidity_sensor.read())

