#! usr/bin/env python3

import time
import json
import urllib.request

from datetime import datetime, timedelta
from timing import Timing
from time import sleep
from weather import Weather

import threading

# LED setup
from led import LED
led = LED(1000, 1000, 1000, 100, 100, 100)

# sensor setup
# distance
from distance_sensor import DistanceSensor
distance = DistanceSensor()
handDetected = False

# temperature
from temperature_sensor import TemperatureSensor
temperature_data = [1, 2, 3]
temperature = TemperatureSensor()

# humidity
from temperature_sensor import HumiditySensor
humidity_data = [3, 2, 1]
humidity = HumiditySensor()

# Timing set up
time_data=['0', '1', '2']
t = Timing()


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
SPEAK = 3

# constants on both topics
TEMPERATURE = 0
HUMIDITY = 1

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

        # time has been set
        if message['type'] == TIME_SET:

            # type 1: 'set alarm at sunrise'
            if message['nature'] == SUNRISE:
                wakeup_datetime = t.sunrise()
                                
            # type 2: 'set alarm at time ___'
            elif message['nature'] == AT:
                message_time = message['time']
                wakeup_datetime = t.timeAt(message_time)

            # confirm time
            print("wake up date time: ", wakeup_datetime)

            # while user is sleeping, i.e. alarm hasn't gone off yet
            # monitor temperature and humidity of room
            while datetime.now() < wakeup_datetime:
                # appending to arrays for chart display
                # temperature data
                temp = temperature.read()
                temperature_data.append(temp)
                # humidity data
                humid = humidty.read()
                humidity_data.append(humid)
                # time of each reading
                curr_time = t.currentTime()
                time_data.append(curr_time)
                # read every 10 minutes
                sleep(0.5)


            # time to wake up!
            start_alarm_message = json.dumps({'type': START_ALARM})
            client.publish(appTopic, start_alarm_message)

            # activate distance sensor to check for user's hand  
            while not handDetected:
                distance = distance.read()
                if distance < 200:
                    # hand has come within threshold
                    # turn alarm off
                    stop_alarm_message = json.dumps({'type': STOP_ALARM})
                    client.publish(appTopic, stop_alarm_message)
                    handDetected = True

            # greet user and give weather info
            w = Weather()
            client.publish(appTopic, json.dumps({'type': SPEAK, 'say': 'Good Morning! The current weather state is ' + w.description + ' and it is ' + str(w.temperature) + 'degrees Celsius.'}))

        elif message['type'] == ASK_RESULTS:
            # add all temperature sensor data to a dictionary
            # monitors room overnight and then displays graphically on web page
            # check if there is any data first
            if len(temperature_data) == 0 or len(humidity_data) == 0:
                client.publish(appTopic, json.dumps({'type': SPEAK, 'say': 'There is currently no data for your night.'}))
            else:
                # if user asked for temperature data
                if message['data_for'] == TEMPERATURE:
                    data =  {
                        'type': RESULTS,
                        'data_for': TEMPERATURE,
                        'temp_data': temperature_data,    # array of ints
                        'time': time_data                 # array strings: hh:mm
                    }
                    client.publish(appTopic, json.dumps({'type': SPEAK, 'say': 'Here is your temperature data.'}))
                # else if user asked for humidity data
                elif message['data_for'] == HUMIDITY:
                    data =  {
                        'type': RESULTS,
                        'data_for': HUMIDITY,
                        'humid_data': humidity_data,      # array of ints
                        'time': time_data                 # array strings: hh:mm
                    }
                    client.publish(appTopic, json.dumps({'type': SPEAK, 'say': 'Here is your humidity data.'}))
                client.publish(appTopic, json.dumps(data))


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
