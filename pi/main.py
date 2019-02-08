#! usr/bin/env python3

import time
import json
import paho.mqtt.client as mqtt
#from distance_sensor import DistanceSensor
import urllib.request
from datetime import datetime, timedelta
from timing import Timing

#CONSTANTS
TIME_SET = 1
SUNRISE = 0
AT = 1

piTopic = "IC.embedded/tEEEm/TO_PI"

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print('connected OK')
        client.connected_flag=True
        client.subscribe(piTopic)
    else:
        print('Bad connection, returned code=', rc)
        client.bad_connection_flag=True

def on_message(client, userdata, message):
    # check the topic
    if message.topic == piTopic:

        message = json.loads(message.payload.decode())
        
        if message['type'] == TIME_SET:
            t = Timing()
            
            if message['nature'] == SUNRISE:
                wakeup_datetime = t.sunrise()

            elif message['nature'] == AT:
                message_time = message['time']
                wakeup_datetime = t.timeAt(message_time)
            
            print("wake up date time: ", wakeup_datetime)


mqtt.Client.connected_flag = False
mqtt.Client.bad_connection_flag = False
client = mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message

print('Connecting to broker')
try:
    client.connect("test.mosquitto.org",port=1883)
except:
    print('connection failed!')

# while not client.connected_flag and not client.bad_connection_flag:
#     print('in wait loop')
#     time.sleep(1)
# if client.bad_connection_flag:
#     client.loop_stop()
#     sys.exit()
# print('in Main loop')

client.loop_forever()
