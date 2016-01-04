import sqlite3
from datetime import datetime, timedelta

from therm.model.thermometer import Thermometer

class DB:
    def __init__(self, dbName):
        self._connection = sqlite3.connect(dbName)
        self._initialize()

    def _initialize(self):
        # make sure all tables exist
        cursor = self._connection.cursor()
        cursor.execute('''PRAGMA foreign_keys = ON;''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS zones
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                name TEXT
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS thermometers
            (
                identifier TEXT PRIMARY KEY NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                name TEXT
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS join_thermometer_zone
            (
                zone_id INTEGER,
                thermometer_identifier TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(zone_id, thermometer_identifier)
                FOREIGN KEY(zone_id) REFERENCES zones(id)
                FOREIGN KEY(thermometer_identifier) REFERENCES thermometers(identifier)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temperature_reading
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                temperature NUMBERIC NOT NULL,
                thermometer_identifier INTEGER,
                FOREIGN KEY(thermometer_identifier) REFERENCES thermometers(identifier)
            );
        ''')
        self._connection.commit()

    def reset(self):
        # dangerous call: clears all data
        cursor = self._connection.cursor()
        # drop tables in reverse creation order to avoid constraints
        cursor.execute('''
            DROP TABLE temperature_reading;
        ''')
        cursor.execute('''
            DROP TABLE join_thermometer_zone;
        ''')
        cursor.execute('''
            DROP TABLE thermometers;
        ''')
        cursor.execute('''
            DROP TABLE zones;
        ''')
        self._connection.commit()
        self._initialize()
        

    def saveThermometers(self, therms):
        cursor = self._connection.cursor()
        rawData = []
        for therm in therms:
            cursor.execute('''
                INSERT OR REPLACE INTO thermometers
                (identifier, name) VALUES (?, ?)
            ''', (therm.getIdentifier(), therm.getName()))
        self._connection.commit()

    def readThermometers(self):
        cursor = self._connection.cursor()
        cursor.execute('''
            SELECT identifier, name FROM thermometers
        ''')
        therms = []
        for row in cursor:
            therms.append(Thermometer(row[0], row[1]))
        return therms

    def getThermometer(self, identifier):
        cursor = self._connection.cursor()
        cursor.execute('''
            SELECT identifier, name FROM thermometers
            WHERE identifier = (?)
        ''', (identifier,))
        for row in cursor:
            return Thermometer(row[0], row[1])
        return None

    # save raw temperature reading associated with a thermometer
    def saveTemperatureReading(self, milliC, thermometer_identifier):
        cursor = self._connection.cursor()
        cursor.execute('''
            INSERT INTO temperature_reading
            (temperature, thermometer_identifier)  VALUES (?, ?)
        ''', (milliC, thermometer_identifier))
        self._connection.commit()

    # return the last temperature reading for a thermometer (in milliCs)
    # a row is (millicC, thermostat_identifier, created_at) in UTC
    def getLastTemperatureReading(self, thermometer_identifier):
        cursor = self._connection.cursor()
        identifier = [(thermometer_identifier)]
        cursor.execute('''
            SELECT temperature, created_at FROM temperature_reading
            WHERE thermometer_identifier = (?) ORDER BY created_at DESC LIMIT 1;
        ''', identifier)
        for row in cursor:
            # there is at most one row
            return (row[0], thermometer_identifier, row[1])
        return None

    # return a range of temperature readings for a thermometer (in milliCs)
    # a row is (millicC, thermostat_identifier, created_at) in UTC
    # if not range provided defaults to the last 24h of data
    def getTemperatureReadings(self, thermometer_identifier,
                               end_at = None,
                               duration = timedelta(days=1)):
        if end_at == None:
            end_at = datetime.utcnow()
        start_at = end_at - duration
        cursor = self._connection.cursor()
        cursor.execute('''
            SELECT temperature, created_at FROM temperature_reading
            WHERE thermometer_identifier = (?) AND
                created_at BETWEEN (?) AND (?)
            ORDER BY created_at;
        ''', (thermometer_identifier, start_at, end_at))
        reading = []
        for row in cursor:
            reading.append((row[0], thermometer_identifier, row[1]))

        return reading
