"""
This module contains all functions and classes for reading a station file in `CSS3.0 format`_ and pushing them into the database.

.. _CSS3.0 format: ftp://ftp.pmel.noaa.gov/newport/lau/tphase/data/css_wfdisc.pdf

Functions and Classes
---------------------
"""

from datetime import date, timedelta
import string
import logging 
import sys
import psycopg2
import unidecode 

from nordb.core import usernameUtilities
from nordb.validation.stationValidation import validateStation
from nordb.validation.sitechanValidation import validateSiteChan
from nordb.validation.instrumentValidation import validateInstrument
from nordb.validation.sensorValidation import validateSensor
from nordb.validation import validationTools

MONTH_CONV = {  "Jan": "01",
                "Feb": "02",
                "Mar": "03",
                "Apr": "04",
                "May": "05",
                "Jun": "06",
                "Jul": "07",
                "Aug": "08",
                "Sep": "09",
                "Oct": "10",
                "Nov": "11",
                "Dec": "12"

}

STATION_INSERT = (  "INSERT INTO station " +
                        "(   station_code, on_date, off_date, " +
                            "latitude, longitude, elevation, " +
                            "station_name, station_type," +
                            "reference_station, north_offset, " +
                            "east_offset, load_date, network_id) " +
                    "VALUES " +
                        "(   %s, %s, %s, %s, %s, %s, %s, %s," +
                            "%s, %s, %s, %s, %s);" )

STATION_UPDATE = (
                    "UPDATE "
                    "   station "
                    "SET "
                    "   station_code = %s "
                    "   on_date = %s "
                    "   off_date = %s "
                    "   latitude = %s "
                    "   longitude = %s "
                    "   elevation = %s "
                    "   station_name = %s "
                    "   station_type = %s "
                    "   reference_station = %s "
                    "   north_offset = %s "
                    "   east_offset = %s "
                    "   load_date = %s "
                    "   network_id = %s "
                    "WHERE "
                    "   id = %s"
)

CHANNEL_INSERT = (  "INSERT INTO sitechan" +
                        "(      station_id, channel_code, on_date, off_date, " +
                        "       channel_type, emplacement_depth, " +
                        "       horizontal_angle, vertical_angle," +
                        "       description, load_date)" + 
                    "VALUES " +
                        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "  +
                    "RETURNING " +
                    "   id" )

FAKE_CHANNEL_LINE = (
                        "-1 {0}        -1 n       0.0000    0.0   90.0 % AUTOMATICALLY GENERATED CHANNEL PROBABLY NOT OK           -1",
                        "-1 {0}        -1 n       0.0000   90.0   90.0 % AUTOMATICALLY GENERATED CHANNEL PROBABLY NOT OK           -1",
                        "-1 {0}        -1 n       0.0000   -1.0    0.0 % AUTOMATICALLY GENERATED CHANNEL PROBABLY NOT OK           -1"
                    )

SENSOR_INSERT = (   "INSERT INTO sensor " +
                        "(  time, endtime, jdate, calratio, " +
                        "   calper, tshift, instant, lddate, " +
                        "   channel_id, instrument_id) " +
                    "VALUES " +
                        "(  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ")
                
INSTRUMENT_INSERT = (   "INSERT INTO instrument " +
                            "(  instrument_name, instrument_type, " +
                            "   band, digital, samprate, ncalib, " +
                            "   ncalper, dir, dfile, rsptype, " +
                            "   lddate) " +
                        "VALUES " +
                            "(  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " +
                        "RETURNING " +
                            "id") 

