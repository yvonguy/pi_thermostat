import sqlite3
import db
import time
import os
import inspect
from datetime import datetime, timedelta
import therm.model.thermometer as T

def InitTestDB():
    callerName = inspect.stack()[1][3]
    dbPathname = os.path.dirname(db.__file__) + '/test_data/' + callerName + '.db'
    dbDir = os.path.dirname(dbPathname)
    # make sure dir exists
    try:
        os.stat(dbDir)
    except:
        os.mkdir(dbDir)

    try:
        testDb = db.DB(dbPathname)
        testDb.reset()
    except Exception, e:
        assert e != None, dbPathname
    return testDb, dbPathname

class TestDB:
    def test_createDB(self):
        (thermDb, dbName) = InitTestDB()

        # verify table creation
        checkDb = sqlite3.connect(dbName)
        cursor = checkDb.cursor()
        cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table';
        ''')
        
        knownTables = dict(
            zones = False,
            temperature_reading = False,
            thermometers = False,
            join_thermometer_zone = False)

        count = 0
        for row in cursor:
            if row[0] in knownTables:
                knownTables[row[0]] = True
            count += 1

        checkDb.close()
        for table in knownTables.keys():
            assert knownTables[table] == True, 'Table ' + table + ' missing'

    def test_putThermometersInDB(self):
        (thermDb, dbName) = InitTestDB()

        therms = (
            T.Thermometer("FASTFOOD", "Fake1"),
            T.Thermometer("FATSFOOD", "Fake2"))
        count = len(therms)
        assert count > 0
        thermDb.saveThermometers(therms)

        #verify they got created
        checkDb = sqlite3.connect(dbName)
        cursor = checkDb.cursor()
        cursor.execute('''
            SELECT identifier, created_at, name FROM thermometers
        ''')
        for row in cursor:
            assert row[1] != None, 'CreatedDate is missing!'
            count -= 1
        assert count == 0
        checkDb.close()

    def test_readThermometersFromDB(self):
        (thermDb, dbName) = InitTestDB()

        therms = T.get_thermometers_from_os()
        therms = (
            T.Thermometer("FASTFOOD", "Fake1"),
            T.Thermometer("FATSFOOD", "Fake2"))
        count = len(therms)
        assert count > 0
        thermDb.saveThermometers(therms)

        #verify that we can read one back
        therm = thermDb.getThermometer("FASTFOOD")
        assert therm != None
        assert therm.getIdentifier() == 'FASTFOOD'
        assert therm.getName() == 'Fake1'

        #verify that we can read them back
        therms_from_db = thermDb.readThermometers()
        assert count == len(therms_from_db)

        originalDict = dict()
        for therm in therms:
            originalDict[therm.getIdentifier()] = therm

        restoredDict = dict()
        for therm in therms_from_db:
            restoredDict[therm.getIdentifier()] = therm

        assert originalDict.keys() == restoredDict.keys()

    def test_updateThermometersInDB(self):
        (thermDb, dbName) = InitTestDB()

        therms = (
            T.Thermometer("FASTFOOD", "Fake1"),
            T.Thermometer("FATSFOOD", "Fake2"))
        count = len(therms)
        assert count > 0
        thermDb.saveThermometers(therms)

        #now change the values
        for therm in therms:
            therm.setName('Therm_' + therm.getIdentifier()[:-5])

        thermDb.saveThermometers(therms)

        #verify that we can read them back
        therms_from_db = thermDb.readThermometers()
        assert count == len(therms_from_db)

        originalDict = dict()
        for therm in therms:
            originalDict[therm.getIdentifier()] = therm

        for therm in therms_from_db:
            assert therm.getName() == originalDict[therm.getIdentifier()].getName()
        
    def test_putTemperatureIntoDB(self):
        (thermDb, dbName) = InitTestDB()

        #get the thermometers into the DB
        therms = T.get_thermometers_from_os()
        therms = (
            T.Thermometer("FASTFOOD", "Fake1"),
            T.Thermometer("FATFOOD", "Fake2"))
        thermDb.saveThermometers(therms)

        #read temperature and save to DB
        readings = dict()
        i = 0
        for therm in therms:
            temp = i
            readings[therm.getIdentifier()] = temp
            thermDb.saveTemperatureReading(temp, therm.getIdentifier())
            i += 1

        #verify that temperature is in DB
        for therm in therms:
            (temp, identifier, date) = thermDb.getLastTemperatureReading(therm.getIdentifier())
            assert identifier == therm.getIdentifier()
            assert temp == readings[therm.getIdentifier()]
        
    def test_multipleTemperatureIntoDB(self):
        (thermDb, dbName) = InitTestDB()

        #get the thermometers into the DB
        therm = T.Thermometer("000FATFOOD", "Test5")
        therms = [ therm ]
        thermDb.saveThermometers(therms)

        #read temperature and save to DB
        # create temperature readings
        for i in [1, 2, 3, 4, 5]:
            temp = 2000 + i
            thermDb.saveTemperatureReading(temp, therm.getIdentifier())

        # sleep a second to allow for "now" to be more recent
        #time.sleep(1)

        #verify that temperature is in DB
        readings = thermDb.getTemperatureReadings(therm.getIdentifier())
        assert len(readings) == 5
        i = 1
        for reading in readings:
            assert reading[1] == therm.getIdentifier()
            assert reading[0] == (2000 + i)
            i += 1
            
