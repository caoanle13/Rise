#! usr/bin/env python3

import time
import json
import urllib.request
from datetime import datetime, timedelta
from timing import Timing
from time import sleep

# sensor setup
from distance_sensor import DistanceSensor
from temperature_sensor import TemperatureSensor
from temperature_sensor import HumiditySensor
temperature_data = []
temperature = TemperatureSensor()
humidity_data = []
humidity = HumiditySensor()
distance = DistanceSensor()
handDetected = False

# mqtt setup
import paho.mqtt.client as mqtt
piTopic = "IC.embedded/tEEEm/TO_PI"
appTopic = "IC.embedded/tEEEm/TO_APP"

# constants on piTopic
SPEECH_TRIGGER = 0
TIME_SET = 1
SUNRISE = 0
AT = 1
ASK_RESULTS = 2

# constants on appTopic
START_ALARM = 0
STOP_ALARM = 1
RESULTS = 2

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
        # read from the topic
        message = json.loads(message.payload.decode())
        # confirms time has been set
        if message['type'] == TIME_SET:
            t = Timing()
            # type 1: 'set alarm at sunrise'
            if message['nature'] == SUNRISE:
                wakeup_datetime = t.sunrise()
            # type 2: 'set alarm at time ___'
            elif message['nature'] == AT:
                message_time = message['time']
                wakeup_datetime = t.timeAt(message_time)
            # confirm time
            print("wake up date time: ", wakeup_datetime)

            while datetime.now() < wakeup_datetime:
                # appending to arrays for chart display
                # temperature data
                temp = temperature.read()
                temperature_data.append(temp)
                # humidity data
                humid = humidty.read()
                humidity_data.append(humid)
                # read every 10 minutes
                sleep(600)

            start_alarm_message = json.dumps({'type': START_ALARM})
            client.publish(appTopic, start_alarm_message)

            #activate distance sensor here
            while not handDetected:
                distance = distance.read()
                if distance < 200:
                    # hand has come within threshold
                    handDetected = True

            stop_alarm_message = json.dumps({'type': STOP_ALARM})
            client.publish(appTopic, stop_alarm_message)

        elif message['type'] == ASK_RESULTS:
            results_message = json.dumps({'type': RESULTS, 'data': temperature_data})
            client.publish(appTopic, results_message)


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
