import busio
import board
import adafruit_vl53l0x

class DistanceSensor:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(i2c)

    def read(self):
        return self.sensor.range


if __name__ == "__main__":

    distance_sensor = DistanceSensor()
    print(distance_sensor.read())
