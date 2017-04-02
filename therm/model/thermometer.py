import os
import glob
import time
import re
from temperature import Temperature

# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

def get_identifier_from_path(device_path):
    name = re.match('/sys/bus/w1/devices/28-(.+)/w1_slave', device_path)
    return name.group(1)

def build_device_path(identifier):
    return '/sys/bus/w1/devices/28-' + identifier + '/w1_slave'
    

class Thermometer:
    def __init__(self, device_identifier, name='Undefined'):
        self._device_path = build_device_path(device_identifier)
        self._identifier = device_identifier
        self._name = name

    def getIdentifier(self):
        return self._identifier

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
    
    def _read_temp_raw(self):
        f = open(self._device_path, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def getRawTemperature(self):
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            print("Thermometer " + self.getIdentifier() + " not ready. Sleeping()")
            time.sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            self._lastRawTemp = int(temp_string)
            return self._lastRawTemp
        return None

    def getTemperature(self):
        return Temperature(self.getRawTemperature())

    def getLastTemperature(self):
        return Temperature(self._lastRawTemp)

def get_thermometers_from_os():
    base_dir = '/sys/bus/w1/devices/'
    device_folders = glob.glob(base_dir + '28*/w1_slave')
    therms = []
    for folder in device_folders:
        therms.append(Thermometer(get_identifier_from_path(folder)))
    return therms

