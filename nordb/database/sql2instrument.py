"""
This module contains all operations for reading an :class:`.Instrument` object from the database and dumping it to a file or giving it to a user as a object.

Functions and Classes
---------------------
"""

import logging
import psycopg2

from nordb.database.sql2response import getResponseFromDB
from nordb.database.sql2response import responses2stations
from nordb.nordic.instrument import Instrument
from nordb.core import usernameUtilities
from nordb.core.utils import addFloat2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addString2String

SELECT_INSTRUMENTS =    (
                        "SELECT "
                        "   instrument_name, instrument_type, "
                        "   band, digital, samprate, ncalib, ncalper, dir, "
                        "   dfile, rsptype, instrument.lddate, instrument.id, "
                        "   instrument.css_id, response_id, "
                        "   station.id, sensor.id "
                        "FROM "
                        "   instrument, sensor, sitechan, station "
                        "WHERE "
                        "   sensor.id IN %(sensor_ids)s"
                        "AND "
                        "   sensor.instrument_id = instrument.id "
                        "AND "
                        "   sensor.sitechan_id = sitechan.id "
                        "AND "
                        "   station.id = sitechan.station_id "
                        )

def instruments2stations(stations, db_conn = None):
    """
    Function for fetching all instrument data related to stations into the station objects.

    :param Dict stations: dictionary of stations
    :param psycopg2.connection db_conn: connection object to the database
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    sensor_ids = []

    for stat in stations.values():
        for sitechan in stat.sitechans:
            for sensor in sitechan.sensors:
                sensor_ids.append(sensor.s_id)

    sensor_ids = tuple(sensor_ids)

    cur = conn.cursor()

    cur.execute(SELECT_INSTRUMENTS, {'sensor_ids':sensor_ids})

    ans = cur.fetchall()

    for a in ans:
        instrument = Instrument(a[:-2])
        for chan in stations[a[-2]].sitechans:
            for sen in chan.sensors:
                if sen.s_id == a[-1]:
                    sen.instruments.append(instrument)

    responses2stations(stations, db_conn=conn)

    if db_conn is None:
        conn.close()

