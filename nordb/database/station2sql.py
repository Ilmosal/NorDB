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
username = ""

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
                    "             -1 {0}       -1 n       0.0000    0.0   90.0 % AUTOMATICALLY GENERATED CHANNEL PROBABLY NOT OK           -1",
                    "             -1 {0}       -1 n       0.0000   90.0   90.0 % AUTOMATICALLY GENERATED CHANNEL PROBABLY NOT OK           -1",
                    "             -1 {0}       -1 n       0.0000   -1.0    0.0 % AUTOMATICALLY GENERATED CHANNEL PROBABLY NOT OK           -1"
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

    Attributes:
        TIME(int): epoch time of start of recording period
        ENDTIME(int): epoch time of end of recording period
        JDATE(int): julian date
        CALRATIO(int): calibration
        CALPER(int): calibration period
        TSHIFT(int): correction to data processing time
        INSTANT(int): (y/n) discrete/continuing snapshot
        LDDATE (int):
        ID(int): id of the sensor
        CHANNEL_ID(int): id of the channel to which sensor refers to. 
        INTRUMENT_ID(int): id of the instrument to which the sensor refers to. 
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

class Instrument:
    """
    Class for instrument information. Comes from css instrument format.

    Attributes:
        INSTRUMENT_NAME
        INSTRUMENT_TYPE 
        BAND
        DIGITAL
        SAMPRATE
        NCALIB
        NCALPER
        DIR
        DFILE
        RSPTYPE
        LDDATE
        ID
        CSS_ID
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

class SiteChan:
    """
    Class for site channel information. Comes from css sitechan format.


    Attributes:
        STATION_ID(int): Id of the station to which sitechan refers to. Value 0
        CHANNEL_CODE(int): channel code of the channel. Value 1
        ON_DATE(int): date when the station started working. Value 2
        OFF_DATE(int): date when the station was closed. Value 3
        CHANNEL_TYPE (int): type of the channel. Value 4
        EMPLACEMENT_DEPTH (int): depth relative to station elevation. Value 5
        HORIZONTAL_ANGLE (int): angle horizontally. Value 6
        VERTICAL_ANGLE (int): angle verically. Value 7
        DESCRIPTION (int): description of the channel. Value 8
        LOAD_DATE (int): date of the time when this information was created. Value 9
        ID (int): id of the sitechan in the database. Value 10
        CSS_ID(int): id of the css id to which the sitechan is linked to. Value 11
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
    

class Station:
    """
    Class for information in station. Comes from the css site format.
  
    Attributes:
        STATION_CODE(int): code of the station. Value 0
        ON_DATE(int): date when the station started working. Value 1 
        OFF_DATE(int): date when the station was closed. Value 2
        LATITUDE(int): latitude of the station. Value 3
        LONGITUDE(int): longitude of the staion. Value 4
        ELEVATION(int): elevation of the station. Value 5
        STATION_NAME(int): the whole name of the station. Value 6
        STATION_TYPE(int): 2 letter string of the type of the station. Value 7
        REFERENCE_STATION (int): if the station is a part of an array, this is the reference to the station. Value 8
        NORTH_OFFSET (int): if the station is a part of an array, this is the offset of the north to the main station in km. Value 9
        EAST_OFFSET (int): if the station is a part of an array, this is the offset of the east to the main station in km. Value 10
        LOAD_DATE (int): date of the time when this information was created. Value 11
        NETWORK_ID (int): id of the network where the station belongs to

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

def stringToDate(sDate):
    """
    Function for converting a date in string format "YYYYDDD" or "YYYY-MMM-DD" to "YYYY-MM-DD".

    Args:
        sDate(str): date string

    Returns:
        The date in correct format as a string
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

    Args:
        stat_line (str): css site string
    
    Returns:
        station (str[]): station string array    
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

    return station

def readSiteChanInfoToString(chan_line):
    """
    Function for reading channel info to string array from css sitechan string

    Args:
        chan_line(str): css sitechan string

    Returns:
        sitechan string array and css_id
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

    return [channel, css_id]

def readSensorInfoToString(sen_line):
    """
    Function for reading sensor info to string array from css sensor string

    Args:
        sen_line(str):  css sensor string

    Returns:
