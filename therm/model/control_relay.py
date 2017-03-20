from relay import Relay
import argparse
import sys

def turnOn(channel):
    if channel == -1:
        for i in range(8):
            turnOn(i)
    else:
        relay = Relay(channel)
        relay.turnOn()

def turnOff(channel):
    if channel == -1:
        for i in range(8):
            turnOff(i)
    else:
        relay = Relay(channel)
        relay.turnOff()

def printStatus(channel):
    if channel == -1:
        for i in range(8):
            printStatus(i)
    else:
        relay = Relay(channel)
        print "Relay[" + str(channel) + "] = " + str(relay.isOn())

def main(args):
    parser = argparse.ArgumentParser(description='Control the Relay')
    parser.add_argument('-c', '--channel', type=int, default=-1, help='The channel number in the range [0-7]')
    parser.add_argument('-s', '--status', action='store_true', help='The status of the relay')
    parser.add_argument('-o', '--on', type=int, default=-1, help='1 for on, 0 for off')

    args = parser.parse_args(args)
    print args
    if args.status == True:
        printStatus(args.channel)

    if args.on > -1:
        if args.on == 1:
            turnOn(args.channel)
        else:
            turnOff(args.channel)

if __name__ == '__main__':
    main(sys.argv[1:])
