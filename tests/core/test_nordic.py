import pytest
from nordb.core.nordic import *

@pytest.mark.usefixtures("nordicEvents", "faultyNordicEvents", "fixableNordicEvent")
class TestReadNordic(object):
    def testReadNordic(self, nordicEvents):
        for ev in nordicEvents:
            nordic_event = readNordic(ev, False)
            assert str(nordic_event) == "".join(ev)

    def testFaultyReadNordic(self, faultyNordicEvents):
        for ev in faultyNordicEvents:
            with pytest.raises(Exception):
                readNordic(ev, False)


