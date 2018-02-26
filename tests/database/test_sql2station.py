import pytest

from nordb.database import station2sql
from nordb.database import sql2station
from nordb.core import usernameUtilities
from nordb.nordic import station

@pytest.mark.userfixtures("setupdb", "stationFiles")
class TestSQL2Station(object):
    def testReadAllWorks(self, setupdb, stationFiles):
        stations = []
        for stat in stationFiles:    
            stations.append(station.readStationStringToStation(stat, "HE"))

        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)

        stations = sql2station.readAllStations()    
   
        assert len(stations) == len(stationFiles)

    def testReadOneWorks(self, setupdb, stationFiles):
        stations = []
        for stat in stationFiles:    
            stations.append(station.readStationStringToStation(stat, "HE"))

        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)

        stat = sql2station.readStation(1)    
   
        assert str(stat).strip() == stationFiles[0].strip()


