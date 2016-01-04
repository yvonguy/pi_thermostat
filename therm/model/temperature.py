

# Holds the temperature in milli-celcius
class Temperature:
    # defaults to absolute zero (zero Kelvin)
    def __init__(self, milliC = -273150):
        self._milliC = milliC

    def _getTempInFormat(self, temp, integer, decimal):
        form = "{{:{integer}.{decimal}f}}".format(integer=integer, decimal=decimal)
        return form.format(temp)

    def getKelvin(self):
        return self._milliC / 1000.0 + 273.15

    def getCelcius(self):
        return self._milliC / 1000.0

    def getFahrenheit(self):
        return self._milliC * 9.0 / 5000.0 + 32.0
        
    def getCelciusString(self, integer = 5, decimal = 1):
        return self._getTempInFormat(self.getCelcius(), integer, decimal)

    def getFahrenheitString(self, integer = 5, decimal = 1):
        return self._getTempInFormat(self.getFahrenheit(), integer, decimal)

    
