import pytest

from nordb.database import station2sql
from nordb.database import sql2station
from nordb.core import usernameUtilities
from nordb.nordic import station

@pytest.mark.userfixtures("setupdb", "stationFiles")
class TestSQL2Station(object):
    def testGetAllWorks(self, setupdb, stationFiles):
        stations = []
        for stat in stationFiles:
            stations.append(station.readStationStringToStation(stat, "HE"))

        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)

        stations = sql2station.getAllStations()

        assert len(stations) == len(stationFiles)

    def testGetOneWorks(self, setupdb, stationFiles):
        stations = []

        for stat in stationFiles:
            stations.append(station.readStationStringToStation(stat, "HE"))
        print("paasee")
        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)
        print("paasee")
        stat = sql2station.getStation(1)

        assert str(stat).strip() == stationFiles[0].strip()


