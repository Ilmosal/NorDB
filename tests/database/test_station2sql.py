import pytest
from nordb.database import station2sql
from nordb.core import usernameUtilities
from nordb.nordic import station

@pytest.mark.userfixtures("setupdb", "stationFiles")
class TestInsertStation2Database(object):
    def testInsertIsSuccesfull(self, setupdb, stationFiles):
        stations = []
        for stat in stationFiles:
            stations.append(station.readStationStringToStation(stat, "HE"))

        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM station")
        ans = cur.fetchone()

        conn.close()

        assert ans[0] == len(stationFiles)

    def testInsertTwice(self, setupdb, stationFiles):
        stations = []
        for stat in stationFiles:
            stations.append(station.readStationStringToStation(stat, "HE"))

        for stat in stations:
            station2sql.insertStation2Database(stat, stat.network)
            station2sql.insertStation2Database(stat, stat.network)

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()

        cur.execute("SELECT count(*) FROM station")
        ans = cur.fetchone()

        conn.close()

        assert ans[0] == 7


