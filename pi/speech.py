import paho.mqtt.client as mqtt
import json
import speech_recognition as sr


# Constants
SPEECH_TRIGGER = 0

client = mqtt.Client()
client.connect("test.mosquitto.org",port=1883)
client.subscribe("IC.embedded/tEEEm/TO_PI")

def on_message(client, userdata, message):
    #print('received message')
    message_payload = json.loads(message.payload.decode())
    message_type = message_payload['type']
    
    if message_type == SPEECH_TRIGGER:
        #print('this is a speech trigger from the web page')

        r = sr.Recognizer()
        print('Speech starts listening')
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            try:
                print("You said " + r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Not understood")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))



client.on_message = on_message
client.loop_forever()