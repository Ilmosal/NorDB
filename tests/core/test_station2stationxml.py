import pytest
from nordb.core import station2stationxml
from nordb.nordic import station
from nordb.nordic import sitechan

@pytest.mark.usefixture("faultyFiles, stationFiles", "siteChanFiles")
class TestStation2StationXML(object):
    def testCorrectStation(self, stationFiles, siteChanFiles):
        stats = []
        for stat in stationFiles:
            stats.append(station.readStationStringToStation(stat, "HE"))
        sitechans = []
        print(stats[0].sitechans)
        for chan in siteChanFiles:
            stats[0].sitechans.append(sitechan.readSiteChanStringToSiteChan(chan))

        station2stationxml.stationsToStationXML(stats)

        assert True