class Sensor:
    """
    Class for sensor information. Comes from css sensor format.

    :param array data: all the relevant data for Sensor in an array. These values are accessed by its numerations. 
    :ivar array data: all the relevant data for Sensor in an array. These values are accessed by its numerations.
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
    TIME = 0
    ENDTIME = 1
    JDATE = 2
    CALRATIO = 3
    CALPER = 4
    TSHIFT = 5
    INSTANT = 6
    LDDATE = 7
    CHANNEL_ID = 8
    INSTRUMENT_ID = 9
    ID = 10
    STATION_CODE = 11
    CHANNEL_CODE = 12

    def __init__(self, data):
        self.data = data

class Instrument:
    """
    Class for instrument information. Comes from css instrument format.

    :param array data: all the relevant data for Sensor in an array. These values are accessed by its numerations. 
    :ivar array data: all the relevant data for Sensor in an array. These values are accessed by its numerations.
    :ivar int INSTRUMENT_NAME: name of the instrument
    :ivar int INSTRUMENT_TYPE: type of the instrument
    :ivar int BAND: bandwidth of the instrument
    :ivar int DIGITAL: type of the instrument data
    :ivar int SAMPRATE: Sampling rate of the instrument
    :ivar int NCALIB: nominal calibration of the instrument
    :ivar int NCALPER: nominal calibration period of the instrument
    :ivar int DIR: directory the instrument response file
    :ivar int DFILE: name of the instrument response file
    :ivar int RSPTYPE: response type
    :ivar int LDDATE: load date
    :ivar int ID: id of the css file
    :ivar int CSS_ID: css id of th instrument
    """
    INSTRUMENT_NAME = 0
    INSTRUMENT_TYPE = 1
    BAND = 2 
    DIGITAL = 3
    SAMPRATE = 4
    NCALIB = 5
    NCALPER = 6
    DIR = 7
    DFILE = 8
    RSPTYPE = 9
    LDDATE = 10
    ID = 11
    CSS_ID = 12

    def __init__(self, data):
        self.data = data

class SiteChan:
    """
    Class for site channel information. Comes from css sitechan format.

    :param array data: all the relevant data for SiteChan in an array. These values are accessed by its numerations. 
    :ivar array data: all the relevant data for SiteChan in an array. These values are accessed by its numerations.
    :ivar int STATION_ID: Id of the station to which sitechan refers to. Value 0
    :ivar int CHANNEL_CODE: channel code of the channel. Value 1
    :ivar int ON_DATE: date when the station started working. Value 2
    :ivar int OFF_DATE: date when the station was closed. Value 3
    :ivar int CHANNEL_TYPE: type of the channel. Value 4
    :ivar int EMPLACEMENT_DEPTH: depth relative to station elevation. Value 5
    :ivar int HORIZONTAL_ANGLE: angle horizontally. Value 6
    :ivar int VERTICAL_ANGLE: angle verically. Value 7
    :ivar int DESCRIPTION: description of the channel. Value 8
    :ivar int LOAD_DATE: date of the time when this information was created. Value 9
    :ivar int ID: id of the sitechan in the database. Value 10
    :ivar int CSS_ID: id of the css id to which the sitechan is linked to. Value 11
    """
    STATION_ID = 0
    CHANNEL_CODE = 1
    ON_DATE = 2
    OFF_DATE = 3
    CHANNEL_TYPE = 4
    EMPLACEMENT_DEPTH = 5
    HORIZONTAL_ANGLE = 6
    VERTICAL_ANGLE = 7
    DESCRIPTION = 8
    LOAD_DATE = 9
    ID = 10
    CSS_ID = 11
 
    def __init__(self, data):
        self.data = data

class Station:
    """
    Class for information in station. Comes from the css site format.
 
    :param array data: all the relevant data for Station in an array. These values are accessed by its numerations. 
    :ivar array data: all the relevant data for Station in an array. These values are accessed by its numerations. 
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
    :ivar int NETWORK_ID: id of the network where the station belongs to

    """
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
    NETWORK_ID = 12
 
    def __init__(self, data):
        self.data = data

def stringToDate(sDate):
    """
    Function for converting a date in string format "YYYYDDD" or "YYYY-MMM-DD" to "YYYY-MM-DD".

    :param str sDate: date string
    :returns: the date in correct format as a string
    """
    try:
        if len(sDate) == 7:
            ndate = date(day=1, month=1, year=int(sDate[:4]))
            ndate += timedelta(days= int(sDate[4:]) - 1)
            rdate = ndate.strftime("%Y-%m-%d")
        elif len(sDate) == 11:
            rdate = sDate[:4] + "-" + MONTH_CONV[sDate[5:8]] + "-" + sDate[9:]
        elif sDate == "-1":
            rdate = ""
        else:
            rdate = ""
    except:
        return sDate
    return rdate
 
def readStationInfoToString(stat_line):
    """
    Function for reading station info to string array from a css site string

    :param str stat_line: css site string
    :returns: station string array    
    """
    station = []
    station.append(unidecode.unidecode(stat_line[0:6].strip()))                 #STATION_CODE
    station.append(unidecode.unidecode(stringToDate(stat_line[8:15].strip())))  #ON_DATE
    station.append(unidecode.unidecode(stringToDate(stat_line[17:24].strip()))) #OFF_DATE
    station.append(unidecode.unidecode(stat_line[26:34].strip()))               #LATITUDE
    station.append(unidecode.unidecode(stat_line[36:44].strip()))               #LONGITUDE
    station.append(unidecode.unidecode(stat_line[47:54].strip()))               #ELEVATION
    station.append(unidecode.unidecode(stat_line[55:106].strip()))              #STATION_NAME
    station.append(unidecode.unidecode(stat_line[106:108].strip()))             #STATION_TYPE
    station.append(unidecode.unidecode(stat_line[111:117].strip()))             #REFERENCE_STATION
    station.append(unidecode.unidecode(stat_line[119:127].strip()))             #NORTH_OFFSET
    station.append(unidecode.unidecode(stat_line[130:137].strip()))             #EAST_OFFSET
    station.append(unidecode.unidecode(stringToDate(stat_line[138:].strip())))  #LOAD_DATE

    return Station(station)

def readSiteChanInfoToString(chan_line):
    """
    Function for reading channel info to string array from css sitechan string

    :param str chan_line: css sitechan string
    :return: sitechan string array and css_id
    """
    channel = [None]*10

    channel[SiteChan.STATION_ID]        = unidecode.unidecode(chan_line[:7].strip())
    channel[SiteChan.CHANNEL_CODE]      = unidecode.unidecode(chan_line[7:17].strip())
    channel[SiteChan.ON_DATE]           = unidecode.unidecode(stringToDate(chan_line[17:24].strip()))
    channel[SiteChan.OFF_DATE]          = unidecode.unidecode(stringToDate(chan_line[35:42].strip()))
    channel[SiteChan.CHANNEL_TYPE]      = unidecode.unidecode(chan_line[43:48].strip())
    channel[SiteChan.EMPLACEMENT_DEPTH] = unidecode.unidecode(chan_line[49:57].strip())
    channel[SiteChan.HORIZONTAL_ANGLE]  = unidecode.unidecode(chan_line[57:64].strip())
    channel[SiteChan.VERTICAL_ANGLE]    = unidecode.unidecode(chan_line[64:71].strip())
    channel[SiteChan.DESCRIPTION]       = unidecode.unidecode(chan_line[72:122].strip())
    channel[SiteChan.LOAD_DATE]         = unidecode.unidecode(stringToDate(chan_line[123:].strip()))
    
    try:
        css_id = int(chan_line[25:33])
    except:
        logging.error("css_id not in a correct format: {0}".format(chan_line[25:33]))
        logging.error("Line: {0}".format(chan_line))
        return [None, None]

    return [SiteChan(channel), css_id]

def readSensorInfoToString(sen_line):
    """
    Function for reading sensor info to string array from css sensor string

    :param str sen_line:  css sensor string
    :return: sensor string array, channel id, instrument id and station_info
    """
    if sen_line[0] == "#":
        return [None, None, None, None]

    sensor = [None]*8

    sensor[Sensor.TIME]     = unidecode.unidecode(sen_line[15:33].strip())
    sensor[Sensor.ENDTIME]  = unidecode.unidecode(sen_line[35:51].strip())
    sensor[Sensor.JDATE]    = unidecode.unidecode(stringToDate(sen_line[71:78].strip()))
    sensor[Sensor.CALRATIO] = unidecode.unidecode(sen_line[78:96].strip())
    sensor[Sensor.CALPER]   = unidecode.unidecode(sen_line[95:112] .strip())
    sensor[Sensor.TSHIFT]   = unidecode.unidecode(sen_line[113:119].strip())
    sensor[Sensor.INSTANT]  = unidecode.unidecode(sen_line[120].strip())
    sensor[Sensor.LDDATE]   = unidecode.unidecode(stringToDate(sen_line[122:].strip()))

    try:
        instrument_id = int(sen_line[51:60].strip())
    except:
        logging.error("instrument_id not in a correct format: {0}".format(sen_line[51:60].strip()))
        logging.error("Line: {0}".format(sen_line))
        return [None, None, None, None]

    try:
        channel_id = int(sen_line[62:69].strip())
    except:
        logging.error("channel_id not in a correct format: {0}".format(sen_line[51:60].strip()))
        logging.error("Line: {0}".format(sen_line))
        return [None, None, None, None]

    station_info = sen_line[:15].strip()

    return [Sensor(sensor), instrument_id, channel_id, station_info]

def readInstrumentInfoToString(ins_line):
    """
    Function for reading instrument info to a strin array from a css instrument string 

    :param str ins_line: css intrument line
    :returns: instrument string array, instrument_id
    """
    instrument = [None]*11

    instrument[Instrument.INSTRUMENT_NAME]  = unidecode.unidecode(ins_line[8:58].strip())
    instrument[Instrument.INSTRUMENT_TYPE]  = unidecode.unidecode(ins_line[58:67].strip())
    instrument[Instrument.BAND]             = unidecode.unidecode(ins_line[67].strip())
    instrument[Instrument.DIGITAL]          = unidecode.unidecode(ins_line[69].strip())
    instrument[Instrument.SAMPRATE]         = unidecode.unidecode(ins_line[70:82].strip())
    instrument[Instrument.NCALIB]           = unidecode.unidecode(ins_line[82:100].strip())
    instrument[Instrument.NCALPER]          = unidecode.unidecode(ins_line[101:116].strip())
    instrument[Instrument.DIR]              = unidecode.unidecode(ins_line[117:182].strip())
    instrument[Instrument.DFILE]            = unidecode.unidecode(ins_line[182:215].strip())
    instrument[Instrument.RSPTYPE]          = unidecode.unidecode(ins_line[215:228].strip())
    instrument[Instrument.LDDATE]           = unidecode.unidecode(stringToDate(ins_line[228:].strip()))

    try:
        instrument_id = int(ins_line[:8].strip())
    except:
        logging.error("instrument_id not in a correct format: {0}".format(ins_line[:8].strip()))
        logging.error("Line: {0}".format(ins_line))
        return [None, None]
  
    return [Instrument(instrument), instrument_id]

def insertSen2Database(sensor):
    """
    Function for inserting the sensor array to the database

    :param Sensor sensor: sensor that will be inserted to the database
    :return: true or false depending on if the operation was successful or not 
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    try:
        cur.execute(SENSOR_INSERT, sensor.data)
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return False

    conn.commit()
    conn.close()

    return True

