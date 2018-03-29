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

SELECT_STATION_ID = (
                        "SELECT " 
                        "   station_code, on_date, off_date, latitude, " 
                        "   longitude, elevation, station_name, station_type, " 
                        "   reference_station, north_offset, east_offset, " 
                        "   load_date, network.network, network_id, station.id " 
                        "FROM " 
                        "   station, network " 
                        "WHERE " 
                        "   station.id = %s " 
                        "AND "
                        "   network.id = network_id"
                    )

SELECT_STATION_CODE =   (
                        "SELECT " 
                        "   station_code, on_date, off_date, latitude, " 
                        "   longitude, elevation, station_name, station_type, " 
                        "   reference_station, north_offset, east_offset, " 
                        "   load_date, network.network, network_id, station.id " 
                        "FROM " 
                        "   station, network " 
                        "WHERE " 
                        "   station.station_code = %s " 
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

def getAllStations():
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

def getStation(station_id):
    """
    Function for reading a station from database by id or code

    :param int,str station_id: id of the station wanted or the station code of the station
    :returns: Station object
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    if isinstance(station_id, int):
        cur.execute(SELECT_STATION_ID, (station_id,))
    elif isinstance(station_id, str):
        cur.execute(SELECT_STATION_CODE, (station_id,))

    ans = cur.fetchone()
    conn.close()

    if ans is None:
        return None

    stat = Station(ans)
    
    sql2sitechan.sitechans2station(stat)

    return stat
