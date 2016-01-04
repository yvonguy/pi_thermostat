import thermometer as T
from thermometer import Thermometer
from temperature import Temperature

class TestThermometer:
    def test_thatTheyExist(self):
        therms = T.get_thermometers_from_os()
        assert len(therms) > 0
        # make sure they are unique
        thermsDict = dict()
        for therm in therms:
            assert therm.getIdentifier() not in thermsDict
            thermsDict[therm.getIdentifier()] = therm
        
    def test_thatTheyReadTemp(self):
        therms = T.get_thermometers_from_os()
        for therm in therms:
            t = therm.getTemperature()
            assert t.getKelvin() > 0

    def test_theRightIdentifierTypeName(self):
        therms = T.get_thermometers_from_os()
        assert len(therms) > 0
        assert type('string') == type(therms[0].getIdentifier())

        therm = Thermometer("FOODNAME")
        assert type('string') == type(therm.getIdentifier())
        