def insertIns2Database(instrument, instrument_id):
    """
    Function for inserting the instrument array to the database

    :param Instrument instrument: instrument that will be inserted to the database
    :returns: true or false depending on if the operation was successful or not 
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    try:
        cur.execute(INSTRUMENT_INSERT, instrument.data)
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return False

    db_id = cur.fetchone()[0]

    try:
        cur.execute("INSERT INTO instrument_css_link (css_id, instrument_id) VALUES (%s, %s)", (instrument_id, db_id))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return False

    conn.commit()
    conn.close()

    return True

def insertChan2Database(channel, css_id):
    """
    Function for inserting the sitechan array to the database.
        
    :param SiteChan channel: sitechan that will be inserted to the database
    :param int css_id: id for the css format which is different from the id in the database. Stupid, I know.
    :return: true or false depending on if the operation was succesful
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    try:
        cur.execute(CHANNEL_INSERT, channel.data)
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return False
 
    db_id = cur.fetchone()[0]

    try:
        cur.execute("INSERT INTO sitechan_css_link (css_id, sitechan_id) VALUES (%s, %s)", (css_id, db_id))
    except:
        logging.error("Link between table id {0} and css id {1} already exists".format(db_id, css_id))

    conn.commit()
    conn.close()

    return True

def insertStat2Database(station):
    """
    Function for inserting the information to the database. If the station with the given code already exists the function will replace the old one.

    :param Station station: station that will be inserted to the database
    :return: True or False depending on if the operation was succesful
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    search_stations = (
                        "SELECT " 
                        "   id "
                        "FROM "
                        "   station "
                        "WHERE "
                        "   station_code = %s "
                        "AND "
                        "   (off_date is null OR (off_date < %s OR on_date > %s ))"
                    
    )

    cur.execute(search_stations, (  station.data[station.STATION_CODE], 
                                    station.data[station.ON_DATE],
                                    station.data[station.OFF_DATE]))
    ans = cur.fetchone()

    if ans is not None:
        st_id = ans[0]
        station.data.append(st_id)
        try:
            cur.execute(STATION_UPDATE, station.data)
        except psycopg2.Error as e:
            logging.error(e.pgerror)
            return False
    else:

        try:
            cur.execute(STATION_INSERT, station.data)
        except psycopg2.Error as e:
            logging.error(e.pgerror)
            return False

    conn.commit()
    conn.close()

    return True

def strSen2Sen(sensor, instrument_id, channel_id, station_code):
    """
    Function for creating a proper Sensor list from sensor string array
    
    :param Sensor sensor: String array of all data in a sensor string array
    :return: The sensor array with info in correct format
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    try:
        cur.execute("SELECT instrument_id FROM instrument_css_link WHERE css_id = %s", (instrument_id,))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return None

    ans = cur.fetchone()

    if ans is None:
        logging.error("No instrument for sensor")
        return None

    ins_id = ans[0]
   
    try:
        cur.execute("SELECT sitechan_id FROM sitechan_css_link WHERE css_id = %s", (channel_id,))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return None

    ans = cur.fetchone()
 
    if ans is None:
        print("No channel for sensor. Generating a fake one. Sensor: {0} - {1}".format(station_code, sensor.data))
        if not genFakeChannel(station_code, channel_id):
            return None
        cur.execute("SELECT sitechan_id FROM sitechan_css_link WHERE css_id = %s", (channel_id, ))
        ans = cur.fetchone()

    cha_id = ans[0]

    conn.commit()
    conn.close()

    nsensor = [None]*10

    nsensor[Sensor.TIME]            = float(sensor.data[sensor.TIME])
    nsensor[Sensor.ENDTIME]         = float(sensor.data[sensor.ENDTIME])
    nsensor[Sensor.JDATE]           = date( year=int(sensor.data[sensor.JDATE][:4]),
                                            month=int(sensor.data[sensor.JDATE][5:7]),
                                            day=int(sensor.data[sensor.JDATE][8:]))
    nsensor[Sensor.CALRATIO]        = float(sensor.data[sensor.CALRATIO])
    nsensor[Sensor.CALPER]          = float(sensor.data[sensor.CALPER])
    nsensor[Sensor.TSHIFT]          = float(sensor.data[sensor.TSHIFT])
    nsensor[Sensor.INSTANT]         = sensor.data[sensor.INSTANT]
    nsensor[Sensor.LDDATE]          = date( year=int(sensor.data[sensor.LDDATE][:4]),
                                            month=int(sensor.data[sensor.LDDATE][5:7]),
                                            day=int(sensor.data[sensor.LDDATE][8:]))

    nsensor[Sensor.CHANNEL_ID]      = cha_id
    nsensor[Sensor.INSTRUMENT_ID]   = ins_id

    return Sensor(nsensor)

