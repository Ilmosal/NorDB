import pytest

from nordb.database import resetDB
from nordb.database import nordic2sql
from nordb.database import creationInfo
from nordb.database import station2sql
from nordb.database import sitechan2sql
from nordb.database import instrument2sql
from nordb.database import sensor2sql
from nordb.database import response2sql

from nordb.core import usernameUtilities
from nordb.core import nordic

from nordb.nordic import station
from nordb.nordic import sitechan
from nordb.nordic import instrument
from nordb.nordic import sensor
from nordb.nordic import response

@pytest.mark.usefixture("nordicEvents", "setupdb")
class TestResetEvents(object):
    def testResetEvents(self, nordicEvents, setupdb):
        events = []
        for e in nordicEvents:
            events.append(nordic.readNordic(e, False))

        creation_id = creationInfo.createCreationInfo('public')

        for e in events:
            nordic2sql.event2Database(e, "F", "dummy_name", creation_id, -1)

        resetDB.resetEvents()

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM nordic_event")
        ans = cur.fetchone()[0]
        conn.close()

        assert ans == 0

@pytest.mark.userfixtures("setupdb", "stationFiles", "siteChanFiles", "instrumentFiles", "sensorFiles", "responseFiles")
class TestResetStations(object):
    def testResetStations(self, setupdb, stationFiles, siteChanFiles, instrumentFiles, sensorFiles, responseFiles):
        for resp in responseFiles:
            response2sql.insertResponse2Database(response.readResponseArrayToResponse(resp[0], resp[1]))

        stations = []
        for stat in stationFiles:    
            stations.append(station.readStationStringToStation(stat, "HE"))

        sitechans = []
        for chan in siteChanFiles:
            sitechans.append(sitechan.readSiteChanStringToSiteChan(chan))

        instruments = []
        for ins in instrumentFiles:
            instruments.append(instrument.readInstrumentStringToInstrument(ins))

        sensors = []
        for sen in sensorFiles:
            sensors.append(sensor.readSensorStringToSensor(sen))

        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)

        for chan in sitechans:
            sitechan2sql.insertSiteChan2Database(chan)

        for ins in instruments:
            instrument2sql.insertInstrument2Database(ins)
    
        for sen in sensors:
            sensor2sql.insertSensor2Database(sen)

        resetDB.resetStations()

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM sensor") 
        ans = cur.fetchone()[0]
 
        conn.close()
    
        assert ans == 0

@pytest.mark.userfixtures("setupdb", "nordicEvents", "stationFiles", "siteChanFiles", "instrumentFiles", "sensorFiles", "responseFiles")
class TestResetAll(object):
    def testResetAll(self, nordicEvents, setupdb, stationFiles, siteChanFiles, instrumentFiles, sensorFiles, responseFiles):
        events = []
        for e in nordicEvents:
            events.append(nordic.readNordic(e, False))

        creation_id = creationInfo.createCreationInfo('public')

        for e in events:
            nordic2sql.event2Database(e, "F", "dummy_name", creation_id, -1)

        for resp in responseFiles:
            response2sql.insertResponse2Database(response.readResponseArrayToResponse(resp[0], resp[1]))

        stations = []
        for stat in stationFiles:    
            stations.append(station.readStationStringToStation(stat, "HE"))

        sitechans = []
        for chan in siteChanFiles:
            sitechans.append(sitechan.readSiteChanStringToSiteChan(chan))

        instruments = []
        for ins in instrumentFiles:
            instruments.append(instrument.readInstrumentStringToInstrument(ins))

        sensors = []
        for sen in sensorFiles:
            sensors.append(sensor.readSensorStringToSensor(sen))

        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)

        for chan in sitechans:
            sitechan2sql.insertSiteChan2Database(chan)

        for ins in instruments:
            instrument2sql.insertInstrument2Database(ins)
    
        for sen in sensors:
            sensor2sql.insertSensor2Database(sen)

        resetDB.resetDatabase()

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM sensor") 
        sensors = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM nordic_event")
        events = cur.fetchone()[0]
 
        conn.close()
    
        assert sensors == 0
        assert events == 0

