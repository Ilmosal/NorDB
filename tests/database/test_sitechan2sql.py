import pytest
from nordb.database import station2sql
from nordb.database import sitechan2sql
from nordb.core import usernameUtilities
from nordb.nordic import station
from nordb.nordic import sitechan

@pytest.mark.userfixtures("setupdb", "stationFiles", "siteChanFiles")
class TestInsertSiteChan2Database(object):
    def testInsertIsSuccesfull(self, setupdb, stationFiles, siteChanFiles):
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
    
        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM sitechan") 
        ans = cur.fetchone()
 
        conn.close()
    
        assert ans[0] == len(siteChanFiles)

    def testInsertWithoutStations(self, setupdb, siteChanFiles):
        sitechans = []
        for chan in siteChanFiles:
            sitechans.append(sitechan.readSiteChanStringToSiteChan(chan))

        for chan in sitechans:
            with pytest.raises(Exception):
                sitechan2sql.insertSiteChan2Database(chan)

    