def strIns2Ins(instrument):
    """
    Function for creating a proper instrument list from :class:`.Instrument`.

    :param Instrument instrument: Instrument object which's values will be converted into the correct formats
    :returns: An :class:`.Instrument` object with info in correct format
    """
    ninstrument = [None]*11

    ninstrument[Instrument.INSTRUMENT_NAME] = instrument.data[instrument.INSTRUMENT_NAME]
    ninstrument[Instrument.INSTRUMENT_TYPE] = instrument.data[instrument.INSTRUMENT_TYPE]
    ninstrument[Instrument.BAND]            = instrument.data[instrument.BAND]
    ninstrument[Instrument.DIGITAL]         = instrument.data[instrument.DIGITAL]
    ninstrument[Instrument.SAMPRATE]        = float(instrument.data[instrument.SAMPRATE])
    ninstrument[Instrument.NCALIB]          = float(instrument.data[instrument.NCALIB])
    ninstrument[Instrument.NCALPER]         = float(instrument.data[instrument.NCALPER])
    ninstrument[Instrument.DIR]             = instrument.data[instrument.DIR]
    ninstrument[Instrument.DFILE]           = instrument.data[instrument.DFILE]
    ninstrument[Instrument.RSPTYPE]         = instrument.data[instrument.RSPTYPE]
    ninstrument[Instrument.LDDATE]          = date( year=int(instrument.data[instrument.LDDATE][:4]),
                                                    month=int(instrument.data[instrument.LDDATE][5:7]),
                                                    day=int(instrument.data[instrument.LDDATE][8:]))

    return Instrument(ninstrument)

