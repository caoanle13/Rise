#! usr/bin/env python3

import time
import json
import paho.mqtt.client as mqtt

TIME_SET = 1
SUNRISE = 0
AT = 1

piTopic = "IC.embedded/tEEm/TO_PI"

# connecting to mqtt

client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
client.connect("test.mosquitto.org",port=1883)
print("connection success")
client.subscribe(piTopic)


# print time of START_ALARM

def on_message(client, userdata, message):
    # check the topic
    if message.topic == piTopic

        x = json.loads(message.payload)
        command = x['type']

        # check TIME_SET
        if command == TIME_SET:
            # check type of input
            nature = x['nature']
            # nature 1: SUNRISE
            if nature == SUNRISE:

            # type 2: AT
            elif nature == AT:
            # access nature
            # access time
            # decode
            # play with string
            # datetime python obj

def sunrise(x):
    # process data if nature = SUNRISE

def atTime(x):
    # process data if nature = AT

client.on_message = on_message

client.loop_forever()
