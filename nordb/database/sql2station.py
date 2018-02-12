"""
This module contains all functions for getting station information from the database and writing it into the database.

Functions and Classes
---------------------
"""

import logging
import psycopg2

from nordb.database import sql2sitechan
from nordb.nordic.station import Station
from nordb.core import usernameUtilities
from nordb.core.utils import addFloat2String 
from nordb.core.utils import addInteger2String
from nordb.core.utils import addString2String

SELECT_STATION =    (
                        "SELECT " 
                        "   station_code, on_date, off_date, latitude, " 
                        "   longitude, elevation, station_name, station_type, " 
                        "   reference_station, north_offset, east_offset, " 
                        "   load_date, network.network, network_id, station.id " 
                        "FROM " 
                        "   station, network " 
                        "WHERE " 
                        "   id = %s " 
                        "AND "
                        "   network.id = network_id"
                    )

ALL_STATIONS =      (
                        "SELECT " 
                        "   station_code, on_date, off_date, latitude, " 
                        "   longitude, elevation, station_name, station_type, " 
                        "   reference_station, north_offset, east_offset, " 
                        "   load_date, network.network, network_id, station.id " 
                        "FROM " 
                        "   station, network " 
                        "WHERE " 
                        "   network.id = network_id"
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

    stations = []
    for a in ans:
        stat = Station(a)
        sql2sitechan.sitechans2station(stat)

        stations.append(stat)

    conn.close()
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
    stat = Station(ans)
    
    sql2sitechan.sitechans2station(stat)

    return stat
