# Rise

Start your day right with our smart alarm clock. Speak to Rise to set your alarm to wake you up at a certain time, in a period of time or at sunrise. Rise will wake you up using a LED which gradually lights up to simulate sunrise, and then emits a soothing alarm tone. To stop the alarm. simply hover your hand over Rise's distance sensor. When you wake up, Rise will tell you the weather for the day, and you will be able to view data about your sleep environment (temperature and humidity) in the app.

## About This Repository

* **pi:** contains the files on the Raspberry Pi, including sensor, hardware and speech modules, and communication with MQTT broker.
* **www:** contains the interface (index.html) and its associated JavaScript file (index.js) which manages communication with server.

### Sensors & Additional Hardware Used

* **Temperature & Humidity Sensor (Adafruit Si7021):** Measures the temperature and humidity of your sleep environment.
* **Distance sensor (Adafruit VL53L0X):** Used to stop the alarm by hovering your hand over the device.

## Running The Application

1. Open the interface (index.html) and run speech.py on your PC.
2. Run main.py on the Raspberry Pi.

## Authors

* **Anuja Gaitonde** - *Web and Graphic Designer*
* **Cao An Le** - *App Developer*
* **Loic Alix-Brown** - *Marketing*
* **Rebecca Hallam** - *Software & Hardware Developer*
