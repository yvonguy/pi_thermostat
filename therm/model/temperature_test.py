import temperature as T

class TestTemperature:
    def test_initValue(self):
        t = T.Temperature(0)
        assert t.getCelcius() == 0
        assert t.getFahrenheit() == 32.0
        assert t.getKelvin() == 273.15

    def test_intersectionValue(self):
        t = T.Temperature(-40000)
        assert t.getCelcius() == t.getFahrenheit()
        assert t.getCelciusString() == t.getFahrenheitString()
        
    def test_stringConversion(self):
        t = T.Temperature(1234)
        assert t.getCelciusString() == "  1.2"
