import pytest
from nordb.core.validationTools import *

nType = -999

class TestValidateInteger(object):
    def testWithCorrectValueWorks(self):
        assert validateInteger(2, "value", 0, 3, nType) == 2

    def testWithCorrectStringValueWorks(self):
        assert validateInteger("2", "value", 0, 3, nType) == 2

    def testWithUpperLimitWorks(self):
        assert validateInteger(3, "value", 0, 3, nType) == 3

    def testWithLowerLimitWorks(self):
        assert validateInteger(0, "value", 0, 3, nType) == 0

    def testWithEmptyStringWorks(self):
        assert validateInteger("", "value", 0, 3, nType) is None

    def testWithNoneWorks(self):
        assert validateInteger(None, "value", 0, 3, nType) is None

    def testFailLowerLimitWorks(self):
        with pytest.raises(Exception):
            assert validateInteger(1, "value", 2, 3, nType) 

    def testFailUpperLimitWorks(self):
        with pytest.raises(Exception):
            assert validateInteger(5, "value", 2, 3, nType) 

    def testWrongTypeWorks(self):
        with pytest.raises(Exception):
            assert validateInteger(5.12, "value", 2, 6, nType) 

    def testWrongTypeStringWorks(self):
        with pytest.raises(Exception):
            assert validateInteger("5.12", "value", 2, 6, nType) 

    def testWithNoUpperLimitWorks(self):    
        assert validateInteger(5, "value", 0, None, nType) == 5

    def testWithNoUpperLimitWorks(self):    
        assert validateInteger(1, "value", None, 4, nType) == 1

class TestValidateFloat(object):
    def testWithCorrectValueWorks(self):
        assert validateFloat(1.5, "value", 0.0, 2.0, nType) == 1.5

    def testWithCorrectStringValueWorks(self):
        assert validateFloat("1.5", "value", 0.0, 2.0, nType) == 1.5

    def testWithUpperLimitWorks(self):
        assert validateFloat(2.0, "value", 0.0, 2.0, nType) == 2.0

    def testWithLowerLimitWorks(self):
        assert validateFloat(0.0, "value", 0.0, 2.0, nType) == 0.0

    def testWithEmptyStringWorks(self):
        assert validateFloat("", "value", 0.0, 2.0, nType) is None

    def testWithNoneWorks(self):
        assert validateFloat(None, "value", 0.0, 2.0, nType) is None

    def testFailUpperLimitWorks(self):
        with pytest.raises(Exception):
            validateFloat(2.5, "value", 0.0, 2.0, nType)

    def testFailLowerLimitWorks(self):
        with pytest.raises(Exception):
            validateFloat(0.0, "value", 1.0, 2.0, nType)

    def testFailWithNAN(self):
        with pytest.raises(Exception):
            validateFloat(float('nan'), "value", 1.0, 2.0, nType)

    def testFailWithInf(self):
        with pytest.raises(Exception):
            validateFloat(float('inf'), "value", 1.0, 2.0, nType)

    def testWrongTypeFails(self):    
         with pytest.raises(Exception):
            validateFloat(12, "value", 1.0, 2.0, nType)

    def testWrongStringTypeFails(self):    
          with pytest.raises(Exception):
            validateFloat("12", "value", 1.0, 2.0, nType)

    def testWithNoUpperLimitWorks(self):    
        assert validateFloat(5.0, "value", 0.0, None, nType) == 5.0

    def testWithNoUpperLimitWorks(self):    
        assert validateFloat(1.0, "value", None, 4.0, nType) == 1.0

class TestValidateString(object):
    def testWithCorrectStringWorks(self):
        assert validateString("test", "value", 0, 10, None, nType) == "test"

    def testWithListAllowedWorks(self):
        assert validateString("test", "value", 0, 10, ["test"], nType) == "test"
    
    def testWithSingleCharListStringWorks(self):
        assert validateString("t", "value", 1, 1, "test", nType) == "t"

    def testWithMaxLenWorks(self):
        assert validateString("test", "value", 0, 4, None, nType) == "test"

    def testWithMinLenWorks(self):
        assert validateString("test", "value", 4, 10, None, nType) == "test"

    def testWithListAllowedFails(self):
        with pytest.raises(Exception):
            validateString("test", "value", 0, 10, ["nottest"], nType)

    def testWithgListAllowedSingleChar(self):
        with pytest.raises(Exception):
            validateString("l", "value", 0, 10, "nottest", nType)

    def testWithTooLongStringFails(self):
        with pytest.raises(Exception):
            validateString("testtest", "value", 0, 3, None, nType)

    def testWithTooLongSmallFails(self):
        with pytest.raises(Exception):
            validateString("test", "value", 5, 10, None, nType)



#class TestValidateDate(object):

