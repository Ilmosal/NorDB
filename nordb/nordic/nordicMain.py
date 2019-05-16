"""
This module contains all class information related to NordicMain header

Functions and Classes
---------------------
"""
import operator

from nordb.core.validationTools import validateFloat
from nordb.core.validationTools import validateInteger
from nordb.core.validationTools import validateString
from nordb.core.validationTools import validateDate
from nordb.core.validationTools import validateTime

from nordb.nordic.nordicError import NordicError
from nordb.core.utils import addString2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addFloat2String

class NordicMain:
    """
    A class that functions as a collection of enums. Contains the information of the main header line of a nordic file. 

    :param list header: The header of a nordic main in a list where each index of a value corresponds to NordicMain's pseudo-enum. This data is easily accessed by it's enums.
    :ivar time origin_time: Origin time of the event
    :ivar date origin_date: Origin date of the event
    :ivar str location_model: location model used for this main header or the quality indicator.
    :ivar str distance_indicator: distance indicator of the event. L - Local, R - Regional, D - Distant
    :ivar str event_desc_id: Event Description id. See 'Nordic Format' page in the documentation for more details
    :ivar float epicenter_latitude: latitude coordinate of the event
    :ivar float epicenter_longitude: longitude coordinate of the event
    :ivar float depth: depth of the event
    :ivar str depth_control: Flag for whether the depth is fixed or not
    :ivar str locating_indicator: Flag for whether the depth is fixed or not
    :ivar str epicenter_reporting_agency: The reporting agency of the event
    :ivar int stations_used: How many stations were used for this analysis
    :ivar float rms_time_residuals: RMS of the time residuals
    :ivar float magnitude_1: Magnitude of this analysis
    :ivar str type_of_magnitude_1: Type of the magnitude of this analysis
    :ivar str magnitude_reporting_agency_1: reporting agency of this analysis
    :ivar float magnitude_2: Magnitude of an other analysis
    :ivar str type_of_magnitude_2: Type of the magnitude of an other analysis
    :ivar str magnitude_reporting_agency_2: Reporting agency of an other analysis
    :ivar float magnitude_3: Magnitude of an other analysis
    :ivar str type_of_magnitude_3: Type of the magnitude of this analysis
    :ivar str magnitude_reporting_agency_3: Reporting agency of an other analysis
    :ivar int event_id: Event id of this event in the database
    :ivar int h_id: id of this header in the database
    :ivar int header_type: This value tells that this is a NordicMain object. Value of 1
    :ivar int ORIGIN_TIME: Location of the date in a array. Value of 0
    :ivar int ORIGIN_DATE: Location of the hour in a array. Value of 1
    :ivar int LOCATION_MODEL: Location of the location_model in a array. Value of 2
    :ivar int DISTANCE_INDICATOR: Location of the distance_indicator in a array. Value of 3
    :ivar int EVENT_DESC_ID: Location of the event_desc_id in a array. Value of 4
    :ivar int EPICENTER_LATITUDE: Location of the epicenter_latitude in a array. Value of 5
    :ivar int EPICENTER_LONGITUDE: Location of the epicenter_longitude in a array. Value of 6
    :ivar int DEPTH: Location of the depth in a array. Value of 7
    :ivar int DEPTH_CONTROL: Location of the depth_control in a array. Value of 8
    :ivar int LOCATING_INDICATOR: Location of the locating_indicator in a array. Value of 9
    :ivar int EPICENTER_REPORTING_AGENCY: Location of the epicenter_reporting_agency in a array. Value of 10
    :ivar int STATIONS_USED: Location of the stations_used in a array. Value of 11
    :ivar int RMS_TIME_RESIDUALS: Location of the rms_time_residuals in a array. Value of 12
    :ivar int MAGNITUDE_1: Location of the magnitude_1 in a array. Value of 13
    :ivar int TYPE_OF_MAGNITUDE_1: Location of the type_of_magnitude_1 in a array. Value of 14
    :ivar int MAGNITUDE_REPORTING_AGENCY_1: Location of the magnitude_reporting_agency_1 in a array. Value of 15
    :ivar int MAGNITUDE_2: Location of the magnitude_2 in a array. Value of 16
    :ivar int TYPE_OF_MAGNITUDE_2: Location of the type_of_magnitude_2 in a array. Value of 17
    :ivar int MAGNITUDE_REPORTING_AGENCY_2: Location of the magnitude_reporting_agency_2 in a array. Value of 18
    :ivar int MAGNITUDE_3: Location of the magnitude_3 in a array. Value of 19
    :ivar int TYPE_OF_MAGNITUDE_3: Location of the type_of_magnitude_3 in a array. Value of 20
    :ivar int MAGNITUDE_REPORTING_AGENCY_3: Location of the magnitude_reporting_agency_3 in a array. Value of 21
    :ivar int EVENT_ID: Location of the event_id in a array. Value of 22
    :ivar int ID: Location of the id in a array. Value of 23
    """

    header_type = 1
    ORIGIN_TIME = 0
    ORIGIN_DATE = 1
    LOCATION_MODEL = 2
    DISTANCE_INDICATOR = 3
    EVENT_DESC_ID = 4
    EPICENTER_LATITUDE = 5
    EPICENTER_LONGITUDE = 6
    DEPTH = 7
    DEPTH_CONTROL = 8
    LOCATING_INDICATOR = 9
    EPICENTER_REPORTING_AGENCY = 10
    STATIONS_USED = 11
    RMS_TIME_RESIDUALS = 12
    MAGNITUDE_1 = 13
    TYPE_OF_MAGNITUDE_1 = 14
    MAGNITUDE_REPORTING_AGENCY_1 = 15
    MAGNITUDE_2 = 16
    TYPE_OF_MAGNITUDE_2 = 17
    MAGNITUDE_REPORTING_AGENCY_2 = 18
    MAGNITUDE_3 = 19
    TYPE_OF_MAGNITUDE_3 = 20
    MAGNITUDE_REPORTING_AGENCY_3 = 21
    EVENT_ID = 22
    H_ID = 23

    def __init__(self, header=None, error_h = None):
        self.error_h = error_h
        if header is None:
            self.origin_time = None
            self.origin_date = None
            self.location_model = None
            self.distance_indicator = None
            self.event_desc_id = None
            self.epicenter_latitude = None
            self.epicenter_longitude = None
            self.depth = None
            self.depth_control = None
            self.locating_indicator = None
            self.epicenter_reporting_agency = None
            self.stations_used = None
            self.rms_time_residuals = None
            self.magnitude_1 = None
            self.type_of_magnitude_1 = None
            self.magnitude_reporting_agency_1 = None
            self.magnitude_2 = None
            self.type_of_magnitude_2 = None
            self.magnitude_reporting_agency_2 = None
            self.magnitude_3 = None
            self.type_of_magnitude_3 = None
            self.magnitude_reporting_agency_3 = None
            self.event_id = -1
            self.h_id = -1
        else:
            self.origin_time = header[self.ORIGIN_TIME]
            self.origin_date = header[self.ORIGIN_DATE]
            self.location_model = header[self.LOCATION_MODEL]
            self.distance_indicator = header[self.DISTANCE_INDICATOR]
            self.event_desc_id = header[self.EVENT_DESC_ID]
            self.epicenter_latitude = header[self.EPICENTER_LATITUDE]
            self.epicenter_longitude = header[self.EPICENTER_LONGITUDE]
            self.depth = header[self.DEPTH]
            self.depth_control = header[self.DEPTH_CONTROL]
            self.locating_indicator = header[self.LOCATING_INDICATOR]
            self.epicenter_reporting_agency = header[self.EPICENTER_REPORTING_AGENCY]
            self.stations_used = header[self.STATIONS_USED]
            self.rms_time_residuals = header[self.RMS_TIME_RESIDUALS]
            self.magnitude_1 = header[self.MAGNITUDE_1]
            self.type_of_magnitude_1 = header[self.TYPE_OF_MAGNITUDE_1]
            self.magnitude_reporting_agency_1 = header[self.MAGNITUDE_REPORTING_AGENCY_1]
            self.magnitude_2 = header[self.MAGNITUDE_2]
            self.type_of_magnitude_2 = header[self.TYPE_OF_MAGNITUDE_2]
            self.magnitude_reporting_agency_2 = header[self.MAGNITUDE_REPORTING_AGENCY_2]
            self.magnitude_3 = header[self.MAGNITUDE_3]
            self.type_of_magnitude_3 = header[self.TYPE_OF_MAGNITUDE_3]
            self.magnitude_reporting_agency_3 = header[self.MAGNITUDE_REPORTING_AGENCY_3]
            self.event_id = header[self.EVENT_ID]
            self.h_id = header[self.H_ID]

    error_h = property(operator.attrgetter('_error_h'), doc="")

    @error_h.setter
    def error_h(self, val):
        if type(val) is NordicError or val is None:
            self._error_h = val
        else:
            raise Exception("Given value not a NordicError!")

    origin_time = property(operator.attrgetter('_origin_time'), doc="")

    @origin_time.setter
    def origin_time(self, val):
        val_origin_time = validateTime(val, "origin_time", self.header_type)
        self._origin_time = val_origin_time

    origin_date = property(operator.attrgetter('_origin_date'), doc="")

    @origin_date.setter
    def origin_date(self, val):
        val_origin_date = validateDate(val, "origin_date", self.header_type)
        self._origin_date = val_origin_date

    location_model = property(operator.attrgetter('_location_model'), doc="")

    @location_model.setter
    def location_model(self, val):
        val_location_model = validateString(val, "location_model", 0, 1, None, self.header_type)
        self._location_model = val_location_model

    distance_indicator = property(operator.attrgetter('_distance_indicator'), doc="")

    @distance_indicator.setter
    def distance_indicator(self, val):
        val_distance_indicator = validateString(val, "distance_indicator", 0, 1, "LRD", self.header_type)
        self._distance_indicator = val_distance_indicator

    event_desc_id = property(operator.attrgetter('_event_desc_id'), doc="")

    @event_desc_id.setter
    def event_desc_id(self, val):
        val_event_desc_id = validateString(val, "event_desc_id", 0, 1, None, self.header_type)
        self._event_desc_id = val_event_desc_id

    epicenter_latitude = property(operator.attrgetter('_epicenter_latitude'), doc="")

    @epicenter_latitude.setter
    def epicenter_latitude(self, val):
        val_epicenter_latitude = validateFloat(val, "epicenter_latitude", -90.0, 90.0, self.header_type)
        self._epicenter_latitude = val_epicenter_latitude

    epicenter_longitude = property(operator.attrgetter('_epicenter_longitude'), doc="")

    @epicenter_longitude.setter
    def epicenter_longitude(self, val):
        val_epicenter_longitude = validateFloat(val, "epicenter_longitude", -180.0, 180.0, self.header_type)
        self._epicenter_longitude = val_epicenter_longitude

    depth = property(operator.attrgetter('_depth'), doc="")

    @depth.setter
    def depth(self, val):
        val_depth = validateFloat(val, "depth", 0.0, 999.9, self.header_type)
        self._depth = val_depth

    depth_control = property(operator.attrgetter('_depth_control'), doc="")

    @depth_control.setter
    def depth_control(self, val):
        val_depth_control = validateString(val, "depth_control", 0, 1, "FSGA", self.header_type)
        self._depth_control = val_depth_control

    locating_indicator = property(operator.attrgetter('_locating_indicator'), doc="")

    @locating_indicator.setter
    def locating_indicator(self, val):
        val_locating_indicator = validateString(val, "locating_indicator", 0, 1, "FS", self.header_type)
        self._locating_indicator = val_locating_indicator

    epicenter_reporting_agency = property(operator.attrgetter('_epicenter_reporting_agency'), doc="")

    @epicenter_reporting_agency.setter
    def epicenter_reporting_agency(self, val):
        val_epicenter_reporting_agency = validateString(val, "epicenter_reporting_agency", 0, 3, None, self.header_type)
        self._epicenter_reporting_agency = val_epicenter_reporting_agency

    stations_used = property(operator.attrgetter('_stations_used'), doc="")

    @stations_used.setter
    def stations_used(self, val):
        val_stations_used = validateInteger(val, "stations_used", 0, 999, self.header_type)
        self._stations_used = val_stations_used

    rms_time_residuals = property(operator.attrgetter('_rms_time_residuals'), doc="")

    @rms_time_residuals.setter
    def rms_time_residuals(self, val):
        val_rms_time_residuals = validateFloat(val, "rms_time_residuals", -9.9, 99.9, self.header_type)
        self._rms_time_residuals = val_rms_time_residuals

    magnitude_1 = property(operator.attrgetter('_magnitude_1'), doc="")

    @magnitude_1.setter
    def magnitude_1(self, val):
        val_magnitude_1 = validateFloat(val, "magnitude_1", -1.0, 9.9, self.header_type)
        self._magnitude_1 = val_magnitude_1

    type_of_magnitude_1 = property(operator.attrgetter('_type_of_magnitude_1'), doc="")

    @type_of_magnitude_1.setter
    def type_of_magnitude_1(self, val):
        val_type_of_magnitude_1 = validateString(val, "type_of_magnitude_1", 0, 1, None, self.header_type)
        self._type_of_magnitude_1 = val_type_of_magnitude_1

    magnitude_reporting_agency_1 = property(operator.attrgetter('_magnitude_reporting_agency_1'), doc="")

    @magnitude_reporting_agency_1.setter
    def magnitude_reporting_agency_1(self, val):
        val_magnitude_reporting_agency_1 = validateString(val, "magnitude_reporting_agency_1", 0, 3, None, self.header_type)
        self._magnitude_reporting_agency_1 = val_magnitude_reporting_agency_1

    magnitude_2 = property(operator.attrgetter('_magnitude_2'), doc="")

    @magnitude_2.setter
    def magnitude_2(self, val):
        val_magnitude_2 = validateFloat(val, "magnitude_2", -1.0, 9.9, self.header_type)
        self._magnitude_2 = val_magnitude_2

    type_of_magnitude_2 = property(operator.attrgetter('_type_of_magnitude_2'), doc="")

    @type_of_magnitude_2.setter
    def type_of_magnitude_2(self, val):
        val_type_of_magnitude_2 = validateString(val, "type_of_magnitude_2", 0, 1, None, self.header_type)
        self._type_of_magnitude_2 = val_type_of_magnitude_2

    magnitude_reporting_agency_2 = property(operator.attrgetter('_magnitude_reporting_agency_2'), doc="")

    @magnitude_reporting_agency_2.setter
    def magnitude_reporting_agency_2(self, val):
        val_magnitude_reporting_agency_2 = validateString(val, "magnitude_reporting_agency_2", 0, 3, None, self.header_type)
        self._magnitude_reporting_agency_2 = val_magnitude_reporting_agency_2

    magnitude_3 = property(operator.attrgetter('_magnitude_3'), doc="")

    @magnitude_3.setter
    def magnitude_3(self, val):
        val_magnitude_3 = validateFloat(val, "magnitude_3", -1.0, 9.9, self.header_type)
        self._magnitude_3 = val_magnitude_3

    type_of_magnitude_3 = property(operator.attrgetter('_type_of_magnitude_3'), doc="")

    @type_of_magnitude_3.setter
    def type_of_magnitude_3(self, val):
        val_type_of_magnitude_3 = validateString(val, "type_of_magnitude_3", 0, 1, None, self.header_type)
        self._type_of_magnitude_3 = val_type_of_magnitude_3

    magnitude_reporting_agency_3 = property(operator.attrgetter('_magnitude_reporting_agency_3'), doc="")

    @magnitude_reporting_agency_3.setter
    def magnitude_reporting_agency_3(self, val):
        val_magnitude_reporting_agency_3 = validateString(val, "magnitude_reporting_agency_3", 0, 3, None, self.header_type)
        self._magnitude_reporting_agency_3 = val_magnitude_reporting_agency_3

    def __str__(self):
        h_string = " "

        if self.origin_date is not None:
            h_string += addInteger2String(self.origin_date.year, 4, '<')
            h_string += " "
            h_string += addInteger2String(self.origin_date.month, 2, '0')
            h_string += addInteger2String(self.origin_date.day, 2, '0')
        else:
            h_string = "         "
        h_string += " "
        if self.origin_time is not None:
            h_string += addInteger2String(self.origin_time.hour, 2, '0')
            h_string += addInteger2String(self.origin_time.minute, 2, '0')
            h_string += " "
            second = float(self.origin_time.second) + float(self.origin_time.microsecond)/1000000
            h_string += addFloat2String(second, 4, 1, '0')
        else:
            h_string += "         "
        h_string += addString2String(self.location_model, 1, '<')
        h_string += addString2String(self.distance_indicator, 1, '<')
        h_string += addString2String(self.event_desc_id, 1, '<')
        h_string += addFloat2String(self.epicenter_latitude, 7, 3, '>')
        h_string += addFloat2String(self.epicenter_longitude, 8, 3, '>')
        h_string += addFloat2String(self.depth, 5, 1, '>')
        h_string += addString2String(self.depth_control, 1, '>')
        h_string += addString2String(self.locating_indicator, 1, '>')
        h_string += addString2String(self.epicenter_reporting_agency, 3, '<')
        h_string += addInteger2String(self.stations_used, 3, '>')
        h_string += addFloat2String(self.rms_time_residuals, 4, 1, '>')
        h_string += " "
        h_string += addFloat2String(self.magnitude_1, 3, 1, '>')
        h_string += addString2String(self.type_of_magnitude_1, 1, '>')
        h_string += addString2String(self.magnitude_reporting_agency_1, 3, '>')
        h_string += " "
        h_string += addFloat2String(self.magnitude_2, 3, 1, '>')
        h_string += addString2String(self.type_of_magnitude_2, 1, '>')
        h_string += addString2String(self.magnitude_reporting_agency_2, 3, '>')
        h_string += " "
        h_string += addFloat2String(self.magnitude_3, 3, 1, '>')
        h_string += addString2String(self.type_of_magnitude_3, 1, '>')
        h_string += addString2String(self.magnitude_reporting_agency_3, 3, '>')
        h_string += "1"

        return h_string

    def getAsList(self):
        header_list = []
        header_list.append(self.origin_time)
        header_list.append(self.origin_date)
        header_list.append(self.location_model)
        header_list.append(self.distance_indicator)
        header_list.append(self.event_desc_id)
        header_list.append(self.epicenter_latitude)
        header_list.append(self.epicenter_longitude)
        header_list.append(self.depth)
        header_list.append(self.depth_control)
        header_list.append(self.locating_indicator)
        header_list.append(self.epicenter_reporting_agency)
        header_list.append(self.stations_used)
        header_list.append(self.rms_time_residuals)
        header_list.append(self.magnitude_1)
        header_list.append(self.type_of_magnitude_1)
        header_list.append(self.magnitude_reporting_agency_1)
        header_list.append(self.magnitude_2)
        header_list.append(self.type_of_magnitude_2)
        header_list.append(self.magnitude_reporting_agency_2)
        header_list.append(self.magnitude_3)
        header_list.append(self.type_of_magnitude_3)
        header_list.append(self.magnitude_reporting_agency_3)
        header_list.append(self.event_id)

        return header_list
