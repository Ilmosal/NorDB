"""
Contains information relevant to Station class
"""

import operator
import unidecode 

from nordb.core.validationTools import validateFloat
from nordb.core.validationTools import validateString
from nordb.core.validationTools import validateDate
from nordb.core.utils import addString2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addFloat2String
from nordb.core.utils import stringToDate

class Station(object):
    """
    Class for information in station. Comes from the css site format.
 
    :param array data: all the relevant data for Station in an array. These values are accessed by its numerations. 
    :ivar int STATION_CODE: code of the station. Value 0
    :ivar int ON_DATE: date when the station started working. Value 1 
    :ivar int OFF_DATE: date when the station was closed. Value 2
    :ivar int LATITUDE: latitude of the station. Value 3
    :ivar int LONGITUDE: longitude of the staion. Value 4
    :ivar int ELEVATION: elevation of the station. Value 5
    :ivar int STATION_NAME: the whole name of the station. Value 6
    :ivar int STATION_TYPE: 2 letter string of the type of the station. Value 7
    :ivar int REFERENCE_STATION: if the station is a part of an array, this is the reference to the station. Value 8
    :ivar int NORTH_OFFSET: if the station is a part of an array, this is the offset of the north to the main station in km. Value 9
    :ivar int EAST_OFFSET: if the station is a part of an array, this is the offset of the east to the main station in km. Value 10
    :ivar int LOAD_DATE: date of the time when this information was created. Value 11
    :ivar int NETWORK: network code the network where the station belongs to
    :ivar int NETWORK_ID: id of the network where the station belongs to

    """
    header_type = 10
    STATION_CODE = 0
    ON_DATE = 1
    OFF_DATE = 2
    LATITUDE = 3
    LONGITUDE = 4
    ELEVATION = 5
    STATION_NAME = 6
    STATION_TYPE = 7 
    REFERENCE_STATION = 8
    NORTH_OFFSET = 9
    EAST_OFFSET = 10
    LOAD_DATE = 11
    NETWORK = 12
    NETWORK_ID = 13
    S_ID = 14
    sitechans = []
 
    def __init__(self, data):
        self.station_code = data[self.STATION_CODE]
        self.on_date = data[self.ON_DATE]
        self.off_date = data[self.OFF_DATE]
        self.latitude = data[self.LATITUDE]
        self.longitude = data[self.LONGITUDE]
        self.elevation = data[self.ELEVATION]
        self.station_name = data[self.STATION_NAME]
        self.station_type = data[self.STATION_TYPE]
        self.reference_station = data[self.REFERENCE_STATION]
        self.north_offset = data[self.NORTH_OFFSET]
        self.east_offset = data[self.EAST_OFFSET]
        self.load_date = data[self.LOAD_DATE]
        self.network = data[self.NETWORK]
        self.network_id = data[self.NETWORK_ID]
        self.s_id = data[self.S_ID]

    station_code = property(operator.attrgetter('_station_code'))
    
    @station_code.setter
    def station_code(self, val):
        val_station_code = validateString(val, "station_code", 0, 6, None, self.header_type)
        self._station_code = val_station_code

    on_date = property(operator.attrgetter('_on_date'))
    
    @on_date.setter
    def on_date(self, val):
        val_on_date = validateDate(val, "on_date", self.header_type)
        self._on_date = val_on_date

    off_date = property(operator.attrgetter('_off_date'))
    
    @off_date.setter
    def off_date(self, val):
        val_off_date = validateDate(val, "off_date", self.header_type)
        self._off_date = val_off_date

    latitude = property(operator.attrgetter('_latitude'))
    
    @latitude.setter
    def latitude(self, val):
        val_latitude = validateFloat(val, "latitude", -90.0, 90.0, self.header_type)
        self._latitude = val_latitude

    longitude = property(operator.attrgetter('_longitude'))
    
    @longitude.setter
    def longitude(self, val):
        val_longitude = validateFloat(val, "longitude", -180.0, 180.0, self.header_type)
        self._longitude = val_longitude

    elevation = property(operator.attrgetter('_elevation'))
    
    @elevation.setter
    def elevation(self, val):
        val_elevation = validateFloat(val, "elevation", -10.0, 10.0, self.header_type)
        self._elevation = val_elevation

    station_name = property(operator.attrgetter('_station_name'))
    
    @station_name.setter
    def station_name(self, val):
        val_station_name = validateString(val, "station_name", 0, 50, None, self.header_type)
        self._station_name = val_station_name

    station_type = property(operator.attrgetter('_station_type'))
    
    @station_type.setter
    def station_type(self, val):
        val_station_type = validateString(val, "station_type", 1, 2, ['b', 'ss', 'bb', 'll', 'ar'], self.header_type)
        self._station_type = val_station_type

    reference_station = property(operator.attrgetter('_reference_station'))
    
    @reference_station.setter
    def reference_station(self, val):
        val_reference_station = validateString(val, "reference_station", 0, 6, None, self.header_type)
        self._reference_station = val_reference_station

    north_offset = property(operator.attrgetter('_north_offset'))
    
    @north_offset.setter
    def north_offset(self, val):
        val_north_offset = validateFloat(val, "north_offset", -100.0, 100.0, self.header_type)
        self._north_offset = val_north_offset

    east_offset = property(operator.attrgetter('_east_offset'))
    
    @east_offset.setter
    def east_offset(self, val):
        val_east_offset = validateFloat(val, "east_offset", -100.0, 100.0, self.header_type)
        self._east_offset = val_east_offset

    load_date = property(operator.attrgetter('_load_date'))
    
    @load_date.setter
    def load_date(self, val):
        val_load_date = validateDate(val, "load_date", self.header_type)
        self._load_date = val_load_date

    def __str__(self):
        stationString = ""
        stationString += addString2String(self.station_code, 8, '<')

        stationString += addInteger2String(self.on_date.year, 5, '<') 
        stationString += addInteger2String(self.on_date.timetuple().tm_yday, 3, '0') 
        
        stationString += "  "

        if self.off_date is None:
            stationString += addInteger2String(-1, 7, '>')
        else:
            stationString += addInteger2String(self.off_date.year, 4, '<') 
            stationString += addInteger2String(self.off_date.timetuple().tm_yday, 3, '0') 

        stationString += "  "
        stationString += addFloat2String(self.latitude, 8, 4, '>')
        stationString += "  "
        stationString += addFloat2String(self.longitude, 8, 4, '>')

        stationString += " "
        stationString += addFloat2String(self.elevation, 9, 4, '>')

        stationString += " "
        stationString += addString2String(self.station_name, 50, '<')

        stationString += " "
        stationString += addString2String(self.station_type, 2, '<')

        stationString += "   "
        stationString += addString2String(self.reference_station, 8, '<')

        stationString += " "
        stationString += addFloat2String(self.north_offset, 7, 4, '>')

        stationString += "   "
        stationString += addFloat2String(self.east_offset, 7, 4, '>')

        stationString += " "
        stationString += addString2String(self.load_date.strftime("%Y-%b-%d"), 11, '<')

        stationString += "      "

        return stationString

    def getAsList(self):
        station_list = [self.station_code,
                        self.on_date,
                        self.off_date,
                        self.latitude,
                        self.longitude,
                        self.elevation,
                        self.station_name,
                        self.station_type,
                        self.reference_station,
                        self.north_offset,
                        self.east_offset,
                        self.load_date,
                        self.network_id,]

        return station_list
 
