import pytest
from nordb.core.nordic import *

@pytest.mark.usefixtures("fixableNordicEvent")
class TestNordicFix(object):
    def testFixNordic(self, fixableNordicEvent):
        with pytest.raises(Exception):
            readNordic(fixableNordicEvent[0], False)
        nordic_event = readNordic(fixableNordicEvent[0], True)
        assert str(nordic_event) == "".join(fixableNordicEvent[1])

    def testFixFaultyNordic(self, fixableNordicEvent):
        for fix_event in fixableNordicEvent[2:]:
            with pytest.raises(Exception):
                readNordic(fix_event, True)
        
