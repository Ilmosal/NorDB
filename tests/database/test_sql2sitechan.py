import pytest
from nordb.database import station2sql
from nordb.database import sitechan2sql
from nordb.database import sql2sitechan
from nordb.core import usernameUtilities
from nordb.nordic import station
from nordb.nordic import sitechan

@pytest.mark.userfixtures("setupdb", "stationFiles", "siteChanFiles")
class TestSQL2SiteChan(object):
    def testGetAllSuccesfull(self, setupdb, stationFiles, siteChanFiles):
        stations = []
        for stat in stationFiles:    
            stations.append(station.readStationStringToStation(stat, "HE"))

        sitechans = []
        for chan in siteChanFiles:
            sitechans.append(sitechan.readSiteChanStringToSiteChan(chan))

        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)

        for chan in sitechans:
            sitechan2sql.insertSiteChan2Database(chan)

        chans = sql2sitechan.getAllSitechans()
   
        assert len(chans) == len(siteChanFiles)

    def testGetOneSuccesfull(self, setupdb, stationFiles, siteChanFiles):
        stations = []
        for stat in stationFiles:    
            stations.append(station.readStationStringToStation(stat, "HE"))

        sitechans = []
        for chan in siteChanFiles:
            sitechans.append(sitechan.readSiteChanStringToSiteChan(chan))

        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)

        for chan in sitechans:
            sitechan2sql.insertSiteChan2Database(chan)

        chan = sql2sitechan.getSitechan(1)
   
        assert str(chan).strip() == siteChanFiles[0].strip()
