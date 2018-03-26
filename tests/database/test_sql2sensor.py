import pytest
from nordb.database import station2sql
from nordb.database import sitechan2sql
from nordb.database import sensor2sql
from nordb.database import instrument2sql
from nordb.database import sql2sensor
from nordb.core import usernameUtilities
from nordb.nordic import station
from nordb.nordic import sitechan
from nordb.nordic import sensor
from nordb.nordic import instrument

@pytest.mark.userfixtures("setupdb", "stationFiles", "siteChanFiles", "instrumentFiles", "sensorFiles")
class TestSQL2Sensor(object):
    def testGetAllSensors(self, setupdb, stationFiles, siteChanFiles, instrumentFiles, sensorFiles):
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

        sensors = sql2sensor.getAllSensors()
    
        assert len(sensors) == len(sensorFiles)

    def testGetOneSensor(self, setupdb, stationFiles, siteChanFiles, instrumentFiles, sensorFiles):
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

        sen = sql2sensor.getSensor(1)
    
        assert str(sen).strip() == str(sensors[0]).strip()