def strChan2Chan(channel):
    """
    Function for creating a proper sitechan list from sitechan string array

    :param SiteChan channel: SiteChan object which's values will be converted into the correct formats
    :return: A :class:`.SiteChan` object with info in correct format

    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id FROM station WHERE STATION_CODE = %s", (channel.data[SiteChan.STATION_ID],))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return None

    ans = cur.fetchone()

    if ans is None:
        logging.error("No station for channel")
        return None

    station_id = ans[0]
    
    conn.commit()
    conn.close()

    nchannel = [None]*10

    nchannel[SiteChan.STATION_ID] = station_id
    nchannel[SiteChan.CHANNEL_CODE] = channel.data[channel.CHANNEL_CODE]
    if channel.data[channel.OFF_DATE] != "":
        nchannel[SiteChan.ON_DATE] = date(  year=int(channel.data[channel.ON_DATE][:4]), 
                                            month=int(channel.data[channel.ON_DATE][5:7]),
                                            day =int(channel.data[channel.ON_DATE][8:]))
    
    
    if channel.data[channel.OFF_DATE] != "":
        nchannel[SiteChan.OFF_DATE] =  (date(   year=int(channel.data[channel.OFF_DATE][:4]), 
                                                month=int(channel.data[channel.OFF_DATE][5:7]),
                                                day=int(channel.data[channel.OFF_DATE][8:])))   
    nchannel[SiteChan.CHANNEL_TYPE] = channel.data[channel.CHANNEL_TYPE]
    nchannel[SiteChan.EMPLACEMENT_DEPTH] = float(channel.data[channel.EMPLACEMENT_DEPTH])
    nchannel[SiteChan.HORIZONTAL_ANGLE]  = float(channel.data[channel.HORIZONTAL_ANGLE])
    nchannel[SiteChan.VERTICAL_ANGLE]    = float(channel.data[channel.VERTICAL_ANGLE])
    nchannel[SiteChan.DESCRIPTION]       = channel.data[channel.DESCRIPTION]  
   
    if channel.data[channel.LOAD_DATE] != "":
        nchannel[SiteChan.LOAD_DATE]         = date(year=int(channel.data[channel.LOAD_DATE][:4]), 
                                                    month=int(channel.data[channel.LOAD_DATE][5:7]),
                                                    day =int(channel.data[channel.LOAD_DATE][8:]))
    return SiteChan(nchannel)

def strStat2Stat(station, network_id):
    """
    Function for creating a proper station list from station string array

    :param Station station: Station object which's values will be converted into the correct formats
    :return: The station array with info in correct format
    """
    nstation = []

    nstation.append(station.data[station.STATION_CODE])                     
    nstation.append(date(   year=int(station.data[station.ON_DATE][:4]), 
                            month=int(station.data[station.ON_DATE][5:7]),
                            day=int(station.data[station.ON_DATE][8:])))   
    if station.data[station.OFF_DATE] != "":
        nstation.append(date(   year=int(station.data[station.OFF_DATE][:4]), 
                            month=int(station.data[station.OFF_DATE][5:7]),
                            day=int(station.data[station.OFF_DATE][8:])))   
    else:   
        nstation.append(None)
    nstation.append(float(station.data[station.LATITUDE]))            
    nstation.append(float(station.data[station.LONGITUDE]))  
    nstation.append(float(station.data[station.ELEVATION]))
    nstation.append(station.data[station.STATION_NAME])
    nstation.append(station.data[station.STATION_TYPE])
    nstation.append(station.data[station.REFERENCE_STATION])
    nstation.append(float(station.data[station.NORTH_OFFSET]))
    nstation.append(float(station.data[station.EAST_OFFSET]))

    try:
        nstation.append(date(   year=int(station.data[station.LOAD_DATE][:4]), 
                            month=int(station.data[station.LOAD_DATE][5:7]),
                            day=int(station.data[station.LOAD_DATE][8:])))   
    except ValueError:
        print(station)
    nstation.append(network_id)

    return Station(nstation)

def genFakeChannel(stat_code, chan_id):
    """
    Function for generating a fake sitechan obj to insert to the database to quarantee that all sensors can get in the database.

    :param int stat_id: id of the station to which the channel is inserted
    :param array chan_id: list of related sensor information 
    :return: True or False depending on if the operation was succesful  
    """
    whitespace = " " * (22 - len(stat_code.strip()))

    sitechanline = stat_code.strip() + whitespace

    chan_id_str = ((8-len(str(chan_id))) * " ") + str(chan_id)
    
    channel_line_str = ""

    if stat_code[-1] == "n": 
        channel_line_str += FAKE_CHANNEL_LINE[0].format(chan_id_str)
    elif stat_code[-1] == "e":
        channel_line_str += FAKE_CHANNEL_LINE[1].format(chan_id_str)
    elif stat_code[-1] == "z":
        channel_line_str += FAKE_CHANNEL_LINE[2].format(chan_id_str)
    else:
        logging.error("No valid fake lines")
        return False 

    if stat_code == 8:
        sitechanline += channel_line_str
    else:
         sitechanline += channel_line_str[1:]

    chan = readSiteChanInfoToString(sitechanline)

    tmp_chan = strChan2Chan(chan[0])
    if tmp_chan is None:
        logging.error("Problem parsing channel: \n{0}".format(chan))
        return False
    else:    
        insertChan2Database(tmp_chan, chan[1])

    return True
    
def getNetworkID(network):
    """
    Function for inserting the information to the database.

    :param array station: Array of all station related information in their correct spaces
    :return: True or False depending on if the operation was succesful
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT id FROM network WHERE network = %s", (network.strip(),))
    ans = cur.fetchone()

    if ans is None:
        cur.execute("INSERT INTO network (network) VALUES (%s) RETURNING id", (network.strip(),))
        ans = cur.fetchone()

    conn.commit()
    conn.close()

    return ans[0]

