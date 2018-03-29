import pytest
from nordb.core.nordic2sc3 import *
from nordb.core.nordic import readNordic

@pytest.mark.usefixture("nordicEvents")
class TestNordic2SC3(object):

    def test_Conversion(self, nordicEvents):
        for e in nordicEvents:
            try:
                 nordicEvents2SC3([readNordic(e)])
            except:
                assert False

        assert True

