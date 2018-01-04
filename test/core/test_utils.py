import unittest
from nordb.core.utils import *

class TestXstr(unittest.TestCase):

    def testString(self):
        self.assertEqual(xstr("test"), "test")

    def testNone(self):
        self.assertEqual(xstr(None), "")

class TestAddString2String(unittest.TestCase):
    
    def testCorrect1(self):
        self.assertEqual(addString2String("asia", 5, '>'), " asia")

    def testCorrect2(self):
        self.assertEqual(addString2String("asia", 5, '<'), "asia ")

    def testFaulty1(self):
        with self.assertRaises(ValueError):
            addString2String("asia", 2, '<')
    
    def testFaulty2(self):
        with self.assertRaises(ValueError):
            addString2String("asia", 5, 'a')

    def testFaulty3(self):
        with self.assertRaises(TypeError):
            addString2String(12, 5, 'a')

    def testFaulty4(self):
       with self.assertRaises(TypeError):
            addString2String(12.213, 5, 'a')

class TestAddInteger2String(unittest.TestCase):
    
    def testCorrect1(self):
        self.assertEqual(addInteger2String(3, 5, '>'), "    3")

    def testCorrect2(self):
        self.assertEqual(addInteger2String(3, 5, '<'), "3    ")

    def testCorrect3(self):
        self.assertEqual(addInteger2String(3, 5, '0'), "00003")

    def testWithTooSmallValLen(self):
        with self.assertRaises(ValueError):
            addInteger2String(123, 2, '<')
    
    def testWrongFormatter(self):
        with self.assertRaises(ValueError):
            addInteger2String(3, 5, 'a')

    def testWithWrongValueType(self):
        with self.assertRaises(ValueError):
            addInteger2String("12.3", 5, '<')

class TestAddFloat2String(unittest.TestCase):
    
    def testCorrect1(self):
        self.assertEqual(addFloat2String(3.13, 5, 2, '>'), " 3.13")

    def testCorrect2(self):
        self.assertEqual(addFloat2String(3.13, 5, 2, '<'), "3.13 ")

    def testCorrect3(self):
        self.assertEqual(addFloat2String(3.1, 5, 2, '0'), "03.10")

    def testWithTooSmallValLen(self):
        with self.assertRaises(ValueError):
            addFloat2String(123.12, 3, 1, '<')
    
    def testWrongFormatter(self):
        with self.assertRaises(ValueError):
            addFloat2String(3.13, 5, 2, 'a')

    def testWithWrongValueType(self):
        with self.assertRaises(ValueError):
            addFloat2String("12.3", 5, 1, '<')

if __name__ == '__main__':
    unittest.main()
