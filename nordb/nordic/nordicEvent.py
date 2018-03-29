"""
This module contains NordicEvent class and its methods.

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

    :param array main_h: NordicMain objects of the NordicEvent
    :param array macro_h: NordicMacroseismic objects of the NordicEvent
    :param array comment_h: NordicComment objects of the NordicEvent
    :param array waveform_h: NordicWaveform objects of the NordicEvent
    :param array data: data array of the event
    :param int event_id: id of the event in the database
    :param int root_id: root id of the event
    :param int creation_id: creation_id of the event
    :param string solution_type: solution type of the event
    :ivar int event_id: event id of the event
    """
    def __init__(self, event_id = -1, root_id = -1, creation_id = -1, solution_type = "O"):
        self.main_h = []
        self.macro_h = []
        self.comment_h = []
        self.waveform_h = []
        self.data = []
        self.event_id = event_id
        self.root_id = root_id
        self.creation_id = creation_id
        self.solution_type = solution_type

    event_id = property(operator.attrgetter('_event_id'), doc="")

    @event_id.setter
    def event_id(self, val_event_id):
        val_event_id = validateInteger(val_event_id, "event_id", None, None, 0)
        self._event_id = val_event_id

    root_id = property(operator.attrgetter('_root_id'), doc="")

    @root_id.setter
    def root_id(self, val_root_id):
        val_root_id = validateInteger(val_root_id, "root_id", None, None, 0)
        self._root_id = val_root_id

    creation_id = property(operator.attrgetter('_creation_id'), doc="")

    @creation_id.setter
    def creation_id(self, val_creation_id):
        val_creation_id = validateInteger(val_creation_id, "creation_id", None, None, 0)
        self._creation_id = val_creation_id

    solution_type = property(operator.attrgetter('_solution_type'), doc="")

    @solution_type.setter
    def solution_type(self, val_solution_type):
        val_solution_type = validateString(val_solution_type, "solution_type", 1, 6, None, 0)
        self._solution_type = val_solution_type

    def __eq__(self, other):
        return str(self) == str(other) 

    def __str__(self):
        n_string = ""

        n_string += str(self.main_h[0]) + "\n"

        if self.main_h[0].error_h:
            n_string += str(self.main_h[0].error_h) + "\n"

        if self.waveform_h:
            n_string += str(self.waveform_h[0]) + "\n"

        for comment in self.comment_h:
            n_string += str(comment) + "\n"

        for i in range(1, len(self.main_h)):
            n_string += str(self.main_h[i]) + "\n"
            if self.main_h[i].error_h:
                n_string += str(self.main_h[i].error_h) + "\n"

        for h_macro in self.macro_h:
            n_string += str(h_macro) + "\n"

        n_string += self.createHelpHeaderString()
       
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

