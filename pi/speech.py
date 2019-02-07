import paho.mqtt.client as mqtt
import json

# Constants
SPEECH_TRIGGER = 0

client = mqtt.Client()
client.connect("test.mosquitto.org",port=1883)
client.subscribe("IC.embedded/tEEEm/TO_PI")

def on_message(client, userdata, message):
    print('received message')
    message_payload = json.loads(message.payload.decode())
    message_type = message_payload['type']
    
    if message_type == SPEECH_TRIGGER:
        print('this is a speech trigger from the web page')

client.on_message = on_message
client.loop_forever()