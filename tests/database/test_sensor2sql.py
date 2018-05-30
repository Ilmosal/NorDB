import pytest
from nordb.database import station2sql
from nordb.database import sitechan2sql
from nordb.database import sensor2sql
from nordb.database import instrument2sql
from nordb.database import response2sql
from nordb.core import usernameUtilities
from nordb.nordic import station
from nordb.nordic import sitechan
from nordb.nordic import sensor
from nordb.nordic import instrument
from nordb.nordic import response

@pytest.mark.userfixtures("setupdb", "stationFiles", "siteChanFiles", "instrumentFiles", "sensorFiles", "responseFiles")
class TestInsertSensor2Database(object):
    def testInsertIsSuccesfull(self, setupdb, stationFiles, siteChanFiles, instrumentFiles, sensorFiles, responseFiles):
        stations = []
        for resp in responseFiles:
            response2sql.insertResponse2Database(response.readResponseArrayToResponse(resp[0], resp[1]))

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

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM sensor") 
        ans = cur.fetchone()
 
        conn.close()
    
        assert ans[0] == len(sensorFiles)


    def testInsertWithoutInsturmentFail(self, setupdb, sensorFiles):
        sensors = []
        for sen in sensorFiles:
            sensors.append(sensor.readSensorStringToSensor(sen))
   
        for sen in sensors:
            with pytest.raises(Exception):
                sensor2sql.insertSensor2Database(sen)

