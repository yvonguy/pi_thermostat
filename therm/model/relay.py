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
this._gpioInitialized = False
this._pinList = [5, 6, 13, 19, 26, 16, 20, 21]

class Relay:
    def __init__(self, channel):
        
        #gpio_init_time = 
        #mc = memcache.Client(['127.0.0.1:11796'], debug=0)
        #gpio_initialized = mc.get('gpio_initialized')
        #print 'Get gpio_initialized = ' + str(gpio_initialized)
        #if gpio_initialized == None:
        #    gpio_initialized = False

        #if not gpio_initialized:
        #    try:
        #        GPIO.setmode(GPIO.BCM)
        #        GPIO.setup(this._pinList, GPIO.OUT)
        #        mc.set('gpio_initialized', True)
        #        print 'Set gpio_initialized = ' + str(mc.get('gpio_initialized'))
        #    except:
        #        print 'Got Exception'

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

def init(last_init_time):
    #get the system uptime
    uptime = sh.Command('uptime')
    os_start_str = uptime('-s')
    os_start_time = datetime.strptime(os_start_str, '%Y-%m-%d %H:%M:%S')

    if last_init_time > os_start_time:
        return last_init_time

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(this._pintList, GPIO.OUT)
    return datetime.now()