'       sensor string array, channel id, instrument id
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
    sensor[Sensor.INSTANT]  = unidecode.unidecode(sen_line[121].strip())
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

    station_info = sen_line[:9]

    return [sensor, instrument_id, channel_id, station_info]

def readInstrumentInfoToString(ins_line):
    """
    Function for reading instrument info to a strin array from a css instrument string 

    Args:
        ins_line(str): css intrument line

    Returns:
        instrument string array, instrument_id
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
  
    return [instrument, instrument_id]

def insertSen2Database(sensor):
    """
    Function for inserting the sensor array to the database

    Args:
        sensor(str[]): Array of all sensor related information
        
    Returns:
        True or False depending on if the operation was successful or not 
    """
    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Could not connect to database!")
        sys.exit()

    cur = conn.cursor()

    try:
        cur.execute(SENSOR_INSERT, sensor)
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return False

    conn.commit()
    conn.close()

    return True

def insertIns2Database(instrument, instrument_id):
    """
    Function for inserting the instrument array to the database

    Args:
        instrument(str[]): Array of all instrument related information
        
    Returns:
        True or False depending on if the operation was successful or not 
    """
    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Could not connect to database!")
        sys.exit()

    cur = conn.cursor()

    try:
        cur.execute(INSTRUMENT_INSERT, instrument)
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

    Args:
        channel([]): Array of all station related information in their correct spaces
        css_id(int): id for the css format which is different from the id in the database. Stupid, I know.

    Returns:
        True or False depending on if the operation was succesful
    """
    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Could not connect to database!")
        sys.exit()

    cur = conn.cursor()

    try:
        cur.execute(CHANNEL_INSERT, channel)
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
    Function for inserting the information to the database.

    Args:
        station([]): Array of all station related information in their correct spaces

    Returns:
        True or False depending on if the operation was succesful
    """
    conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    cur = conn.cursor()

    try:
        cur.execute(STATION_INSERT, station)
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return False
    conn.commit()
    conn.close()

    return True

def strSen2Sen(sensor, instrument_id, channel_id, station_code):
    """
    Function for creating a proper Sensor list from sensor string array

    Args:
        sensor (str[]):String array of all data in a sensor string array

    Returns:
        The sensor array with info in correct format
    """
    try: 
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to database")
        sys.exit()

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
        logging.error("No channel for sensor. Generating a fake one.")
        if not genFakeChannel(station_code, channel_id):
            return None
        cur.execute("SELECT sitechan_id FROM sitechan_css_link WHERE css_id = %s", (channel_id, ))
        ans = cur.fetchone()

    cha_id = ans[0]

    conn.commit()
    conn.close()

    nsensor = [None]*10

    nsensor[Sensor.TIME]            = float(sensor[Sensor.TIME])
    nsensor[Sensor.ENDTIME]         = float(sensor[Sensor.ENDTIME])
    nsensor[Sensor.JDATE]           = date( year=int(sensor[Sensor.JDATE][:4]),
                                            month=int(sensor[Sensor.JDATE][5:7]),
                                            day=int(sensor[Sensor.JDATE][8:]))
    nsensor[Sensor.CALRATIO]        = float(sensor[Sensor.CALRATIO])
    nsensor[Sensor.CALPER]          = float(sensor[Sensor.CALPER])
    nsensor[Sensor.TSHIFT]          = float(sensor[Sensor.TSHIFT])
    nsensor[Sensor.INSTANT]         = sensor[Sensor.INSTANT]
    nsensor[Sensor.LDDATE]          = date( year=int(sensor[Sensor.LDDATE][:4]),
                                            month=int(sensor[Sensor.LDDATE][5:7]),
                                            day=int(sensor[Sensor.LDDATE][8:]))

    nsensor[Sensor.CHANNEL_ID]      = cha_id
    nsensor[Sensor.INSTRUMENT_ID]   = ins_id

    return nsensor

def strIns2Ins(instrument):
    """
    Function for creating a proper instrument list from instrument string array

    Args:
        instrument (str[]): String array of all data in instrument strin array
    
    Returns:
        The instrument array with info in correct format
    """
    ninstrument = [None]*11

    ninstrument[Instrument.INSTRUMENT_NAME] = instrument[Instrument.INSTRUMENT_NAME]
    ninstrument[Instrument.INSTRUMENT_TYPE] = instrument[Instrument.INSTRUMENT_TYPE]
    ninstrument[Instrument.BAND]            = instrument[Instrument.BAND]
    ninstrument[Instrument.DIGITAL]         = instrument[Instrument.DIGITAL]
    ninstrument[Instrument.SAMPRATE]        = float(instrument[Instrument.SAMPRATE])
    ninstrument[Instrument.NCALIB]          = float(instrument[Instrument.NCALIB])
    ninstrument[Instrument.NCALPER]         = float(instrument[Instrument.NCALPER])
    ninstrument[Instrument.DIR]             = instrument[Instrument.DIR]
    ninstrument[Instrument.DFILE]           = instrument[Instrument.DFILE]
    ninstrument[Instrument.RSPTYPE]         = instrument[Instrument.RSPTYPE]
    ninstrument[Instrument.LDDATE]          = date( year=int(instrument[Instrument.LDDATE][:4]),
                                                    month=int(instrument[Instrument.LDDATE][5:7]),
                                                    day=int(instrument[Instrument.LDDATE][8:]))

    return ninstrument

def strChan2Chan(channel):
    """
    Function for creating a proper sitechan list from sitechan string array

    Args:
        channel (str[]): String array of all the data in sitechan string array

    Returns:
        The sitechan array with info in correct format

    """
    conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    cur = conn.cursor()

    try:
        cur.execute("SELECT id FROM station WHERE STATION_CODE = %s", (channel[SiteChan.STATION_ID],))
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
    nchannel[SiteChan.CHANNEL_CODE] = channel[SiteChan.CHANNEL_CODE]
    if channel[SiteChan.OFF_DATE] != "":
        nchannel[SiteChan.ON_DATE] = date(  year=int(channel[SiteChan.ON_DATE][:4]), 
                                            month=int(channel[SiteChan.ON_DATE][5:7]),
                                            day =int(channel[SiteChan.ON_DATE][8:]))
    
    
    if channel[SiteChan.OFF_DATE] != "":
        nchannel[SiteChan.OFF_DATE] =  (date(   year=int(channel[SiteChan.OFF_DATE][:4]), 
                                                month=int(channel[SiteChan.OFF_DATE][5:7]),
                                                day=int(channel[SiteChan.OFF_DATE][8:])))   
    nchannel[SiteChan.CHANNEL_TYPE] = channel[SiteChan.CHANNEL_TYPE]
    nchannel[SiteChan.EMPLACEMENT_DEPTH] = float(channel[SiteChan.EMPLACEMENT_DEPTH])
    nchannel[SiteChan.HORIZONTAL_ANGLE]  = float(channel[SiteChan.HORIZONTAL_ANGLE])
    nchannel[SiteChan.VERTICAL_ANGLE]    = float(channel[SiteChan.VERTICAL_ANGLE])
    nchannel[SiteChan.DESCRIPTION]       = channel[SiteChan.DESCRIPTION]  
   
    if channel[SiteChan.LOAD_DATE] != "":
        nchannel[SiteChan.LOAD_DATE]         = date(year=int(channel[SiteChan.LOAD_DATE][:4]), 
                                                    month=int(channel[SiteChan.LOAD_DATE][5:7]),
                                                    day =int(channel[SiteChan.LOAD_DATE][8:]))
    return nchannel

def strStat2Stat(station, network_id):
    """
    Function for creating a proper station list from station string array

    Args:
        station (str[]): String array of all the data in site file

    Returns:
        The station array with info in correct format
    """
    nstation = []

    nstation.append(station[Station.STATION_CODE])                     
    nstation.append(date(   year=int(station[Station.ON_DATE][:4]), 
                            month=int(station[Station.ON_DATE][5:7]),
                            day=int(station[Station.ON_DATE][8:])))   
    if station[Station.OFF_DATE] != "":
        nstation.append(date(   year=int(station[Station.OFF_DATE][:4]), 
                            month=int(station[Station.OFF_DATE][5:7]),
                            day=int(station[Station.OFF_DATE][8:])))   
    else:   
        nstation.append(None)
    nstation.append(float(station[Station.LATITUDE]))            
    nstation.append(float(station[Station.LONGITUDE]))  
    nstation.append(float(station[Station.ELEVATION]))
    nstation.append(station[Station.STATION_NAME])
    nstation.append(station[Station.STATION_TYPE])
    nstation.append(station[Station.REFERENCE_STATION])
    nstation.append(float(station[Station.NORTH_OFFSET]))
    nstation.append(float(station[Station.EAST_OFFSET]))

    try:
        nstation.append(date(   year=int(station[Station.LOAD_DATE][:4]), 
                            month=int(station[Station.LOAD_DATE][5:7]),
                            day=int(station[Station.LOAD_DATE][8:])))   
    except ValueError:
        print(station)
    nstation.append(network_id)

    return nstation

def genFakeChannel(stat_code, chan_id):
    """
    Function for generating a fake sitechan obj to insert to the database to quarantee that all sensors can get in the database.

    Args:
        stat_id(int): id of the station to which the channel is inserted
        chan_id(list()): list of related sensor information 
    Returns:
        True or False depending on if the operation was succesfull   
    """
    sitechanline = stat_code    

    chan_id_str = ((8-len(str(chan_id))) * " ") + str(chan_id)

    if stat_code[-1] == "n": 
        sitechanline += FAKE_CHANNEL_LINE[0].format(chan_id_str)
    elif stat_code[-1] == "e":
        sitechanline += FAKE_CHANNEL_LINE[1].format(chan_id_str)
    elif stat_code[-1] == "z":
        sitechanline += FAKE_CHANNEL_LINE[2].format(chan_id_str)
    else:
        logging.error("No valid fake lines")
        return False 

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

    Args:
        station([]): Array of all station related information in their correct spaces

    Returns:
        True or False depending on if the operation was succesful
    """
    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("error connecting to database")
        return -1
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

    Args:
        f_sensors(file): file that will be read into the database
        error_log (str): name of the errorlog
    
    Returns:
        True or False depending if the f_sensors was loaded into database succesfully
    """
    sensors = []

    username = usernameUtilities.readUsername()

    for line in f_sensors:
        sensors.append(readSensorInfoToString(line))

    for sen in sensors:
        if sen[0] is None:
            continue
        
        if not validateSensor(sen[0]):
            print("Sitechan validation failed! Check error log {0} for more details.".format(error_log))
            return False
   
    for sen in sensors:
        tmp_sen = strSen2Sen(sen[0], sen[1], sen[2], sen[3])

        if tmp_sen is None:
            logging.error("Problem parsing sensor: \n {0}".format(sen))
        else:
            insertSen2Database(tmp_sen)

    return True

def readInstruments(f_instruments, error_log):
    """
    Function for reading instrument in css format and inserting them to the database

    Args:
        f_instruments (file): the file that will be read into the database

    Returns:
        True or False depending on if the f_instruments was loaded in to database succesfully
    """
    instruments = []

    username = usernameUtilities.readUsername()

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

    Args:
        f_channels (file): the file that will be read into the database

    Returns:
        True or False depending on if the f_channels was loaded into database succesfully
    """
    channels = []
    
    username = usernameUtilities.readUsername()
    
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

    Args:
        f_stations (file): the file that will be read into the database
    
    Returns:
        True or False depending on if the station was loaded into the database succesfully
    """
    stations = []

    for line in f_stations:
        stations.append(readStationInfoToString(line))

    for stat in stations:
        if not validateStation(stat):
            print("Station validation failed! Check error log {0} for more details.".format(error_log))
            return False

    username = usernameUtilities.readUsername()
    
    network_id = getNetworkID(network) 

    for stat in stations:
        insertStat2Database(strStat2Stat(stat, network_id))

    return True
