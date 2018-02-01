"""
This module contains all class information related to Nordic Events.

Functions and Classes
---------------------
"""
import operator

from nordb.core.validationTools import validateFloat
from nordb.core.validationTools import validateInteger
from nordb.core.validationTools import validateString
from nordb.core.validationTools import validateDate
from nordb.core.utils import addString2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addFloat2String

class NordicError:
    """
    A class that functions as a collection of enums. Contains the information of the error header line of a nordic file. 
    :param list header: The header of a nordic error in a list where each index of a value corresponds to NordicError's pseudo-enum.
    :param int header_pos: Position of the main header where the NordicError refers to in the NordicEvent NordicError array
    :ivar int header_type: This value tells that this is a NordicError object. Value of 5
    :ivar int GAP: Location of the gap of the event. Value of 0
    :ivar int SECOND_ERROR: Location of the second error of the event. Value of 1
    :ivar int EPICENTER_LATITUDE_ERROR: Location of the epicenter latitude error of the event. Value of 2
    :ivar int EPICENTER_LONGITUDE_ERROR: Location of the epicenter longitude error of the event. Value of 3
    :ivar int DEPTH_ERROR: Location of the depth error of the event. Value of 4
    :ivar int MAGNITUDE_ERROR: Location of the magnitude error of the event. Value of 5
    :ivar int HEADER_ID: Location of the header id of the event. Value of 6
    :ivar int H_ID: Location of the id of the event. Value of 7
    """
    header_type = 5
    GAP = 0
    SECOND_ERROR = 1
    EPICENTER_LATITUDE_ERROR = 2
    EPICENTER_LONGITUDE_ERROR = 3
    DEPTH_ERROR = 4
    MAGNITUDE_ERROR = 5
    HEADER_ID = 6
    H_ID = 7

    def __init__(self, header, header_pos):
        self.gap = header[self.GAP]
        self.second_error = header[self.SECOND_ERROR]
        self.epicenter_latitude_error = header[self.EPICENTER_LATITUDE_ERROR]
        self.epicenter_longitude_error = header[self.EPICENTER_LONGITUDE_ERROR]
        self.depth_error = header[self.DEPTH_ERROR]
        self.magnitude_error = header[self.MAGNITUDE_ERROR]
        self.header_id = header[self.HEADER_ID]
        self.h_id = header[self.H_ID]
        self.header_pos = header_pos

    gap = property(operator.attrgetter('_gap'))
    
    @gap.setter
    def gap(self, val):
        val_gap = validateInteger(val, "gap", 0, 359, True, self.header_type)
        self._gap = val_gap

    second_error = property(operator.attrgetter('_second_error'))
    
    @second_error.setter
    def second_error(self, val):
        val_second_error = validateFloat(val, "second_error", 0.0, 99.9, True, self.header_type)
        self._second_error = val_second_error

    epicenter_latitude_error = property(operator.attrgetter('_epicenter_latitude_error'))
    
    @epicenter_latitude_error.setter
    def epicenter_latitude_error(self, val):
        val_epicenter_latitude_error = validateFloat(val, "epicenter_latitude_error", 0.0, 99.99, True, self.header_type)
        self._epicenter_latitude_error = val_epicenter_latitude_error

    epicenter_longitude_error = property(operator.attrgetter('_epicenter_longitude_error'))
    
    @epicenter_longitude_error.setter
    def epicenter_longitude_error(self, val):
        val_epicenter_longitude_error = validateFloat(val, "epicenter_longitude_error", 0.0, 99.99, True, self.header_type)
        self._epicenter_longitude_error = val_epicenter_longitude_error

    depth_error = property(operator.attrgetter('_depth_error'))
    
    @depth_error.setter
    def depth_error(self, val):
        val_depth_error = validateFloat(val, "depth_error", 0.0, 999.9, True, self.header_type)
        self._depth_error = val_depth_error

    magnitude_error = property(operator.attrgetter('_magnitude_error'))
    
    @magnitude_error.setter
    def magnitude_error(self, val):
        val_magnitude_error = validateFloat(val, "magnitude_error", 0.0, 9.9, True, self.header_type)
        self._magnitude_error = val_magnitude_error
   
    def __str__(self):
        h_string = " "
        h_string += "GAP="
        h_string += addInteger2String(self.gap, 3,'>')
        h_string += "        "
        h_string += addFloat2String(self.second_error, 4, 1, '>')
        h_string += "   "   
        h_string += addFloat2String(self.epicenter_latitude_error, 7, 3, '>')
        h_string += addFloat2String(self.epicenter_longitude_error, 8, 3, '>')
        h_string += addFloat2String(self.depth_error, 5, 1, '>')
        h_string += "             " 
        h_string += addFloat2String(self.magnitude_error, 3, 1, '>')
        h_string += "                    5"

        return h_string

    def getAsList(self):
        header_list = []
        header_list.append(self.gap)
        header_list.append(self.second_error)
        header_list.append(self.epicenter_latitude_error)
        header_list.append(self.epicenter_longitude_error)
        header_list.append(self.depth_error)
        header_list.append(self.magnitude_error)
        header_list.append(self.header_id)
   
        return header_list 


