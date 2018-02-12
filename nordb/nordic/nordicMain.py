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
from nordb.core.utils import addString2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addFloat2String

class NordicMain:
    """
    A class that functions as a collection of enums. Contains the information of the main header line of a nordic file. 

    :param list header: The header of a nordic main in a list where each index of a value corresponds to NordicMain's pseudo-enum. This data is easily accessed by it's enums.
    :ivar datetime date: 
    :ivar  hour: 
    :ivar  minute: 
    :ivar  second: 
    :ivar  location_model: 
    :ivar  distance_indicator: 
    :ivar  event_desc_id: 
    :ivar  epicenter_latitude: 
    :ivar  epicenter_longitude: 
    :ivar  depth: 
    :ivar  depth_control: 
    :ivar  locating_indicator: 
    :ivar  epicenter_reporting_agency: 
    :ivar  stations_used: 
    :ivar  rms_time_residuals: 
    :ivar  magnitude_1: 
    :ivar  type_of_magnitude_1: 
    :ivar  magnitude_reporting_agency_1: 
    :ivar  magnitude_2: 
    :ivar  type_of_magnitude_2: 
    :ivar  magnitude_reporting_agency_2: 
    :ivar  magnitude_3: 
    :ivar  type_of_magnitude_3: 
    :ivar  magnitude_reporting_agency_3: 
    :ivar  event_id: 
    :ivar  h_id: 
    :ivar int header_type: This value tells that this is a NordicMain object. Value of 1
    :ivar int DATE: Location of the date in a array. Value of 0
    :ivar int HOUR: Location of the hour in a array. Value of 1
    :ivar int MINUTE: Location of the minute in a array. Value of 2
    :ivar int SECOND: Location of the second in a array. Value of 3
    :ivar int LOCATION_MODEL: Location of the location_model in a array. Value of 4
    :ivar int DISTANCE_INDICATOR: Location of the distance_indicator in a array. Value of 5
    :ivar int EVENT_DESC_ID: Location of the event_desc_id in a array. Value of 6
    :ivar int EPICENTER_LATITUDE: Location of the epicenter_latitude in a array. Value of 7
    :ivar int EPICENTER_LONGITUDE: Location of the epicenter_longitude in a array. Value of 8
    :ivar int DEPTH: Location of the depth in a array. Value of 9 
    :ivar int DEPTH_CONTROL: Location of the depth_control in a array. Value of 10
    :ivar int LOCATING_INDICATOR: Location of the locating_indicator in a array. Value of 11
    :ivar int EPICENTER_REPORTING_AGENCY: Location of the epicenter_reporting_agency in a array. Value of 12
    :ivar int STATIONS_USED: Location of the stations_used in a array. Value of 13
    :ivar int RMS_TIME_RESIDUALS: Location of the rms_time_residuals in a array. Value of 14
    :ivar int MAGNITUDE_1: Location of the magnitude_1 in a array. Value of 15
    :ivar int TYPE_OF_MAGNITUDE_1: Location of the type_of_magnitude_1 in a array. Value of 16
    :ivar int MAGNITUDE_REPORTING_AGENCY_1: Location of the magnitude_reporting_agency_1 in a array. Value of 17
    :ivar int MAGNITUDE_2: Location of the magnitude_2 in a array. Value of 18
    :ivar int TYPE_OF_MAGNITUDE_2: Location of the type_of_magnitude_2 in a array. Value of 19
    :ivar int MAGNITUDE_REPORTING_AGENCY_2: Location of the magnitude_reporting_agency_2 in a array. Value of 20
    :ivar int MAGNITUDE_3: Location of the magnitude_3 in a array. Value of 21
    :ivar int TYPE_OF_MAGNITUDE_3: Location of the type_of_magnitude_3 in a array. Value of 22
    :ivar int MAGNITUDE_REPORTING_AGENCY_3: Location of the magnitude_reporting_agency_3 in a array. Value of 23
    :ivar int EVENT_ID: Location of the event_id in a array. Value of 24
    :ivar int ID: Location of the id in a array. Value of 25
    """

    header_type = 1
    DATE = 0
    HOUR = 1
    MINUTE = 2
    SECOND = 3
    LOCATION_MODEL = 4
    DISTANCE_INDICATOR = 5
    EVENT_DESC_ID = 6
    EPICENTER_LATITUDE = 7
    EPICENTER_LONGITUDE = 8
    DEPTH = 9 
    DEPTH_CONTROL = 10
    LOCATING_INDICATOR = 11
    EPICENTER_REPORTING_AGENCY = 12
    STATIONS_USED = 13
    RMS_TIME_RESIDUALS = 14
    MAGNITUDE_1 = 15
    TYPE_OF_MAGNITUDE_1 = 16
    MAGNITUDE_REPORTING_AGENCY_1 = 17
    MAGNITUDE_2 = 18
    TYPE_OF_MAGNITUDE_2 = 19
    MAGNITUDE_REPORTING_AGENCY_2 = 20
    MAGNITUDE_3 = 21
    TYPE_OF_MAGNITUDE_3 = 22
    MAGNITUDE_REPORTING_AGENCY_3 = 23
    EVENT_ID = 24
    H_ID = 25

    def __init__(self, header):
        self.date = header[self.DATE]
        self.hour = header[self.HOUR]
        self.minute = header[self.MINUTE]
        self.second = header[self.SECOND]
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

    date = property(operator.attrgetter('_date'), doc="")
    
    @date.setter
    def date(self, val):
        val_date = validateDate(val, "date", self.header_type)
        self._date = val_date

    hour = property(operator.attrgetter('_hour'), doc="")
    
    @hour.setter
    def hour(self, val):
        val_hour = validateInteger(val, "hour", 0, 23, self.header_type)
        self._hour = val_hour

    minute = property(operator.attrgetter('_minute'), doc="")
    
    @minute.setter
    def minute(self, val):
        val_minute = validateInteger(val, "minute", 0, 59, self.header_type)
        self._minute = val_minute

    second = property(operator.attrgetter('_second'), doc="")
    
    @second.setter
    def second(self, val):
        val_second = validateFloat(val, "second", 0.0, 59.99, self.header_type)
        self._second = val_second

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
        h_string += addInteger2String(self.date.year, 4, '<')
        h_string += " "
        h_string += addInteger2String(self.date.month, 2, '0')
        h_string += addInteger2String(self.date.day, 2, '0')
        h_string += " "
        h_string += addInteger2String(self.hour, 2, '0')
        h_string += addInteger2String(self.minute, 2, '0')
        h_string += " "
        h_string += addFloat2String(self.second, 4, 1, '0')
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
        header_list.append(self.date)
        header_list.append(self.hour)
        header_list.append(self.minute)
        header_list.append(self.second)
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
