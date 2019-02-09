#! usr/bin/env python3

import time
import RPi.GPIO as GPIO
from time import sleep

# choose BCM or BOARD numbering schemes
GPIO.setmode(GPIO.BOARD)

# disable warnings
GPIO.setwarnings(False)

# setup
RGB = [12,11,13]
for pin in RGB:
    # sets each pin as output for LED
    GPIO.setup(pin,GPIO.OUT,initial=GPIO.HIGH)

# setup for PWM at 1000 Hertz for each colour
R = GPIO.PWM(12,1000)
G = GPIO.PWM(11,1000)
B = GPIO.PWM(13,1000)

# start LED OFF
R.start(100)
G.start(100)
B.start(100)

# speed
pause_time = 0.08

try:
    while True:

        # brighten LED
        for i in range(100,-1,-1):
            R.ChangeDutyCycle(i)
            G.ChangeDutyCycle(i)
            B.ChangeDutyCycle(i)
            sleep(pause_time)

        # reset to OFF
        R.ChangeDutyCycle(100)
        G.ChangeDutyCycle(100)
        B.ChangeDutyCycle(100)

except KeyboardInterrupt:

    # stop the led PWM output
    R.stop()
    G.stop()
    B.stop()

    # clean up GPIO
    GPIO.cleanup()
