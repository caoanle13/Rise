#! usr/bin/env python3

import time
import json
import paho.mqtt.client as mqtt
from distance_sensor import DistanceSensor
import urllib.request
from datetime import datetime, timedelta
from timing import Timing as t

#CONSTANTS
TIME_SET = 1
SUNRISE = 0
AT = 1

# STATES
readDistance = False

piTopic = "IC.embedded/tEEm/TO_PI"

client = mqtt.Client()
#client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
client.connect("test.mosquitto.org",port=1883)
client.subscribe(piTopic)

def on_message(client, userdata, message):
    # check the topic
    if message.topic == piTopic:

        message = json.loads(message.payload.decode())
        # check TIME_SET
        if message['type'] == TIME_SET:

            if message['nature'] == SUNRISE:
                wakeup_datetime = sunrise()

            elif message['nature'] == AT:
                message_time = message['time']
                wakeup_datetime = timeAt(message_time)
                

    

client.on_message = on_message

client.loop_forever()
