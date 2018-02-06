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

class NordicEvent:
    """
    Container object of nordic event information

    :param dict headers: headers that will be inserted to the NordicEvent
    :param array data: data array of the event
    :param int event_id: id of the event in the database
    :ivar dict headers: headers of the event in a dict where the header_type of the header is a key to a array that contains all header data of the object
    :ivar array data: data array of the event
    :ivar int event_id: event id of the event
    """

    def __init__(self, headers, data, event_id):
        self.headers = headers
        self.data = data
        self.event_id = event_id

    headers = property(operator.attrgetter('_headers'), doc="")

    @headers.setter
    def headers(self, h):
        self._headers = h

    data = property(operator.attrgetter('_data'), doc="")

    @data.setter
    def data(self, h):
        self._data = h

    def __str__(self):
        n_string = ""

        n_string += str(self.headers[1][0]) + "\n"

        for h_error in self.headers[5]:
            if h_error.header_id != -1 and h_error.header_id == self.headers[1][0].h_id:
                n_string += str(self.headers[5][0]) + "\n"
            elif h_error.header_pos == 0:
                n_string += str(self.headers[5][0]) + "\n"

        if len(self.headers[6]) > 0:
            n_string += str(self.headers[6][0]) + "\n"

        for comment in self.headers[3]:
            n_string += str(comment) + "\n"

        for i in range(1, len(self.headers[1])):
            h_main = self.headers[1][i]
            n_string += str(h_main) + "\n"

            for h_error in self.headers[5]:
                if h_error.header_id != -1:
                    if h_error.header_id == h_main.h_id:
                        n_string += str(h_error) + "\n"
                elif h_error.header_pos == i:
                    n_string += str(h_error) + "\n"

        for h_macro in self.headers[2]:
            n_string += str(h_macro) + "\n"

        n_string += createHelpHeaderString()
       
        for p_data in self.data:
            n_string += str(p_data) + "\n"
 
        return n_string
    
def createHelpHeaderString():
    """
    Function that returns the help header of type 7 as a string. 
    
    Header::
        
        " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\\n"
    :return: The help header as a string
    """
    return " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n"

