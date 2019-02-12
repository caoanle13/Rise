import urllib.request
import os, ssl
import json

class Weather:

 def __init__(self):
    url = "https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b6907d289e10d714a6e88b30761fae22"
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
    with urllib.request.urlopen(url) as r:
        response = json.loads(r.read().decode())

    self.description = response['weather'][0]['description']
    self.temperature = int(response['main']['temp'] - 273.15)

        
if __name__ == '__main__':

    w = Weather()
    print(w.description)
    print(w.temperature)



