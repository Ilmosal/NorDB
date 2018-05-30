"""
This module contains all operations for reading an :class:`.Instrument` object from the database and dumping it to a file or giving it to a user as a object.

Functions and Classes
---------------------
"""

import logging
import psycopg2

from nordb.nordic.instrument import Instrument
from nordb.core import usernameUtilities
from nordb.core.utils import addFloat2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addString2String

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

def getAllInstruments():
    """
    Function for reading all insturments from the database and returning them to user.

    :return: Array of :class:`.Instrument` objects
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    try:
        cur.execute(ALL_INSTRUMENTS)
        ans = cur.fetchall()
    except Exception as e:
        conn.close()
        raise e
    conn.close()

    instruments = []

    for a in ans:
        instruments.append(Instrument(a))

    return instruments

def instruments2sensor(sensor):
    """
    Function for attaching all related instruments to Sensor object.

    :param Sensor sensor: sensor to which its intruments will be attached to
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    try:    
        cur.execute(SELECT_INSTRUMENTS_TO_SENSOR, (sensor.s_id,))
        instrument_ids = cur.fetchall()
    except Exception as e:
        conn.close()
        raise e
    conn.close()

    if instrument_ids:
        for instrument_id in instrument_ids:
            sensor.instruments.append(getInstrument(instrument_id))

def getInstrument(instrument_id):
    """
    Function for reading a instrument from database by id

    :param int instrument_id: id of the instrument wanted
    :return: :class:`.Instrument` object
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(SELECT_INSTRUMENT, (instrument_id, ))
    ans = cur.fetchone()

    conn.close()

    return Instrument(ans)

