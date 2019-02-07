#!/usr/bin/env python3

import busio
import board
import adafruit_vl53l0x
import json
import time
import paho.mqtt.client as mqtt

# constant declarations
SLEEP_TRIGGER = 0   # when the user goes to bed
START_ALARM = 1     # start the alarm
AWAKE = 0           # stop the alarm

# connecting
client = mqtt.Client()
#client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
client.connect("test.mosquitto.org",port=1883)
print("connection success")
client.subscribe("IC.embedded/tEEm/UI_COMMAND")

# setup for using the sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)

def on_message(client, userdata, message):
    # check the topic
    print("check for topic")
    print(message.topic)
    if message.topic == 'IC.embedded/tEEm/UI_COMMAND':
        print(message.payload.decode())
        input = json.loads(message.payload.decode())
        value = input['type']
        # start measuring
        if value == START_ALARM:
            while True:
                print('start measuring')
                if sensor.range < 200:
                        # turn off alarm gesture recognised
                        data = json.dumps({'type': AWAKE})
                        client.publish("IC.embedded/tEEm/UI_FEEDBACK", data)
                        print('stop measuring')
                        # stop measuring
                        break
            time.sleep(1.0)

client.on_message = on_message

client.loop_forever()
