import pytest
from nordb.core.nordic2sc3 import *
from nordb.core.nordic import createNordicEvent

@pytest.mark.usefixture("nordicEvents")
class TestNordic2SC3(object):

    def test_Conversion(self, nordicEvents):
        for e in nordicEvents:
            try:
                 nordicEvents2SC3([createNordicEvent(e)])
            except:
                assert False

        assert True

