"""
Contains information relevant to Sensor class
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

class Sensor(object):
    """
    Class for sensor information. Comes from css sensor format.

    :param array data: all the relevant data for Sensor in an array. These values are accessed by its numerations. 
    :ivar int TIME: epoch time of start of recording period
    :ivar int ENDTIME: epoch time of end of recording period
    :ivar int JDATE: julian date
    :ivar int CALRATIO: calibration
    :ivar int CALPER: calibration period
    :ivar int TSHIFT: correction to data processing time
    :ivar int INSTANT: (y/n) discrete/continuing snapshot
    :ivar int LDDATE:
    :ivar int CHANNEL_ID: id of the channel to which sensor refers to. 
    :ivar int INTRUMENT_ID: id of the instrument to which the sensor refers to. 
    :ivar int ID: id of the sensor
    :ivar int STATION_CODE: code of the station the sensor is attached to
    :ivar int CHANNEL_CODE: channel code of the sensor
    """
    header_type = 13
    TIME = 0
    ENDTIME = 1
    JDATE = 2
    CALRATIO = 3
    CALPER = 4
    TSHIFT = 5
    INSTANT = 6
    LDDATE = 7
    CHANNEL_CSS_ID = 8
    INSTRUMENT_CSS_ID = 9
    S_ID = 10
    STATION_CODE = 11
    CHANNEL_CODE = 12
    CHANNEL_ID = 13
    INSTRUMENT_ID = 14
    instruments = []

    def __init__(self, data):
        self.time = data[self.TIME]
        self.endtime = data[self.ENDTIME]
        self.jdate = data[self.JDATE]
        self.calratio = data[self.CALRATIO]
        self.calper = data[self.CALPER]
        self.tshift = data[self.TSHIFT]
        self.instant = data[self.INSTANT]
        self.lddate = data[self.LDDATE]
        self.channel_id = data[self.CHANNEL_ID]
        self.instrument_id = data[self.INSTRUMENT_ID]
        self.s_id = data[self.S_ID]
        self.station_code = data[self.STATION_CODE]
        self.channel_code = data[self.CHANNEL_CODE]
        self.instrument_css_id = data[self.INSTRUMENT_CSS_ID]
        self.channel_css_id = data[self.CHANNEL_CSS_ID]

    time = property(operator.attrgetter('_time'))
    
    @time.setter
    def time(self, val):
        val_time = validateFloat(val, "time", -9999999999.99, 99999999999.999, self.header_type)
        self._time = val_time

    endtime = property(operator.attrgetter('_endtime'))
    
    @endtime.setter
    def endtime(self, val):
        val_endtime = validateFloat(val, "endtime", 0.0, 9999999999.999, self.header_type)
        self._endtime = val_endtime

    jdate = property(operator.attrgetter('_jdate'))
    
    @jdate.setter
    def jdate(self, val):
        val_jdate = validateDate(val, "jdate", self.header_type)
        self._jdate = val_jdate

    calratio = property(operator.attrgetter('_calratio'))
    
    @calratio.setter
    def calratio(self, val):
        val_calratio = validateFloat(val, "calratio", -1.0, 10.0, self.header_type)
        self._calratio = val_calratio

    calper = property(operator.attrgetter('_calper'))
    
    @calper.setter
    def calper(self, val):
        val_calper = validateFloat(val, "calper", -1.0, 100.0, self.header_type)
        self._calper = val_calper

    tshift = property(operator.attrgetter('_tshift'))
    
    @tshift.setter
    def tshift(self, val):
        val_tshift = validateFloat(val, "tshift", -1.0, 9.9, self.header_type)
        self._tshift = val_tshift

    instant = property(operator.attrgetter('_instant'))
    
    @instant.setter
    def instant(self, val):
        val_instant = validateString(val, "instant", 1, 1, "ynYN", self.header_type)
        self._instant = val_instant

    lddate = property(operator.attrgetter('_lddate'))
    
    @lddate.setter
    def lddate(self, val):
        val_lddate = validateDate(val, "lddate", self.header_type)
        self._lddate = val_lddate

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

    channel_id = property(operator.attrgetter('_channel_id'))
    
    @channel_id.setter
    def channel_id(self, val):
        val_channel_id = validateInteger(val, "channel_id", None, None, self.header_type)
        self._channel_id = val_channel_id

    instrument_id = property(operator.attrgetter('_instrument_id'))
    
    @instrument_id.setter
    def instrument_id(self, val):
        val_instrument_id = validateInteger(val, "instrument_id", None, None, self.header_type)
        self._instrument_id = val_instrument_id

    channel_css_id = property(operator.attrgetter('_channel_css_id'))
    
    @channel_css_id.setter
    def channel_css_id(self, val):
        val_channel_css_id = validateInteger(val, "channel_css_id", None, None, self.header_type)
        self._channel_css_id = val_channel_css_id

    instrument_css_id = property(operator.attrgetter('_instrument_css_id'))
    
    @instrument_css_id.setter
    def instrument_css_id(self, val):
        val_instrument_css_id = validateInteger(val, "instrument_css_id", None, None, self.header_type)
        self._instrument_css_id = val_instrument_css_id



    def __str__(self):
        sensorString = ""

        sensorString += addString2String(self.station_code, 6, '<')
        sensorString += " "
        sensorString += addString2String(self.channel_code, 8, '<')
        sensorString += "  "
        sensorString += addFloat2String(self.time, 16, 5, '>')
        sensorString += "  "
        sensorString += addFloat2String(self.endtime, 16, 5, '>')
        sensorString += " "
        sensorString += addInteger2String(self.instrument_css_id, 8, '>')
        sensorString += " "
        sensorString += addInteger2String(self.channel_css_id, 8, '>')
        sensorString += "  "
        
        if self.jdate is None:
            sensorString += addInteger2String(-1, 7, '>')
        else:
            sensorString += addInteger2String(self.jdate.year, 4, '<')
            sensorString += addInteger2String(self.jdate.timetuple().tm_yday, 3, '0')
        
        sensorString += " "
        sensorString += addFloat2String(self.calratio, 16, 6, '>')
        sensorString += " "
        sensorString += addFloat2String(self.calper, 16, 6, '>')
        sensorString += " "
        sensorString += addFloat2String(self.tshift, 6, 4, '>') 
        sensorString += " "
        sensorString += addString2String(self.instant, 1, '>')
        sensorString += "       "

        if self.lddate is None:
            sensorString += addInteger2String(-1, 10, '>')
        else:
            sensorString += addString2String(self.lddate.strftime("%Y-%b-%d"), 11, '<')

        return sensorString
  
    def getAsList(self):
        sensor_list = [ self.time,
                        self.endtime,
                        self.jdate,
                        self.calratio,
                        self.calper,
                        self.tshift,
                        self.instant,
                        self.lddate,
                        self.channel_id,
                        self.instrument_id]

        return sensor_list

def readSensorStringToSensor(sen_line):
    """
    Function for reading sensor string into a Sensor object

    :param str sen_line:  css sensor string
    :return: Sensor object
    """
    sensor = [None]*15

    sensor[Sensor.TIME]             = unidecode.unidecode(sen_line[15:33].strip())
    sensor[Sensor.ENDTIME]          = unidecode.unidecode(sen_line[35:51].strip())
    sensor[Sensor.JDATE]            = unidecode.unidecode(stringToDate(sen_line[71:78].strip()))
    sensor[Sensor.CALRATIO]         = unidecode.unidecode(sen_line[78:96].strip())
    sensor[Sensor.CALPER]           = unidecode.unidecode(sen_line[95:112] .strip())
    sensor[Sensor.TSHIFT]           = unidecode.unidecode(sen_line[113:119].strip())
    sensor[Sensor.INSTANT]          = unidecode.unidecode(sen_line[120].strip())
    sensor[Sensor.LDDATE]           = unidecode.unidecode(stringToDate(sen_line[122:].strip()))
    sensor[Sensor.CHANNEL_CSS_ID]   = unidecode.unidecode(sen_line[62:69].strip())
    sensor[Sensor.INSTRUMENT_CSS_ID]= unidecode.unidecode(sen_line[51:60].strip())
    sensor[Sensor.S_ID]             = -1
    sensor[Sensor.STATION_CODE]     = unidecode.unidecode(sen_line[:7].strip())
    sensor[Sensor.CHANNEL_CODE]     = unidecode.unidecode(sen_line[7:15].strip())
    sensor[Sensor.CHANNEL_ID]   = -1
    sensor[Sensor.INSTRUMENT_ID]= -1

    return Sensor(sensor)

