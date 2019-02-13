import urllib.request
import os, ssl
import json

class Weather:

 def __init__(self):
    url = "https://api.worldweatheronline.com/premium/v1/weather.ashx?key=23fc338160134dc3aa4155139191302&q=London,united+kingdom&format=json"
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
    with urllib.request.urlopen(url) as r:
        response = json.loads(r.read().decode())

    self.description = response['data']['current_condition'][0]['weatherDesc'][0]['value']
    self.temperature = int(response['data']['current_condition'][0]['temp_C'])

        
if __name__ == '__main__':

    w = Weather()
    print(w.description)
    print(w.temperature)



