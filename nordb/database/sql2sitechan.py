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
def getFreeCSSSitechanID():
    pass

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

    sitechans = []

    for a in ans:
        chan = SiteChan(a)
        sitechans.append(chan)
        stations[chan.station_id].sitechans.append(chan)

    if len(ans) != 0:
        sql2sensor.sensors2sitechans(sitechans, station_date, db_conn = conn)

    if db_conn is None:
        conn.close()
