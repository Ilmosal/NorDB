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

SELECT_INSTRUMENT = (
                        "SELECT "
                        "   instrument_name, instrument_type, "
                        "   band, digital, samprate, ncalib, ncalper, dir, "
                        "   dfile, rsptype, lddate, id, css_id, response_id "
                        "FROM "
                        "   instrument "
                        "WHERE "
                        "   instrument.id = %s")

ALL_INSTRUMENTS =   (
                        "SELECT "
                        "   instrument_name, instrument_type, "
                        "   band, digital, samprate, ncalib, ncalper, dir, "
                        "   dfile, rsptype, lddate, id, css_id, response_id "
                        "FROM "
                        "   instrument "
                    )


SELECT_INSTRUMENTS_TO_SENSOR =  (
                                "SELECT "
                                "   instrument.id "
                                "FROM "
                                "   instrument, sensor "
                                "WHERE "
                                "   sensor.id = %s "
                                "AND "
                                "   instrument.id = sensor.instrument_id "
                                )

def getAllInstruments(db_conn = None):
    """
    Function for reading all insturments from the database and returning them to user.

    :return: Array of :class:`.Instrument` objects
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    cur.execute(ALL_INSTRUMENTS)
    ans = cur.fetchall()

    instruments = []

    for a in ans:
        instrument = Instrument(a)
        instrument.response = getResponseFromDB(instrument.response_id, db_conn=conn)
        instruments.append(instrument)

    if db_conn is None:
        conn.close()

    return instruments

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

def instruments2sensor(sensor, db_conn = None):
    """
    Function for attaching all related instruments to Sensor object.

    :param Sensor sensor: sensor to which its intruments will be attached to
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    cur.execute(SELECT_INSTRUMENTS_TO_SENSOR, (sensor.s_id,))
    instrument_ids = cur.fetchall()

    if instrument_ids:
        for instrument_id in instrument_ids:
            sensor.instruments.append(getInstrument(instrument_id, db_conn=conn))

    if db_conn is None:
        conn.close()

def getInstrument(instrument_id, db_conn = None):
    """
    Function for reading a instrument from database by id

    :param int instrument_id: id of the instrument wanted
    :return: :class:`.Instrument` object
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    cur.execute(SELECT_INSTRUMENT, (instrument_id, ))
    ans = cur.fetchone()

    instrument = Instrument(ans)
    instrument.response = getResponseFromDB(instrument.response_id, db_conn=conn)

    if db_conn is None:
        conn.close()

    return instrument
