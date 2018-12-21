import pytest

from nordb.database import station2sql
from nordb.database import sitechan2sql
from nordb.database import sensor2sql
from nordb.database import instrument2sql
from nordb.database import response2sql
from nordb.database import sql2station
from nordb.database.norDBManagement import countStations
from nordb.core import usernameUtilities
from nordb.nordic import station
from nordb.nordic import sitechan
from nordb.nordic import sensor
from nordb.nordic import instrument
from nordb.nordic import response

@pytest.mark.userfixtures("setupdb", "stationFiles")
class TestSQL2Station(object):
    def testGetAllWorks(self, setupdb, stationFiles):
        stations = []
        for stat in stationFiles:
            stations.append(station.readStationStringToStation(stat, "HE"))

        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)

        stations = sql2station.getAllStations(station_date = None)

        assert len(stations) == len(stationFiles)

    def testGetStationsWorks(self, setupdb, stationFiles, responseFiles,
                             siteChanFiles, instrumentFiles, sensorFiles):
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

        stations = sql2station.getStations([1,2,3])

        assert len(stations) == 3

    def testGetOneWorks(self, setupdb, stationFiles):
        stations = []

        for stat in stationFiles:
            stations.append(station.readStationStringToStation(stat, "HE"))
        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)
        stat = sql2station.getStation(1)

        assert str(stat).strip() == stationFiles[0].strip()

