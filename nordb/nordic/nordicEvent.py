"""
This module contains NordicEvent class and its methods.

Functions and Classes
---------------------
"""
import operator
from datetime import datetime

from lxml import etree
from nordb.core.validationTools import validateFloat
from nordb.core.validationTools import validateInteger
from nordb.core.validationTools import validateString
from nordb.core.validationTools import validateDate
from nordb.core.nordic2quakeml import nordicEvents2QuakeML
from nordb.core.nordic2sc3 import nordicEvents2SC3
from nordb.database.nordic2sql import event2Database
from nordb.database.sql2station import getStation

from nordb.nordic.misc import CreationInfo
from nordb.nordic.misc import Magnitude
from nordb.nordic.misc import OriginTime
from nordb.nordic.misc import Coordinate
from nordb.nordic.misc import Depth

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
    def __init__(self, event_id = -1, root_id = -1, creation_id = -1, solution_type = "O", creation_info = CreationInfo(None)):
        self.main_h = []
        self.macro_h = []
        self.comment_h = []
        self.waveform_h = []
        self.data = []
        self.event_id = event_id
        self.root_id = root_id
        self.creation_id = creation_id
        self.creation_info = creation_info
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

        if len(self.main_h) != 0:
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

        if (self.event_id != -1):
            n_string += self.createIdHeaderString()
        n_string += self.createHelpHeaderString()

        for p_data in self.data:
            n_string += str(p_data) + "\n"

        return n_string

    def createIdHeaderString(self):
        """
        Function that returns the Id header of type I as a string.

        :return: The id header string
        """
        return " ID:{:<74d} I\n".format(self.event_id)

    def createHelpHeaderString(self):
        """
        Function that returns the help header of type 7 as a string.

        Header::

            " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\\n"
        :return: The help header as a string
        """
        return " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n"

    def getOriginTime(self):
        """
        Get origin time of the NordicEvent. Modifying this value will not modify the value inside the event.

        :returns: OriginTime object
        """
        if self.main_h:
            if self.main_h[0].error_h is not None:
                return OriginTime(datetime.combine( self.main_h[0].origin_date,
                                                    self.main_h[0].origin_time),
                                  self.main_h[0].error_h.second_error)
            else:
                return OriginTime(datetime.combine( self.main_h[0].origin_date,
                                                    self.main_h[0].origin_time))
        return None

    def getMagnitude(self):
        """
        Get magnitude of the NordicEvent. Modifying this value will not modify the value inside the event.

        :returns: Magnitude object
        """
        if self.main_h:
            if self.main_h[0].error_h is not None:
                return Magnitude(self.main_h[0].magnitude_1,
                                 self.main_h[0].type_of_magnitude_1,
                                 self.main_h[0].magnitude_reporting_agency_1,
                                 self.main_h[0].error_h.magnitude_error)
            else:
                return Magnitude(self.main_h[0].magnitude_1,
                                 self.main_h[0].type_of_magnitude_1,
                                 self.main_h[0].magnitude_reporting_agency_1)
        return None


    def getLatitude(self):
        """
        Get latitude of the NordicEvent. Modifying this value will not modify the value inside the event.

        :returns: Coordinate object
        """
        if self.main_h:
            if self.main_h[0].error_h is not None:
                return Coordinate(self.main_h[0].epicenter_latitude, self.main_h[0].error_h.epicenter_latitude_error)
            else:
                return Coordinate(self.main_h[0].epicenter_latitude)
        return None

    def getLongitude(self):
        """
        Get longitude of the NordicEvent. Modifying this value will not modify the value inside the event.

        :returns: Coordinate object
        """
        if self.main_h:
            if self.main_h[0].error_h is not None:
                return Coordinate(self.main_h[0].epicenter_longitude, self.main_h[0].error_h.epicenter_longitude_error)
            else:
                return Coordinate(self.main_h[0].epicenter_longitude)
        return None

    def getDepth(self):
        """
        Get depth of the NordicEvent. Modifying this value will not modify the value inside the event.

        :returns: Depth object
        """
        if self.main_h:
            if self.main_h[0].error_h is not None:
                return Depth(self.main_h[0].depth, self.main_h[0].error_h.depth_error)
            else:
                return Depth(self.main_h[0].depth)
        return None

    def getSC3(self, filepath = None):
        """
        GetSC3 returns the nordic event as a SC3-XML string or writes the event as a xml file named filepath.

        :param str filepath: filepath to to the file you want to write the file. Leave empty to only return the sc3 file as a string
        :returns: SC3 xml file as a string
        """
        sc3 = nordicEvents2SC3([self])

        if filepath is not None:
            f_sc = open(filepath, 'w')
            f_sc.write(etree.tostring(sc3, pretty_print=True).decode('utf-8'))
            f_sc.close()

        return etree.tostring(sc3, pretty_print=True).decode('utf-8')

    def getQuakeML(self, filepath = None):
        """
        GetQuakeML returns the nordic event as a QuakeML string or writes the event as a xml file named filepath

        :param str filepath: filepath to to the file you want to write the file. Leave empty to only return the quakeml file as a string
        :returns: quakeml xml file as a string
        """
        quakeml = nordicEvents2QuakeML([self])

        if filepath is not None:
            f_quake = open(filepath, 'w')
            f_quake.write(etree.tostring(quakeml, pretty_print=True).decode('utf-8'))
            f_quake.close()

        return etree.tostring(quakeml, pretty_print=True).decode('utf-8')

    def insert2DB(self, solution_type= "O", filename = None, creation_id = None, e_id = -1):
        """
        Wrapper method for event2Database function. Works exactly the same as the latter function except this method pushes only this event to the database.

        :param str solution_type: solution type of the event. Default is O
        :param str filename: name of the file that created this event. Default is None
        :param int creation_id: creation_id of the event. Default is None, if no creation id yet exist.
        :param int e_id: id of the event to which this event will be attached to. Default -1, which will create a new root_id for the event.
        """
        event2Database(self, solution_type, filename, creation_id, e_id)

    def getStations(self):
        """
        Get all stations as an array that are in the data array of this event

        :returns: array of Station objects
        """
        stations = []
        stat_codes = []
        for pick in self.data:
            if pick.station_code not in stat_codes:
                stat_codes.append(pick.station_code)

        for stat_code in stat_codes:
            stations.append(getStation(stat_code,
                                       self.getOriginTime().val))

        return [stat for stat in stations if stat is not None]

    def getHeaderString(self, *args):
        """
        Get only the header rows as a string. If args is defined, these will determine which header riows are appended to the string. The possible args are 1 - Main header, 2 - Macroseismic header, 3- Comment header, 5 - Error Header, 6 - Waveform Header.

        :param array args: header types which need to be printed
        :returns: the header string
        """
        for arg in args:
            if not isinstance(arg, int):
                raise Exception("Argument given to getHeaderString not a integer: {0}".format(arg))

        n_string = ""
        if not args or 1 in args:
            n_string += str(self.main_h[0]) + "\n"

        if not args or 5 in args:
            if self.main_h[0].error_h:
                n_string += str(self.main_h[0].error_h) + "\n"

        if not args or 6 in args:
            if self.waveform_h:
                n_string += str(self.waveform_h[0]) + "\n"

        if not args or 3 in args:
            for comment in self.comment_h:
                n_string += str(comment) + "\n"

        if not args or (1 in args or 5 in args):
            for i in range(1, len(self.main_h)):
                if not args or 1 in args:
                    n_string += str(self.main_h[i]) + "\n"

                if not args or 5 in args:
                    if self.main_h[i].error_h:
                        n_string += str(self.main_h[i].error_h) + "\n"

        if not args or 2 in args:
            for h_macro in self.macro_h:
                n_string += str(h_macro) + "\n"

        return n_string


