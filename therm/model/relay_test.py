import relay
from relay import Relay
import time

class TestRelay:
    def test_thatItTurnsOff(self):
        relay = Relay(0)
        relay.turnOff()
        isOff = not relay.isOn()
        assert isOff
        time.sleep(1)

    def test_thatItTurnsOn(self):
        relay = Relay(0)
        relay.turnOn()
        isOn = relay.isOn()
        relay.turnOff()
        assert isOn
        time.sleep(1)


    def test_thatTheyTurnOnInTurn(self):
        for i in range(8):
            relay = Relay(i)
            relay.turnOff()
            time.sleep(1)
            relay.turnOn()
            isOn = relay.isOn()
            time.sleep(1)
            relay.turnOff()
            assert isOn
        time.sleep(1)
        
    def test_thatTheyAllTurnOn(self):
        relays = []
        areOn = []

        for i in range(8):
            relay = Relay(i)
            relays.append(relay)
            relay.turnOn()
            areOn.append(relay.isOn())

        time.sleep(1)

        # cleanup
        for r in relays:
            r.turnOff()

        for isOn in areOn:
            assert isOn

        time.sleep(1)

    def test_Cleanup(self):
        relay.cleanup()
