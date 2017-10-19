from datetime import date, timedelta
import string
import logging 

import psycopg2

from nordb.core import usernameUtilities
from nordb.validation.stationValidation import validateStation

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

STATION_INSERT = "INSERT INTO station (station_code, on_date, off_date, latitude, longitude, elevation, station_name, station_type, reference_station, north_offset, east_offset, load_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

class Station:
    """
    Class for information in station. Comes from the css site format.

    Args:
        station_info(str[]): a list of strings that have been validated as working
  
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

def stringToDate(sDate):
    """
    Method for converting a date in string format "YYYYDDD" or "YYYY-MMM-DD" to "YYYY-MM-DD".

    Args:
        sDate(str): date string

    Returns:
        The date in correct format as a string
    """
    if len(sDate) == 7:
        ndate = date(day=1, month=1, year=int(sDate[:4]))
        ndate += timedelta(days= int(sDate[4:]) - 1)
        rdate = ndate.strftime("%Y-%m-%d")
    elif len(sDate) == 11:
        rdate = sDate[:4] + "-" + MONTH_CONV[sDate[5:8]] + "-" + sDate[9:]
    elif sDate == "-1":
        rdate = ""
    else:
        rdate = None
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
    station.append(stat_line[0:6].strip().decode("ascii","ignore"))                 #STATION_CODE
    station.append(stringToDate(stat_line[8:15].strip().decode("ascii","ignore")))  #ON_DATE
    station.append(stringToDate(stat_line[17:24].strip().decode("ascii","ignore"))) #OFF_DATE
    station.append(stat_line[26:34].strip().decode("ascii","ignore"))               #LATITUDE
    station.append(stat_line[36:44].strip().decode("ascii","ignore"))               #LONGITUDE
    station.append(stat_line[47:54].strip().decode("ascii","ignore"))               #ELEVATION
    station.append(stat_line[55:106].strip().decode("ascii","ignore"))              #STATION_NAME
    station.append(stat_line[106:108].strip().decode("ascii","ignore"))             #STATION_TYPE
    station.append(stat_line[111:117].strip().decode("ascii","ignore"))             #REFERENCE_STATION
    station.append(stat_line[119:127].strip().decode("ascii","ignore"))             #NORTH_OFFSET
    station.append(stat_line[130:137].strip().decode("ascii","ignore"))             #EAST_OFFSET
    station.append(stringToDate(stat_line[138:].strip().decode("ascii","ignore")))  #LOAD_DATE

    return station

def insert2Database(station):
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

def strStat2Stat(station):
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
    nstation.append(date(   year=int(station[Station.LOAD_DATE][:4]), 
                            month=int(station[Station.LOAD_DATE][5:7]),
                            day=int(station[Station.LOAD_DATE][8:])))   

    return nstation

def readStations(f_stations):
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
            logging.error("Station Validation Failed!")
            return False

    username = usernameUtilities.readUsername()
    
    nStations = []

    for stat in stations:
        nStations.append(strStat2Stat(stat))

    for stat in nStations:
        insert2Database(stat)

    return True
