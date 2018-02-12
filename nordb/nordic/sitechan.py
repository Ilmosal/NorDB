"""
Contains information relevant to SiteChan object
"""
import operator
import unidecode 

from nordb.core.validationTools import validateFloat
from nordb.core.validationTools import validateInteger
from nordb.core.validationTools import validateString
from nordb.core.validationTools import validateDate
from nordb.core.utils import addString2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addFloat2String
from nordb.core.utils import stringToDate

class SiteChan:
    """
    Class for site channel information. Comes from css sitechan format.

    :param array data: all the relevant data for SiteChan in an array. These values are accessed by its numerations. 
    :ivar array data: all the relevant data for SiteChan in an array. These values are accessed by its numerations.
    :ivar int STATION_CODE: Id of the station to which sitechan refers to. Value 0
    :ivar int CHANNEL_CODE: channel code of the channel. Value 1
    :ivar int ON_DATE: date when the station started working. Value 2
    :ivar int OFF_DATE: date when the station was closed. Value 3
    :ivar int CHANNEL_TYPE: type of the channel. Value 4
    :ivar int EMPLACEMENT_DEPTH: depth relative to station elevation. Value 5
    :ivar int HORIZONTAL_ANGLE: angle horizontally. Value 6
    :ivar int VERTICAL_ANGLE: angle verically. Value 7
    :ivar int DESCRIPTION: description of the channel. Value 8
    :ivar int LOAD_DATE: date of the time when this information was created. Value 9
    :ivar int S_ID: id of the sitechan in the database. Value 10
    :ivar int STATION_ID: id of the station in the database. Value of 11
    :ivar int CSS_ID: id of the css id to which the sitechan is linked to. Value 12
    """
    header_type = 11
    STATION_CODE = 0
    CHANNEL_CODE = 1
    ON_DATE = 2
    OFF_DATE = 3
    CHANNEL_TYPE = 4
    EMPLACEMENT_DEPTH = 5
    HORIZONTAL_ANGLE = 6
    VERTICAL_ANGLE = 7
    DESCRIPTION = 8
    LOAD_DATE = 9
    S_ID = 10
    STATION_ID = 11
    CSS_ID = 12
 
    def __init__(self, data, sensors = []):
        self.station_code = data[self.STATION_CODE]
        self.channel_code = data[self.CHANNEL_CODE]
        self.on_date = data[self.ON_DATE]
        self.off_date = data[self.OFF_DATE]
        self.channel_type = data[self.CHANNEL_TYPE]
        self.emplacement_depth = data[self.EMPLACEMENT_DEPTH]
        self.horizontal_angle = data[self.HORIZONTAL_ANGLE]
        self.vertical_angle = data[self.VERTICAL_ANGLE]
        self.description = data[self.DESCRIPTION]
        self.load_date = data[self.LOAD_DATE]
        self.s_id = data[self.S_ID]
        self.station_id = data[self.STATION_ID]
        self.css_id = data[self.CSS_ID]
        self.sensors = sensors
    
    station_code = property(operator.attrgetter('_station_code'))

    @station_code.setter
    def station_code(self, val):
        val_station_code = validateString(val, "station_code", 0, 6, None, self.header_type)
        self._station_code = val_station_code

    channel_code = property(operator.attrgetter('_channel_code'))

    @channel_code.setter
    def channel_code(self, val):
        val_channel_code = validateString(val, "channel_code", 0, 8, None, self.header_type)
        self._channel_code = val_channel_code

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

    channel_type = property(operator.attrgetter('_channel_type'))
    
    @channel_type.setter
    def channel_type(self, val):
        val_channel_type = validateString(val, "channel_type", 0, 4, None, self.header_type)
        self._channel_type = val_channel_type

    emplacement_depth = property(operator.attrgetter('_emplacement_depth'))
    
    @emplacement_depth.setter
    def emplacement_depth(self, val):
        val_emplacement_depth = validateFloat(val, "emplacement_depth", 0.0, 5.0, self.header_type)
        self._emplacement_depth = val_emplacement_depth

    horizontal_angle = property(operator.attrgetter('_horizontal_angle'))
    
    @horizontal_angle.setter
    def horizontal_angle(self, val):
        val_horizontal_angle = validateFloat(val, "horizontal_angle", -1.0, 360.0, self.header_type)
        self._horizontal_angle = val_horizontal_angle

    vertical_angle = property(operator.attrgetter('_vertical_angle'))
    
    @vertical_angle.setter
    def vertical_angle(self, val):
        val_vertical_angle = validateFloat(val, "vertical_angle", -1.0, 180.0, self.header_type)
        self._vertical_angle = val_vertical_angle

    description = property(operator.attrgetter('_description'))
    
    @description.setter
    def description(self, val):
        val_description = validateString(val, "description", 0, 50, None, self.header_type)
        self._description = val_description

    load_date = property(operator.attrgetter('_load_date'))
    
    @load_date.setter
    def load_date(self, val):
        val_load_date = validateDate(val, "load_date", self.header_type)
        self._load_date = val_load_date

    css_id = property(operator.attrgetter('_css_id'))
    
    @css_id.setter
    def css_id(self, val):
        val_css_id = validateInteger(val, "css_id", None, None, self.header_type)
        self._css_id = val_css_id

    def __str__(self):
        sitechanString = ""

        sitechanString += addString2String(self.station_code, 7, '<')
        sitechanString += addString2String(self.channel_code, 8, '<')
        sitechanString += "  "
        if self.on_date is None:
            sitechanString += addInteger2String(-1, 7, '>')
        else:
            sitechanString += addInteger2String(self.on_date.year, 4, '<') 
            sitechanString += addInteger2String(self.on_date.timetuple().tm_yday, 3, '0') 
        
        sitechanString += "  "

        sitechanString += addInteger2String(self.css_id, 7, '>')

        sitechanString += "  "

        if self.off_date is None:
            sitechanString += addInteger2String(-1, 7, '>')
        else:
            sitechanString += addInteger2String(self.off_date.year, 4, '<') 
            sitechanString += addInteger2String(self.off_date.timetuple().tm_yday, 3, '0') 

        sitechanString += " "
        sitechanString += addString2String(self.channel_type, 4, '<')

        sitechanString += addFloat2String(self.emplacement_depth, 10, 4, '>')
        sitechanString += "  "
        sitechanString += addFloat2String(self.horizontal_angle, 5, 1, '>')
        sitechanString += "  "
        sitechanString += addFloat2String(self.vertical_angle, 5, 1, '>')
        sitechanString += " "
        sitechanString += addString2String(self.description, 50, '<')
        sitechanString += " "

        if self.load_date is None:
            sitechanString += addInteger2String(-1, 10, '>')
        else:
            sitechanString += addString2String(self.load_date.strftime("%Y-%b-%d"), 11, '<')

        return sitechanString

    def getAsList(self):
        sitechan_list = [   self.station_id,
                            self.channel_code,
                            self.on_date,
                            self.off_date,
                            self.channel_type,
                            self.emplacement_depth,
                            self.horizontal_angle,
                            self.vertical_angle,
                            self.description,
                            self.load_date]
                           
        return sitechan_list

