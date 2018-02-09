import pytest
from nordb.core.nordic2quakeml import *
from nordb.core.nordic import createNordicEvent

@pytest.mark.usefixture("nordicEvents")
class TestNordic2Quakeml(object):

    def test_Conversion(self, nordicEvents):
        for e in nordicEvents:
            try:
                 nordicEvents2QuakeML([createNordicEvent(e)])
            except:
                assert False

        assert True

