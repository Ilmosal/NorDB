"""
This module contains all functions for getting sitechan information form the database and writing the to a file.

Functions and Classes
---------------------
"""
import datetime

from nordb.database import sql2sensor
from nordb.nordic.sitechan import SiteChan
from nordb.core import usernameUtilities

SELECT_SITECHAN_OF_STATIONS =   (
                                    "SELECT "
                                    "   station.station_code, sitechan.channel_code, sitechan.on_date, sitechan.off_date, "
                                    "   sitechan.channel_type, sitechan.emplacement_depth,"
                                    "   sitechan.horizontal_angle, sitechan.vertical_angle,"
                                    "   sitechan.description, sitechan.load_date, "
                                    "   sitechan.id, station.id, sitechan.css_id "
                                    "FROM "
                                    "   sitechan, station "
                                    "WHERE "
                                    "   station.id IN %(station_ids)s "
                                    "AND "
                                    "   station.id = sitechan.station_id "
                                    "AND "
                                    "   ( "
                                    "       (sitechan.on_date <= %(station_date)s AND "
                                    "        sitechan.off_date >= %(station_date)s) "
                                    "   OR "
                                    "       (sitechan.on_date <=%(station_date)s AND "
                                    "        sitechan.off_date IS NULL) "
                                    "   ) "
                                )



SELECT_SITECHAN_OF_STATION =    (
                                    "SELECT "
                                    "   sitechan.id "
                                    "FROM "
                                    "   sitechan, station "
                                    "WHERE "
                                    "   station.id = %s "
                                    "AND "
                                    "   station.id = sitechan.station_id "
                                    "AND "
                                    "   ( "
                                    "       (sitechan.on_date <= %s AND "
                                    "        sitechan.off_date >= %s) "
                                    "   OR "
                                    "       (sitechan.on_date <=%s AND "
                                    "        sitechan.off_date IS NULL) "
                                    "   ) "
                                )

SELECT_SITECHAN =   (
                    "SELECT "
                    "   station.station_code, sitechan.channel_code, sitechan.on_date, sitechan.off_date, "
                    "   sitechan.channel_type, sitechan.emplacement_depth,"
                    "   sitechan.horizontal_angle, sitechan.vertical_angle,"
                    "   sitechan.description, sitechan.load_date, "
                    "   sitechan.id, station.id, sitechan.css_id "
                    "FROM "
                    "   sitechan, station "
                    "WHERE "
                    "   sitechan.id = %s "
                    "AND "
                    "   station.id = sitechan.station_id "
                    )

ALL_SITECHANS =     (
                    "SELECT"
                    "   station.station_code, sitechan.channel_code, sitechan.on_date, sitechan.off_date, "
                    "   sitechan.channel_type, sitechan.emplacement_depth,"
                    "   sitechan.horizontal_angle, sitechan.vertical_angle, "
                    "   sitechan.description, sitechan.load_date,"
                    "   sitechan.id, station.id, sitechan.css_id "
                    "FROM "
                    "   sitechan, station "
                    "WHERE "
                    "   station.id = sitechan.station_id "
                    )

def getAllSitechans(db_conn = None):
    """
    Function for reading all sitechans from database and returning them to user.

    :returns: Array of Sitechan objects
    """
    try:
        if db_conn is None:
            conn = usernameUtilities.log2nordb()
        else:
            conn = db_conn

        cur = conn.cursor()

        cur.execute(ALL_SITECHANS)
        ans = cur.fetchall()

        sitechans = []

        for a in ans:
            chan = SiteChan(a)
            sql2sensor.sensors2sitechan(chan, db_conn=conn)
            sitechans.append(chan)

        if db_conn is None:
            conn.close()

        return sitechans
    except Exception as e:
        print(e)
        conn.close()
        return None

def sitechans2stations(stations, station_date, db_conn = None):
    """
    Function for attaching all related sitechans to stations in the stations dict

    :param Dictionary stations: dictionary of stations where the key is the id of the station
    :param datetime station_date: date for getting the right sitechan files
    :param psycopg2.connection db_conn:
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()
    cur.execute(SELECT_SITECHAN_OF_STATIONS, {'station_ids':tuple(stations.keys()), 'station_date':station_date})

    ans = cur.fetchall()

    for a in ans:
        chan = SiteChan(a)
        stations[chan.station_id].sitechans.append(chan)

    if len(ans) != 0:
        sql2sensor.sensors2stations(stations, station_date, db_conn = conn)

    if db_conn is None:
        conn.close()

def sitechans2station(station, station_date, db_conn = None):
    """
    Function for attaching all related sitechans to station

    :param Station station: station to which the sitechans will be attached to
    :param datetime station_date: date for getting the right sitechan files
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    cur.execute(SELECT_SITECHAN_OF_STATION, (station.s_id, station_date,
                                             station_date, station_date))
    sitechan_ids = cur.fetchall()

    if sitechan_ids:
        for chan_id in sitechan_ids:
            station.sitechans.append(getSitechan(chan_id, station_date, db_conn=conn))

    if db_conn is None:
        conn.close()

def getSitechan(sitechan_id, station_date=datetime.datetime.now(), db_conn = None):
    """
    Function for reading a sitechan from database by id.

    :param int sitechan_id: id of the sitechan wanted
    :param datetime station_date: date for getting the right sitechan files
    :returns: Sitechan object
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    cur.execute(SELECT_SITECHAN, (sitechan_id,))
    ans = cur.fetchone()

    chan = SiteChan(ans)

    sql2sensor.sensors2sitechan(chan, station_date, db_conn=conn)

    if db_conn is None:
        conn.close()

    return chan
