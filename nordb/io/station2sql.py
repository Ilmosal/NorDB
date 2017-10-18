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
        station_code (str): code of the station. Maximum on 6 letter
        on_date (date): date when the station started working
        off_date (date): date when the station was closed
        latitude (float): latitude of the station    
        longitude (float): longitude of the staion
        elevation (float): elevation of the station
        station_name (str): the whole name of the station
        station_type (str): 2 letter string of the type of the station
        reference_station (int): if the station is a part of an array, this is the reference to the station
        north_offset (float): if the station is a part of an array, this is the offset of the north to the main station in km
        east_offset (float): if the station is a part of an array, this is the offset of the east to the main station in km
        load_date (date): date of the time when this information was created

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

    def __init__(self, station_info):
        self.station_code = station_info[Station.STATION_CODE]
        self.on_date = station_info[Station.ON_DATE]
        self.off_date = station_info[Station.OFF_DATE]
        self.latitude = station_info[Station.LATITUDE]
        self.longitude = station_info[Station.LONGITUDE]  
        self.elevation = station_info[Station.ELEVATION]
        self.station_name = station_info[Station.STATION_NAME]
        self.station_type = station_info[Station.STATION_TYPE]
        self.reference_station = station_info[Station.REFERENCE_STATION]
        self.north_offset = station_info[Station.NORTH_OFFSET]
        self.east_offset = station_info[Station.EAST_OFFSET]
        self.load_date = station_info[Station.LOAD_DATE]

def stringToDate(sDate):
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
    conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    cur = conn.cursor()

    try:
        cur.execute(STATION_INSERT, station)
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return -1

    conn.commit()
    conn.close()

    return 1

def strStat2Stat(station):
    """
    Method for creating a proper station list from station string array

    Args:
        station (str[]): String array of all the data in site file

    Returns:
        The station array with info on correct format
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
