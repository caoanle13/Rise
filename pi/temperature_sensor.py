import busio
import board
import adafruit_si7021

class TemperatureSensor:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_si7021.SI7021(i2c)

    def read(self):
        # the sensor temperature in degrees celsius
        temp = self.sensor.temperature
        return temp

class HumiditySensor:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_si7021.SI7021(i2c)

    def read(self):
        # the percentage humidity as a value from 0 to 100%
        humid = self.sensor.relative_humidity
        return humid

if __name__ == "__main__":

    temperature_sensor = TemperatureSensor()
    print(temperature_sensor.read())

    humidity_sensor = HumiditySensor()
    print(humidity_sensor.read())
