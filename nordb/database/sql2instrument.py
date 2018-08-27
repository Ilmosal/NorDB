"""
This module contains all operations for reading an :class:`.Instrument` object from the database and dumping it to a file or giving it to a user as a object.

Functions and Classes
---------------------
"""

import logging
import psycopg2

from nordb.database.sql2response import getResponseFromDB
from nordb.database.sql2response import responses2instruments
from nordb.nordic.instrument import Instrument
from nordb.core import usernameUtilities
from nordb.core.utils import addFloat2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addString2String

SELECT_INSTRUMENT =     (
                        "SELECT "
                        "   instrument_name, instrument_type, "
                        "   band, digital, samprate, ncalib, ncalper, dir, "
                        "   dfile, rsptype, instrument.lddate, instrument.id, "
                        "   instrument.css_id, response_id, "
                        "FROM "
                        "   instrument "
                        "WHERE "
                        "   instrument.id = %(instrument_id)s"
                        )

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

def getInstrument(instrument_id, db_conn = None):
    """
    Function for fetching an instrument from the database and returning it to the user.

    :param int instrument_id: id of the instrumnent wanted
    :param psycopg2.connection db_conn: connection object to the database
    :returns: Instrument object
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    cur.execute(SELECT_INSTRUMENT, {'instrument_id':instrument_id})

    ans = cur.fetchone()

    instrument = Instrument(ans)

    responses2instruments([instrument], db_conn=conn)

    if conn is None:
        conn.close()

    return instrument

def instruments2sensors(sensors, db_conn = None):
    """
    Function for fetching all instrument data related to sensors to a list of sensor objects.

    :param list sensor: list of sensors
    :param psycopg2.connection db_conn: connection object to the database
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    sensor_ids = []

    for sensor in sensors:
        sensor_ids.append(sensor.s_id)

    sensor_ids = tuple(sensor_ids)

    cur = conn.cursor()

    cur.execute(SELECT_INSTRUMENTS, {'sensor_ids':sensor_ids})

    ans = cur.fetchall()

    instruments = []

    for a in ans:
        instrument = Instrument(a[:-2])
        instruments.append(instrument)
        for sen in sensors:
            if sen.s_id == a[-1]:
                sen.instruments.append(instrument)

    responses2instruments(instruments, db_conn=conn)

    if db_conn is None:
        conn.close()

