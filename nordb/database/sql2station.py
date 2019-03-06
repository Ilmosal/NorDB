"""
This module contains all functions for getting station information from the database and writing it into the database.

Functions and Classes
---------------------
"""

import datetime
import psycopg2
import numpy

from nordb.database import sql2sitechan
from nordb.nordic.station import Station
from nordb.core import usernameUtilities
from nordb.core.utils import addFloat2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addString2String

SELECT_ALL_CLOSED_STATIONS = (
                            "SELECT "
                            "   station_code, on_date, off_date, latitude, "
                            "   longitude, elevation, station_name, station_type, "
                            "   reference_station, north_offset, east_offset, "
                            "   load_date, network.network, network_id, station.id "
                            "FROM "
                            "   station, network "
                            "WHERE "
                            "   off_date IS NOT NULL"
                            "AND "
                            "   station.network_id = network.id "
                            )

SELECT_ALL_STATIONS =   (
                        "SELECT "
                        "   station_code, on_date, off_date, latitude, "
                        "   longitude, elevation, station_name, station_type, "
                        "   reference_station, north_offset, east_offset, "
                        "   load_date, network.network, network_id, station.id "
                        "FROM "
                        "   station, network "
                        "WHERE "
                        "   station.network_id = network.id "
                        )

SELECT_STATIONS_NEAR_POINT =    (
                                "SELECT "
                                "   id "
                                "FROM "
                                "   station "
                                "WHERE "
                                "   ABS(latitude - %(p_lat)s) <= %(lat_diff)s "
                                "AND "
                                "   ABS(longitude - %(p_lon)s) <= %(lon_diff)s "
                                "AND "
                                "   ( "
                                "       (on_date <= %(station_date)s AND off_date >= %(station_date)s) "
                                "   OR "
                                "       (on_date <= %(station_date)s AND off_date IS NULL) "
                                "   ) "
                                )

SELECT_STATIONS_ID =   (
                        "SELECT "
                        "   station_code, on_date, off_date, latitude, "
                        "   longitude, elevation, station_name, station_type, "
                        "   reference_station, north_offset, east_offset, "
                        "   load_date, network.network, network_id, station.id "
                        "FROM "
                        "   station, network "
                        "WHERE "
                        "   station.id in %(station_ids)s "
                        "AND "
                        "   ( "
                        "       (on_date <= %(station_date)s AND off_date >= %(station_date)s) "
                        "   OR "
                        "       (on_date <=%(station_date)s AND off_date IS NULL) "
                        "   ) "
                        "AND "
                        "   network_id = network.id "
                    )

SELECT_STATIONS_CODE =  (
                        "SELECT "
                        "   station_code, on_date, off_date, latitude, "
                        "   longitude, elevation, station_name, station_type, "
                        "   reference_station, north_offset, east_offset, "
                        "   load_date, network.network, network_id, station.id "
                        "FROM "
                        "   station, network "
                        "WHERE "
                        "   station_code in %(station_codes)s "
                        "AND "
                        "   ( "
                        "       (on_date <= %(station_date)s AND off_date >= %(station_date)s) "
                        "   OR "
                        "       (on_date <=%(station_date)s AND off_date IS NULL) "
                        "   ) "
                        "AND "
                        "   network_id = network.id "
                        )

ALL_STATION_CODES = (
                    "SELECT "
                    "   station_code "
                    "FROM "
                    "   station "
                    "ORDER BY "
                    "   station_code"
                    )

SELECT_ALL_STATION_IDS =    (
                            "SELECT "
                            "   station.id "
                            "FROM "
                            "   station "
                            "WHERE "
                            "   ( "
                            "       (on_date <= %(station_date)s AND off_date >= %(station_date)s) "
                            "   OR "
                            "       (on_date <=%(station_date)s AND off_date IS NULL) "
                            "   ) "
                            )

def getAllClosedStations(db_conn = None):
    """
    Function for getting all closed stations from the database
    :param psycopg2.connection db_conn: Connection object to the database
    :returns: Array of Station objects
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    cur.execute(SELECT_ALL_CLOSED_STATIONS)
    ans = cur.fetchall()

    stations = {}
    for a in ans:
        stations[a[-1]] = Station(a)

    if len(stations.keys()) != 0:
        sql2sitechan.allSitechans2Stations(stations, db_conn=conn)

    conn.close()

    return list(stations.values())

def getStationCodes(db_conn = None):
    """
    Function for reading all station_codes from the database.

    :param psycopg2.connection db_conn: Connection object to the database
    :returns: Array of strings
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    cur.execute(ALL_STATION_CODES)

    ans = cur.fetchall()

    stations = [stat[0] for stat in ans]

    return stations