def readSiteChanStringToSiteChan(chan_line):
    """
    Function for reading channel info to SiteChan object from css sitechan string

    :param str chan_line: css sitechan string
    :return: SiteChan object
    """
    channel = [None]*13

    channel[SiteChan.STATION_CODE]      = unidecode.unidecode(chan_line[:7].strip())
    channel[SiteChan.CHANNEL_CODE]      = unidecode.unidecode(chan_line[7:17].strip())
    channel[SiteChan.ON_DATE]           = unidecode.unidecode(stringToDate(chan_line[17:24].strip()))
    channel[SiteChan.OFF_DATE]          = unidecode.unidecode(stringToDate(chan_line[35:42].strip()))
    channel[SiteChan.CHANNEL_TYPE]      = unidecode.unidecode(chan_line[43:48].strip())
    channel[SiteChan.EMPLACEMENT_DEPTH] = unidecode.unidecode(chan_line[49:57].strip())
    channel[SiteChan.HORIZONTAL_ANGLE]  = unidecode.unidecode(chan_line[57:64].strip())
    channel[SiteChan.VERTICAL_ANGLE]    = unidecode.unidecode(chan_line[64:71].strip())
    channel[SiteChan.DESCRIPTION]       = unidecode.unidecode(chan_line[72:122].strip())
    channel[SiteChan.LOAD_DATE]         = unidecode.unidecode(stringToDate(chan_line[123:].strip()))
    channel[SiteChan.S_ID]              = -1
    channel[SiteChan.STATION_ID]        = -1
    channel[SiteChan.CSS_ID]            = unidecode.unidecode(chan_line[25:33].strip())

    return SiteChan(channel)


