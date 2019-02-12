from datetime import datetime, timedelta
import urllib.request
import os, ssl
import json

class Timing:

    def sunrise(self):
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
        with urllib.request.urlopen("https://api.sunrise-sunset.org/json?lat=51.508530&lng=-0.076132&date=tomorrow") as r:
            response = r.read()
        sunrise = json.loads(response.decode())['results']['sunrise'].split(' ')[0]
        [sunrise_h, sunrise_m, sunrise_s] = [int(x) for x in sunrise.split(':')]
        tomorrow = datetime.now() + timedelta(days=1)
        return tomorrow.replace(hour=sunrise_h, minute=sunrise_m, second=sunrise_s)

    def timeAt(self, message_time):
        wakeup_date, wakeup_time, ignore = message_time.split(' ')
        year, month, day = [int(x) for x in wakeup_date.split('-')]
        hour, minute, second = [int(float(x)) for x in wakeup_time.split(':')]
        return datetime.now().replace(year=year, month=month, day=day,
                                    hour=hour, minute=minute, second=second)


    def currentTime(self):
        now = datetime.now()
        hour = str(now.hour)
        minute = str(now.minute)
        currTime = hour + ":" + minute
        return currTime


if __name__ == "__main__":

    t = Timing()
    sunrise = t.sunrise()
    custom_time = t.timeAt("2019-02-12 00:26:18.977082 +00:00")

    print("sunrise:", sunrise)
    print("custom time:", custom_time)