def getAllStations(station_date = None, db_conn = None):
    """
    Function for reading all stations from database. If None is passed as station_date, the function will fetch all station information in the database which will include all closed stations and sitechans.

    :param psycopg2.connection db_conn: Connection to the database
    :param datetime station_date: date for which the station info will be taken
    :returns: Array of Station objects
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    if station_date is None:
        cur.execute(SELECT_ALL_STATIONS)
        ans = cur.fetchall()

        stations = {}
        for a in ans:
            stations[a[-1]] = Station(a)

        if len(stations.keys()) != 0:
            sql2sitechan.allSitechans2Stations(stations, db_conn=conn)

        if db_conn is None:
            conn.close()

        return list(stations.values())
    else:
        cur.execute(SELECT_ALL_STATION_IDS, {'station_date': station_date })

        ans = cur.fetchall()
        station_ids = []
        for a in ans:
            station_ids.append(a[0])

        stations = getStations(station_ids, station_date, db_conn=conn)

    if db_conn is None:
        conn.close()

    return stations

def getStations(station_ids, station_date = datetime.datetime.now(), db_conn = None):
    """
    Function that returns all stations with id in station_ids to the user.

    :param Array station_ids: array of ids to be fetched
    :param datetime station_date: date for which the station info will be taken
    :param psycopg2.connection db_conn: Existing connection to the database. Defaults to None
    """
    if len(station_ids) == 0:
        return []

    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    if isinstance(station_ids, type([])):
        station_ids = tuple(station_ids)

    if isinstance(station_ids[0], str):
        cur.execute(SELECT_STATIONS_CODE, { 'station_codes':station_ids,
                                            'station_date':station_date})
    else:
        cur.execute(SELECT_STATIONS_ID, {'station_ids':station_ids,
                                         'station_date':station_date})

    ans = cur.fetchall()

    if ans is None:
        if db_conn is None:
            conn.close()
        return

    stations = {}
    for a in ans:
        stations[a[-1]] = Station(a)

    if len(stations.keys()) != 0:
        sql2sitechan.sitechans2stations(stations, station_date, db_conn=conn)

    if db_conn is None:
        conn.close()

    return list(stations.values())

def getStation(station_id, station_date = datetime.datetime.now(), db_conn = None):
    """
    Function for reading a station from database by id or code and datetime.

    :param int,str station_id: id of the station wanted or the station code of the station
    :param psycopg2.connection db_conn: Existing connection to the database. Defaults to None
    :param datetime station_date: date for which the station info will be taken
    :returns: Station object
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    temp = getStations([station_id], station_date, db_conn=conn)

    if len(temp) == 0:
        stat = None
    else:
        stat = temp[0]

    if db_conn is None:
        conn.close()

    return stat

def getStationsNearPoint(latitude, longitude, radius = 10.0, station_date = datetime.datetime.now(), db_conn = None):
    """
    Function for getting all stations that are less than radius away from point (latitude, longitude) radius is in kilometers.

    :param float latitude: latitude of the point
    :param float lognitude: longitude of the point
    :param float radius: maximum radius allowed by the program in kilometers. Defaults to 10.0 km
    :param datetime station_date: date for the station fetching. Defaults to this date
    :param psycopg2.connection db_conn: Existing connection to the database. Defaults to None
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    lat_diff = radius*(1/110.574)
    lon_diff = radius*(1/(111.320*numpy.cos(numpy.radians(latitude))))
    cur.execute(SELECT_STATIONS_NEAR_POINT, {'p_lat':latitude,
                                             'lat_diff':lat_diff,
                                             'p_lon':longitude,
                                             'lon_diff':lon_diff,
                                             'station_date':station_date})

    ans = cur.fetchall()
    stations = []

    if ans is None:
        return None

    station_ids = []
    for a in ans:
        station_ids.append(a[0])

    stations = getStations(station_ids, station_date, db_conn=conn)

    if db_conn is None:
        conn.close()

    return stations
