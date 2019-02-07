#! usr/bin/env python3

import time
import json
import paho.mqtt.client as mqtt
from distance_sensor import DistanceSensor
import urllib.request
from datetime import datetime, timedelta

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
                


def sunrise():
    with urllib.request.urlopen("https://api.sunrise-sunset.org/json?lat=51.508530&lng=-0.076132&date=tomorrow") as r:
        response = r.read()
    sunrise = json.loads(response.decode())['results']['sunrise'].split(' ')[0]
    [sunrise_h, sunrise_m, sunrise_s] = [int(x) for x in sunrise.split(':')]
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.replace(hour=sunrise_h, minute=sunrise_m, second=sunrise_s)

def timeAt(message_time):
    wakeup_date, wakeup_time, ignore = message_time.split(' ')
    year, month, day = wakeup_date.split('-')
    hour, minute, second = wakeup_time.split(':')
    return datetime.now().replace(year=year, month=month, day=day,
                                  hour=hour, minute=minute, second=second)
    

client.on_message = on_message

client.loop_forever()
