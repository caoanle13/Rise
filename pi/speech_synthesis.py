from weather import Weather


# Class containing message to be synthesised as speech
class SpeechSynthesis():
    def __init__(self):
        self.messages = {
            'WAKEUP_SUNRISE' : 'Okay I will wake you up when the sun rises',
            'WAKEUP_TIME' : 'Okay I will set an alarm for ',
            'GOOD_MORNING': 'Good Morning! The current weather state is ' + Weather().description + ' and it is ' + str(Weather().temperature) + ' degrees Celsius.',
            'NO_DATA': 'There is currently no data for your night.',
            'TEMP_DATA': 'Here is your temperature data.',
            'HUMID_DATA': 'Here is your humidity data',

        }