import pytest
from nordb.core.utils import *

class TestXstr(object):

    def testString(self):
        assert xstr("test") == "test"

    def testNone(self):
        assert xstr(None) == ""

class TestAddString2String(object):
    
    def testCorrectString1(self):
        assert addString2String("asia", 5, '>') == " asia"

    def testCorrectString2(self):
        assert addString2String("asia", 5, '<') == "asia "

    def testNone(self):
        assert addString2String(None, 5, '>') == "     "

    def testTooLongString(self):
        with pytest.raises(ValueError):
            addString2String("asia", 2, '<')
    
    def testWrongFormatter(self):
        with pytest.raises(ValueError):
            addString2String("asia", 5, 'a')

    def testWrongInputType(self):
        with pytest.raises(TypeError):
            addString2String(12, 5, 'a')

class TestAddInteger2String(object):
    
    def testCorrectInteger1(self):
        assert addInteger2String(3, 5, '>') == "    3"

    def testCorrectInteger2(self):
        assert addInteger2String(3, 5, '<') == "3    "

    def testCorrectInteger3(self):
        assert addInteger2String(3, 5, '0') == "00003"

    def testNoneValue(self):
        assert addInteger2String(None, 5, '0') == "     "

    def testWithTooSmallValLen(self):
        with pytest.raises(ValueError):
            addInteger2String(123, 2, '<')
    
    def testWrongFormatter(self):
        with pytest.raises(ValueError):
            addInteger2String(3, 5, 'a')

    def testWithWrongValueType(self):
        with pytest.raises(ValueError):
            addInteger2String("12.3", 5, '<')

class TestAddFloat2String(object):
    
    def testCorrectFloat1(self):
        assert addFloat2String(3.13, 5, 2, '>') == " 3.13"

    def testBigNegativeFloat(self):
        assert addFloat2String(-3.13, 5, 2, '<') == "-3.13"

    def testFloatWithLongDecimal(self):
        assert addFloat2String(3.1123413213, 5, 2, '0') == "03.11"

    def testNoneValue(self):
        assert addFloat2String(None, 5, 2, '0') == "     "

    def testWithTooSmallValLen(self):
        with pytest.raises(ValueError):
            addFloat2String(123.12, 3, 1, '<')
    
    def testWrongFormatter(self):
        with pytest.raises(ValueError):
            addFloat2String(3.13, 5, 2, 'a')

    def testWithWrongValueType(self):
        with pytest.raises(ValueError):
            addFloat2String("12.3", 5, 1, '<')

if __name__ == '__main__':
    unittest.main()
