import RPi.GPIO as GPIO
import sys
import glob
import time
import re

# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

this = sys.modules[__name__]
this._gpioInitialized = False
this._pinList = [5, 6, 13, 19, 26, 16, 20, 21]

class Relay:
    def __init__(self, channel):
        if not this._gpioInitialized:
            GPIO.setmode(GPIO.BCM)
            this._gpioInitialized = True

        if channel < 0 or channel >= 8:
            print("Invalid channel number " + channel)
            self._pin = -1
            return

        self._pin = this._pinList[channel]
        GPIO.setup(self._pin, GPIO.OUT)
        self.turnOn()
	

    def turnOn(self):
        GPIO.output(self._pin, GPIO.HIGH)
        self._on = True

    def turnOff(self):
        GPIO.output(self._pin, GPIO.LOW)
        self._on = False

    def isOn(self):
        return self._on
