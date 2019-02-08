import paho.mqtt.client as mqtt
import json
import speech_recognition as sr
from nlp import NLP
import time

# Constants
SPEECH_TRIGGER = 0
TIME_SET = 1
SUNRISE = 0
AT = 1
TO_PI = "IC.embedded/tEEEm/TO_PI"
TO_APP = "IC.embedded/tEEEm/TO_APP"

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print('connected OK')
        client.connected_flag=True
        client.subscribe(TO_PI)
    else:
        print('Bad connection, returned code=', rc)
        client.bad_connection_flag=True

def recognize():
    r = sr.Recognizer()
    print('Speech starts listening')
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        print('Speech starts recognition')
        recognised = r.recognize_google(audio)
        print('Speech stops recognition')
        return True, recognised
    except Exception as e:
        print("Error:", e)
        return False, e

def on_message(client, userdata, message):
    #print('received message')
    message_payload = json.loads(message.payload.decode())
    message_type = message_payload['type']
    
    if message_type == SPEECH_TRIGGER:
        #print('this is a speech trigger from the web page')
        speech_success, text = recognize()
        if speech_success: 
            print("output of speech recognition:", text)
            nlp = NLP()
            nlp_success, meaning = nlp.parse(text)
            if nlp_success:
                print("output of natural language processing:", meaning)
                if meaning == 'sunrise':
                    data = json.dumps({'type': TIME_SET, 'nature': SUNRISE})
                else:
                    data = json.dumps({'type': TIME_SET, 'nature': AT, 'time': meaning})
                client.publish(TO_PI, data)


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