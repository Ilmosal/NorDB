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

class NordicComment:
    """
    A class that functions as a collection of enums. Contains the information of the comment header line of a nordic file. 
    :param list header: The header of a nordic comment in a list where each index of a value corresponds to NordicComment's pseudo-enum.
    :ivar int header_type: This value tells that this is a NordicComment object. Value of 3
    :ivar int H_COMMENT: Location of the comment int the event. Value of 0
    :ivar int EVENT_ID: Location of the event id of the event. Value of 1
    :ivar int ID: Location of the id of the event. Value of 2
    """
    header_type = 3
    H_COMMENT = 0
    EVENT_ID = 1
    H_ID = 2

    def __init__(self, header):
        self.h_comment = header[self.H_COMMENT]
        self.event_id = header[self.EVENT_ID]
        self.h_id = header[self.H_ID]

    h_comment = property(operator.attrgetter('_h_comment'))
    
    @h_comment.setter
    def h_comment(self, val):
        val_h_comment = validateString(val, "h_comment", 0, 78, "", False, self.header_type)
        self._h_comment = val_h_comment


    def __str__(self):
        h_string = " "
        h_string += addString2String(self.h_comment, 78, '<')
        h_string += "3"

        return h_string
    
    def getAsList(self):
        header_list = []
        header_list.append(self.h_comment)
        header_list.append(self.event_id)

        return header_list


