import smbus

class TemperatureSensor:

    bus = smbus.SMBus(1)
    address = 0x40

    def read(self):
        bus.writebyte(address, 0xf3)  
        data = bus.read_i2c_block_data(address, 0xe2, 2)
        raw = int.from_bytes(data,'big')
        return ((175.72*raw)/65536)-46.85

if __name__ == "__main__":

    temperature_sensor = TemperatureSensor()
    print(temperature_sensor.read())
