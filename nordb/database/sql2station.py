"""
This module contains all functions for getting station information from the database and writing it into the database.

Functions and Classes
---------------------
"""

import datetime
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
                        "   ( "
                        "       (on_date <= %s AND off_date >= %s) "
                        "   OR "
                        "       (on_date <=%s AND off_date IS NULL) "
                        "   ) "
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

def getAllStations(db_conn = None):
    """
    Function for reading all stations from database.

    :param psycopg2.connection db_conn: Connection to the database
    :returns: Array of Station objects
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    cur.execute(ALL_STATIONS)

    ans = cur.fetchall()

    stations = []
    for a in ans:
        stat = Station(a)
        sql2sitechan.sitechans2station(stat, datetime.datetime.now(), conn)

        stations.append(stat)

    if db_conn is None:
        conn.close()

    return stations

def getStation(station_id, station_date = datetime.datetime.now(), db_conn = None):
    """
    Function for reading a station from database by id or code and datetime.

    :param int,str station_id: id of the station wanted or the station code of the station
    :param psycopg2.connection db_conn: Connection to the database
    :param datetime station_date: date for which the station info will be taken
    :returns: Station object
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    if isinstance(station_id, int):
        cur.execute(SELECT_STATION_ID, (station_id,))
    elif isinstance(station_id, str):
        cur.execute(SELECT_STATION_CODE, (station_id, station_date,
                                          station_date, station_date))

        ans = cur.fetchone()

    if ans is None:
        return None

    stat = Station(ans)

    sql2sitechan.sitechans2station(stat, station_date, conn)

    if db_conn is None:
        conn.close()

    return stat

