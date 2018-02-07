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
                            "load_date, network_id, id " +
                        "FROM " +
                            "station " +
                        "WHERE " +
                            "id = %s" 
                    )

ALL_STATIONS =      (
                        "SELECT " +
                            "station_code, on_date, off_date, latitude, " +
                            "longitude, elevation, station_name, station_type, " +
                            "reference_station, north_offset, east_offset, " +
                            "load_date, network_id, id " +
                        "FROM " +
                            "station " 
                    )

def readAllStations():
    """
    Function for reading all stations from database.

    :returns: Array of Station objects
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(ALL_STATIONS)

    ans = cur.fetchall()
    conn.close()

    stations = []
    for a in ans:
        stations.append(Station(a))

    return stations

def readStation(station_id):
    """
    Function for reading a station from database by id.

    :param int station_id: id of the station wanted
    :returns: Station object
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(SELECT_STATION, (station_id,))

    ans = cur.fetchone()

    conn.close()

    return Station(ans)