def readSensors(f_sensors, error_log):
    """
    Function for reading sensors in css format and inserting them to the database

    :param file f_sensors: file that will be read into the database
    :param str error_log: name of the errorlog
    :returns: True or False depending if the f_sensors was loaded into database succesfully
    """
    sensors = []

    sensors.append(readSensorInfoToString(line))

    for sen in sensors:
        if sen[0] is None:
            continue
        
        if not validateSensor(sen[0]):
            print("Sitechan validation failed! Check error log {0} for more details.".format(error_log))
            return False
   
    for sen in sensors:
        if sen[0] is None:
            continue

        tmp_sen = strSen2Sen(sen[0], sen[1], sen[2], sen[3])

        if tmp_sen is None:
            logging.error("Problem parsing sensor: \n {0}".format(sen))
        else:
            insertSen2Database(tmp_sen)

    return True

def readInstruments(f_instruments, error_log):
    """
    Function for reading instrument in css format and inserting them to the database

    :param file f_instruments: the file that will be read into the database
    :returns: True or False depending on if the f_instruments was loaded in to database succesfully
    """
    instruments = []

    for line in f_instruments:
        instruments.append(readInstrumentInfoToString(line))

    for ins in instruments:
        if ins[0] is None:
            return False

        if not validateInstrument(ins[0]):
            print("Instrument validation failed! Check error log {0} for more details.".format(error_log))
            return False


    for ins in instruments:
        tmp_ins = strIns2Ins(ins[0])

        if tmp_ins is None:
            logging_error("Problem parsing instrument: \n{0}".format(ins))
        else:
            insertIns2Database(tmp_ins, ins[1])

    return True