def readStationStringToStation(stat_line, network):
    """ 
    Function for reading Station object from a css site string

    :param str stat_line: css site string
    :param str network: network of the station
    :returns: Station object   
    """

    stations = [None]*15
    
    stations[Station.STATION_CODE]      = unidecode.unidecode(stat_line[0:6].strip())
    stations[Station.ON_DATE]           = unidecode.unidecode(stringToDate(stat_line[8:15].strip()))
    stations[Station.OFF_DATE]          = unidecode.unidecode(stringToDate(stat_line[17:24].strip()))
    stations[Station.LATITUDE]          = unidecode.unidecode(stat_line[26:34].strip())
    stations[Station.LONGITUDE]         = unidecode.unidecode(stat_line[36:44].strip())
    stations[Station.ELEVATION]         = unidecode.unidecode(stat_line[47:54].strip())
    stations[Station.STATION_NAME]      = unidecode.unidecode(stat_line[55:106].strip())
    stations[Station.STATION_TYPE]      = unidecode.unidecode(stat_line[106:108].strip())
    stations[Station.REFERENCE_STATION] = unidecode.unidecode(stat_line[111:117].strip())
    stations[Station.NORTH_OFFSET]      = unidecode.unidecode(stat_line[119:127].strip())
    stations[Station.EAST_OFFSET]       = unidecode.unidecode(stat_line[130:137].strip())
    stations[Station.LOAD_DATE]         = unidecode.unidecode(stringToDate(stat_line[138:].strip()))
    stations[Station.NETWORK]           = network
    stations[Station.NETWORK_ID]        = -1
    stations[Station.S_ID]              = -1

    return Station(stations)

