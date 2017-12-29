"""
This module contains all functions for getting station information from the database and writing it into the database.

Functions and Classes
---------------------
"""

import logging
import psycopg2

from nordb.database.station2sql import Station
from nordb.core import usernameUtilities
from nordb.core.utils import addFloat2String 
from nordb.core.utils import addInteger2String
from nordb.core.utils import addString2String

username = ""

SELECT_STATION =    (
                        "SELECT " +
                            "station_code, on_date, off_date, latitude, " +
                            "longitude, elevation, station_name, station_type, " +
                            "reference_station, north_offset, east_offset, " +
                            "load_date, id " +
                        "FROM " +
                            "station " +
                        "WHERE " +
                            "id = %s" 
                    )

def createStationString(station):
    """
    Function for creating a css stations string from a Station object.

    :param Station station: Station object that will be parsed into a string
    :returns: The station string in a css format
    """
    stationString = ""
    stationString += addString2String(station[Station.STATION_CODE], 8, '<')

    stationString += addInteger2String(station[Station.ON_DATE].year, 5, '<') 
    stationString += addInteger2String(station[Station.ON_DATE].timetuple().tm_yday, 3, '0') 
    
    stationString += "  "

    if station[Station.OFF_DATE] is None:
        stationString += addInteger2String(-1, 7, '>')
    else:
        stationString += addInteger2String(station[Station.OFF_DATE].year, 4, '<') 
        stationString += addInteger2String(station[Station.OFF_DATE].timetuple().tm_yday, 3, '0') 

    stationString += "  "
    stationString += addFloat2String(station[Station.LATITUDE], 8, 4, '>')
    stationString += "  "
    stationString += addFloat2String(station[Station.LONGITUDE], 8, 4, '>')

    stationString += " "
    stationString += addFloat2String(station[Station.ELEVATION], 9, 4, '>')

    stationString += " "
    stationString += addString2String(station[Station.STATION_NAME], 50, '<')

    stationString += " "
    stationString += addString2String(station[Station.STATION_TYPE], 2, '<')

    stationString += "   "
    stationString += addString2String(station[Station.REFERENCE_STATION], 8, '<')

    stationString += " "
    stationString += addFloat2String(station[Station.NORTH_OFFSET], 7, 4, '>')

    stationString += "   "
    stationString += addFloat2String(station[Station.EAST_OFFSET], 7, 4, '>')

    stationString += " "
    stationString += addString2String(station[Station.LOAD_DATE].strftime("%Y-%b-%d"), 10, '<')

    return stationString

def readStation(station_id):
    """
    Function for reading a station from database by id.

    :param int station_id: id of the station wanted
    :returns: station as a list 
    """
    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return None

    cur = conn.cursor()

    cur.execute(SELECT_STATION, (station_id,))

    ans = cur.fetchone()

    conn.close()

    return ans

def sql2station(station_ids, output_path):
    """
    Function for reading stations from the database and dumping them to a stations.site file

    :param array station_ids: Array of Integers
    :param str output_path: path to the output file
    """
    username = usernameUtilities.readUsername() 

    stations = []
    
    for station_id in station_ids:
        stations.append(readStation(station_id))

    f = open(output_path, 'w')

    for station in stations:
        f.write(createStationString(station) + '\n')

def writeAllStations(output_path):
    """
    Function for writing all stations to a site file.

    :param str output_path: path to output file
    """
    username = usernameUtilities.readUsername() 

    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return 

    cur = conn.cursor()

    cur.execute("SELECT id FROM station ORDER BY station_code;")

    ans = cur.fetchall()

    conn.close()
    
    station_ids = []

    if not ans:
        print("No stations in the database!")
        return

    for a in ans:
        station_ids.append(a[0])

    sql2station(station_ids, output_path)
