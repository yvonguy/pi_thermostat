from relay import Relay
import time

class TestRelay:
    def test_thatItTurnsOn(self):
        for i in range(8):
            print "Testing Relay Number " + str(i)
            relay = Relay(i)
            relay.turnOn()
            time.sleep(1)
            relay.turnOff()
            time.sleep(1)
            relay.turnOn()

            assert relay.isOn()
        
