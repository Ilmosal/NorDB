import pytest
from nordb.core.nordic import *

@pytest.mark.usefixtures("fixableNordicEvent")
class TestNordicFix(object):
    def testFixNordic(self, fixableNordicEvent):
        with pytest.raises(Exception):
            createNordicEvent(fixableNordicEvent[0], False)
        nordic_event = createNordicEvent(fixableNordicEvent[0], True)
        assert str(nordic_event) == "".join(fixableNordicEvent[1])

    def testFixFaultyNordic(self, fixableNordicEvent):
        with pytest.raises(Exception):
            createNordicEvent(fixableNordicEvent[2], True)

        with pytest.raises(Exception):
            createNordicEvent(fixableNordicEvent[3], True)
        
