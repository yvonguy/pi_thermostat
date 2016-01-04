#!/usr/bin/python
import sys
import time
import datetime
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from therm.model import thermometer
from therm.model.thermometer import Thermometer
from therm.model.temperature import Temperature
from therm.database.db import DB
     
def loadThermometers(db):
    therms = db.readThermometers()
    if len(therms) == 0:
        logging.warning("No thermometers found in DB. Initializing from OS")
        # this must be the first time
        therms = thermometer.get_thermometers_from_os()
        db.saveThermometers(therms)
        
    logging.info("Found " + str(len(therms)) + " thermometers")
    return therms

def saveTemperaturesToDb(db, therms):
    for therm in therms:
        milliC = therm.getRawTemperature()
        db.saveTemperatureReading(milliC, therm.getIdentifier())

        temp = Temperature(milliC)
        logging.info(therm.getIdentifier() + " = " +
                     temp.getCelciusString() + " /" +
                     temp.getFahrenheitString())

def setupLogger(level):
    #configure the default logger
    logger = logging.getLogger('')
    logger.setLevel(level)

    # add rotating handler
    handler = RotatingFileHandler('/var/log/therm.log',
                                  maxBytes=2000000,
                                  backupCount=14)

    msgFormat = '%(asctime)s %(levelname)s %(module)s %(message)s'
    dateFormat = '%Y-%m-%dT%H:%M:%SZ'
    formatter = logging.Formatter(msgFormat,dateFormat)
    formatter.converter = time.gmtime
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
def main():
    setupLogger(logging.INFO)
    try:
        logging.info("Starting up")
        db = DB('therm.db')
        therms = loadThermometers(db)
        saveTemperaturesToDb(db, therms)
        #update heaters...

        #db.close()
        logging.info("Shutting down")
    except Exception, e:
        logging.exception(e)

if __name__ == '__main__':
    main()
