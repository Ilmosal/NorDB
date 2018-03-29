import pytest
from nordb.core.nordic2quakeml import *
from nordb.core.nordic import readNordic

@pytest.mark.usefixture("nordicEvents")
class TestNordic2Quakeml(object):

    def test_Conversion(self, nordicEvents):
        for e in nordicEvents:
            try:
                 nordicEvents2QuakeML([readNordic(e)])
            except:
                assert False

        assert True

