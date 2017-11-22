import logging
import psycopg2

from nordb.database.station2sql import Instrument
from nordb.core import usernameUtilities
from nordb.database.sql2nordic import add_float_to_string, add_integer_to_string, add_string_to_string

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

    Args:
        instrument (list()): instrument array described by Instrument object

    Returns:
        The instrument string in a css format
    """
    instrumentString = ""
    
    instrumentString += add_integer_to_string(instrument[Instrument.CSS_ID], 8, '>')
    
    instrumentString += " "

    instrumentString += add_string_to_string(instrument[Instrument.INSTRUMENT_NAME], 50, '<')

    instrumentString += " "
    
    instrumentString += add_string_to_string(instrument[Instrument.INSTRUMENT_TYPE], 6, '<')

    instrumentString += " "

    instrumentString += add_string_to_string(instrument[Instrument.BAND], 2, '<')
    instrumentString += add_string_to_string(instrument[Instrument.DIGITAL], 2, '<')
    instrumentString += add_float_to_string (instrument[Instrument.SAMPRATE], 11, 7, '>')

    instrumentString += "    "
    
    instrumentString += add_float_to_string (instrument[Instrument.NCALIB], 13, 6, '>')
    
    instrumentString += "    "
    
    instrumentString += add_float_to_string(instrument[Instrument.NCALPER], 13, 6, '>')

    instrumentString += " "

    instrumentString += add_string_to_string(instrument[Instrument.DIR], 64, '<')
        
    instrumentString += " "
    
    instrumentString += add_string_to_string(instrument[Instrument.DFILE], 32, '<')

    instrumentString += add_string_to_string(instrument[Instrument.RSPTYPE], 6, '<')

    instrumentString += add_string_to_string(instrument[Instrument.LDDATE].strftime("%Y-%b-%d"), 10, '<')

    return instrumentString

def readInstrument(instrument_id):
    """
    Function for reading a instrument from database by id

    Args:
        instrument_id(int): id of the instrument wanted

    Returns:
        instrument(list): instrument list
    """
    try:
        conn = psycopg2.connect("dbname = nordb user = {0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return

    cur = conn.cursor()

    cur.execute(SELECT_INSTRUMENT, (instrument_id, ))
    ans = cur.fetchone()

    conn.close()

    return ans

def sql2Instrument(instrument_ids, output_path):
    """
    Function for reading instruments from the database and dumping them to a instruments.instrument file

    Args:
        instrument_ids (ins[]): Array of integers
        output_path (str): path to the output file
    """
    username = usernameUtilities.readUsername()

    instruments = []

    for instrument_id in instrument_ids:
        instruments.append(readInstrument(instrument_id))

    f = open(output_path, "w")

    for instrument in instruments:
        f.write(createInstrumentString(instrument) + "\n")

def writeAllInstruments(output_path):
    """
    Function for writing all instruments to a instrument file

    Args:
        output_path(str): path to output_file
    """
    username = usernameUtilities.readUsername()

    try:
        conn = psycopg2.connect("dbname = nordb user = {0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return

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
