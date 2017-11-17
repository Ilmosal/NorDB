from datetime import date, timedelta
import string
import logging 
import sys
import psycopg2
import unidecode 

from nordb.core import usernameUtilities
from nordb.validation.stationValidation import validateStation
from nordb.validation.sitechanValidation import validateSiteChan

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

class SiteChan:
    """
    Class for site channel information. Comes from css sitechan format.


    Attributes:
        STATION_ID(int): Id of the station to which sitechan refers to value 0
        CHANNEL_CODE(int): channel code of the channel Value 1
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
    Method for converting a date in string format "YYYYDDD" or "YYYY-MMM-DD" to "YYYY-MM-DD".

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
    Method for reading station info to string array from a css site string

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

    channel[SiteChan.STATION_ID]        = unidecode.unidecode((chan_line[:7].strip()))                  #STATION_ID
    channel[SiteChan.CHANNEL_CODE]      = unidecode.unidecode((chan_line[7:17].strip()))               #CHANNEL_CODE
    channel[SiteChan.ON_DATE]           = unidecode.unidecode(stringToDate(chan_line[17:24].strip()))  #ON_DATE 
    channel[SiteChan.OFF_DATE]          = unidecode.unidecode(stringToDate(chan_line[35:42].strip()))  #OFF_DATE
    channel[SiteChan.CHANNEL_TYPE]      = unidecode.unidecode((chan_line[43:48].strip()))              #CHANNEL_TYPE
    channel[SiteChan.EMPLACEMENT_DEPTH] = unidecode.unidecode((chan_line[49:57].strip()))              #EMPLACEMENT_DEPTH
    channel[SiteChan.HORIZONTAL_ANGLE]  = unidecode.unidecode((chan_line[57:64].strip()))              #HORIZONTAL_ANGLE
    channel[SiteChan.VERTICAL_ANGLE]    = unidecode.unidecode((chan_line[64:71].strip()))              #VERTICAL_ANGLE
    channel[SiteChan.DESCRIPTION]       = unidecode.unidecode((chan_line[72:122].strip()))             #DESCRIPTION 
    channel[SiteChan.LOAD_DATE]         = unidecode.unidecode(stringToDate(chan_line[123:].strip()))   #LOAD_DATE 

    try:
        css_id = int(chan_line[25:33])
    except:
        logging.error("css_id not in a correct format: {0}".format(chan_line[25:33]))
        logging.error("Line: {0}".format(chan_line))
        return [None, None]

    return [channel, css_id]

def insertChan2Database(channel, css_id):
    """
    Method for inserting the sitechan information to the database.

    Args:
        channel([]): Array of all station related information in their correct spaces
        css_id(int): id for the css format which is different from the id in the database. Stupid, I know.

    Returns:
        True or False depending on if the operation was succesful
    """
    conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    cur = conn.cursor()

    try:
        cur.execute(CHANNEL_INSERT, channel)
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return False
 
    db_id = cur.fetchone()[0]

    try:
        cur.execute("INSERT INTO css_link (css_id, sitechan_id) VALUES (%s, %s)", (css_id, db_id))
    except:
        error.log("Link between table id {0} and css id {1} already exists".format(db_id, css_id))

    conn.commit()
    conn.close()

    return True

def insertStat2Database(station):
    """
    Method for inserting the information to the database.

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

def strChan2Chan(channel):
    """
    Method for creating a proper sitechan list from sitechan string array

    Args:
        channel (str[]): String array of all the data in sitechan file

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
    Method for creating a proper station list from station string array

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

def getNetworkID(network):
    """
    Method for inserting the information to the database.

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

def readChannels(f_channels, error_log):
    """
    Function for reading sitechan in css format and inserting them to the database

    Args:
        f_channels (file): the file that will be read into the database

    Returns:
        True or False depending if the sitechan was loaded into database succesfully
    """
    channels = []
    
    username = usernameUtilities.readUsername()
    
    for line in f_channels:
        channels.append(readSiteChanInfoToString(line))

    for chan in channels:
        if chan[1] is None:
            return("False")

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
    Method for reading stations in css format and inserting them to the database.

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
