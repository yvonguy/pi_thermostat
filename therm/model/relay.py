import RPi.GPIO as GPIO
import sys
import glob
import memcache
import os
import re
import sh
from datetime import datetime

# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

this = sys.modules[__name__]
this._gpio_initialized = False
this._pinList = [5, 6, 13, 19, 26, 16, 20, 21]

class Relay:
    def __init__(self, channel):
        
        if this._gpio_initialized == None:
            this._gpio_initialized = False

        if not this._gpio_initialized:
            try:
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(this._pinList, GPIO.OUT)
            except:
                print 'Got Exception'

        if channel < 0 or channel >= 8:
            print("Invalid channel number " + channel)
            self._pin = -1
            return

        self._pin = this._pinList[channel]
	

    def turnOn(self):
        GPIO.output(self._pin, GPIO.LOW)

    def turnOff(self):
        GPIO.output(self._pin, GPIO.HIGH)

    def isOn(self):
        return GPIO.input(self._pin) == GPIO.LOW

def cleanup():
    GPIO.cleanup()
