"""
This module contains all functions for getting station information from the database and writing it into the database.

Functions and Classes
---------------------
"""

import logging
import psycopg2

from nordb.nordic.station import Station
from nordb.core import usernameUtilities
from nordb.core.utils import addFloat2String 
from nordb.core.utils import addInteger2String
from nordb.core.utils import addString2String

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

def readStation(station_id):
    """
    Function for reading a station from database by id.

    :param int station_id: id of the station wanted
    :returns: Station object
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

    return Station(ans)

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
    conn = usernameUtilities.log2nordb() 
    cur = conn.cursor()

    cur.execute("SELECT id FROM station ORDER BY station_code;")

    ans = cur.fetchall()

    conn.close()
    
    station_ids = []

    if not ans:
        raise Exception
    for a in ans:
        station_ids.append(a[0])

    sql2station(station_ids, output_path)
