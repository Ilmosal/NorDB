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

class NordicWaveform:
    """
    A class that functions as a collection of enums. Contains the information of the waveform header line of a nordic file. 
    :param list header: The header of a nordic waveform in a list where each index of a value corresponds to NordicWaveform's pseudo-enum.
    :ivar int header_type: This value tells that this is a NordicWaveform object. Value of 6
    :ivar int WAVEFORM INFO: Location of the waveform info of the event. value of 0
    :ivar int EVENT ID: Location of the event id of the event. value of 1
    :ivar int ID: Location of the id of the event. value of 2
    """
    header_type = 6
    WAVEFORM_INFO = 0
    EVENT_ID = 1
    H_ID = 2

    def __init__(self, header = None):
        if header is None:
            self.waveform_info = None
            self.event_id = -1
            self.h_id = -1
        else:
            self.waveform_info = header[self.WAVEFORM_INFO]
            self.event_id = header[self.EVENT_ID]
            self.h_id = header[self.H_ID]

    waveform_info = property(operator.attrgetter('_waveform_info'), doc="")

    @waveform_info.setter
    def waveform_info(self, val):
        val_waveform_info = validateString(val, "waveform_info", 0, 78, None, self.header_type)
        self._waveform_info = val_waveform_info

    def __str__(self):
        h_string = " "
        h_string += addString2String(self.waveform_info, 78, '<')
        h_string += "6"

        return h_string

    def getAsList(self):
        header_list = []
        header_list.append(self.waveform_info)
        header_list.append(self.event_id)

        return header_list


