"""
This module contains all operations for reading an :class:`.Instrument` object from the database and dumping it to a file or giving it to a user as a object.

Functions and Classes
---------------------
"""

import logging
import psycopg2

from nordb.database.station2sql import Instrument
from nordb.core import usernameUtilities
from nordb.core.utils import addFloat2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addString2String

username = ""

SELECT_INSTRUMENT = (   "SELECT " +
                            "instrument_name, instrument_type, " +
                            "band, digital, samprate, ncalib, ncalper, dir, " +
                            "dfile, rsptype, lddate, id, css_id " +
                        "FROM " +
                            "instrument, instrument_css_link " +
                        "WHERE " +
                            "instrument.id = instrument_id " +
                        "AND " +
                            "instrument.id = %s")

def createInstrumentString(instrument):
    """
    Function for creating a css instrument string from a instrument object.

    :param list instrument: instrument array described by Instrument object
    :return: The instrument string in a css format
    """
    instrumentString = ""
    
    instrumentString += addInteger2String(instrument[Instrument.CSS_ID], 8, '>')
    
    instrumentString += " "

    instrumentString += addString2String(instrument[Instrument.INSTRUMENT_NAME], 50, '<')

    instrumentString += " "
    
    instrumentString += addString2String(instrument[Instrument.INSTRUMENT_TYPE], 6, '<')

    instrumentString += " "

    instrumentString += addString2String(instrument[Instrument.BAND], 2, '<')
    instrumentString += addString2String(instrument[Instrument.DIGITAL], 2, '<')
    instrumentString += addFloat2String (instrument[Instrument.SAMPRATE], 11, 7, '>')

    instrumentString += "    "
    
    instrumentString += addFloat2String (instrument[Instrument.NCALIB], 13, 6, '>')
    
    instrumentString += "    "
    
    instrumentString += addFloat2String(instrument[Instrument.NCALPER], 13, 6, '>')

    instrumentString += " "

    instrumentString += addString2String(instrument[Instrument.DIR], 64, '<')
        
    instrumentString += " "
    
    instrumentString += addString2String(instrument[Instrument.DFILE], 32, '<')

    instrumentString += addString2String(instrument[Instrument.RSPTYPE], 6, '<')

    instrumentString += addString2String(instrument[Instrument.LDDATE].strftime("%Y-%b-%d"), 10, '<')

    return instrumentString

def readInstrument(instrument_id):
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

    return ans

def sql2Instrument(instrument_ids, output_path):
    """
    Function for reading instruments from the database and dumping them to a instruments.instrument file

    :param array instrument_ids: Array of instrument ids you want to get from the database
    :param str output_path: path to the output file
    """
    instruments = []

    for instrument_id in instrument_ids:
        instruments.append(readInstrument(instrument_id))

    f = open(output_path, "w")

    for instrument in instruments:
        f.write(createInstrumentString(instrument) + "\n")

def writeAllInstruments(output_path):
    """
    Function for writing all instruments to a instrument file

    :param str output_path: path to output_file
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT id FROM instrument;")
    ans = cur.fetchall()

    conn.close()

    instrument_ids = []

    if not ans:
        print("No stations in the database")
        return

    for a in ans:
        instrument_ids.append(a[0])

    sql2Instrument(instrument_ids, output_path)
