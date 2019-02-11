#! usr/bin/env python3

import time
import RPi.GPIO as GPIO
from time import sleep


class LED:

    def __init__(self, r, g, b, r_duty, g_duty, b_duty):

        # choose BCM or BOARD numbering schemes
        GPIO.setmode(GPIO.BOARD)

        # disable warnings
        GPIO.setwarnings(False)

        # setup
        self.RGB = [12,11,13]
        for pin in self.RGB:
            # sets each pin as output for LED
            GPIO.setup(pin,GPIO.OUT,initial=GPIO.HIGH)

        # setup for PWM at 1000 Hertz for each colour
        self.R = GPIO.PWM(12,r)
        self.G = GPIO.PWM(11,g)
        self.B = GPIO.PWM(13,b)

        # start LED OFF
        self.R.start(r_duty)
        self.G.start(g_duty)
        self.B.start(b_duty)


    def gradual_on(self, pause_time):
        # brighten LED
        for i in range(100,-1,-1):
            self.R.ChangeDutyCycle(i)
            self.G.ChangeDutyCycle(i)
            self.B.ChangeDutyCycle(i)
            sleep(pause_time)

    def turn_on(self):
        self.R.ChangeDutyCycle(0)
        self.G.ChangeDutyCycle(0)
        self.B.ChangeDutyCycle(0)

    def turn_off(self):
        self.R.ChangeDutyCycle(100)
        self.G.ChangeDutyCycle(100)
        self.B.ChangeDutyCycle(100)

    def change_colour(self, r_duty, g_duty, b_duty):
        self.R.ChangeDutyCycle(r_duty)
        self.G.ChangeDutyCycle(g_duty)
        self.B.ChangeDutyCycle(b_duty)



if __name__ == "__main__":

    led = LED(1000,1000,1000,100,100,100)
    # test gradual turn on
    led.gradual_on(0.08)
    sleep(1)

    # test turn off
    led.turn_off()
    sleep(1)

    # test turn on
    led.turn_on()
    sleep(1)

    # test change colour
    led.change_colour(0,100,100)    # red
    sleep(1)
    led.change_colour(0,0,100)      # red + green
    sleep(1)
    led.change_colour(100,0,100)    # green
    sleep(1)
    led.change_colour(100,0,0)      # green + blue
    sleep(1)
    led.change_colour(100,100,0)    # blue
    sleep(1)
    led.change_colour(0,100,0)      # blue + red
    sleep(1)

    led.turn_off()
    GPIO.cleanup()