def readChannels(f_channels, error_log):
    """
    Function for reading sitechan in css format and inserting them to the database

    :param file f_channels: the file that will be read into the database
    :returns: True or False depending on if the f_channels was loaded into database succesfully
    """
    channels = []
    
    for line in f_channels:
        channels.append(readSiteChanInfoToString(line))

    for chan in channels:
        if chan[1] is None:
            continue

        if not validateSiteChan(chan[0]):
            print("Sitechan validation failed! Check error log {0} for more details.".format(error_log))
            return False

    for chan in channels:
        tmp_chan = strChan2Chan(chan[0])
        if tmp_chan is None:
            logging.error("Problem parsing channel: \n{0}".format(chan))
        else:    
            insertChan2Database(tmp_chan, chan[1])

    return True

def readStations(f_stations, network, error_log):
    """
    Function for reading stations in css format and inserting them to the database.

    :param file f_stations: the file that will be read into the database
    :return: True or False depending on if the station was loaded into the database succesfully
    """
    stations = []

    for line in f_stations:
        stations.append(readStationInfoToString(line))

    for stat in stations:
        if not validateStation(stat):
            print("Station validation failed! Check error log {0} for more details.".format(error_log))
            return False

    network_id = getNetworkID(network) 

    for stat in stations:
        insertStat2Database(strStat2Stat(stat, network_id))

    return True
