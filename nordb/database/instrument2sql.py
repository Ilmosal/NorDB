"""
This module contains all functions and classes for reading a instrument file in `CSS3.0 format`_ and pushing it into the database

.. _CSS3.0 format: ftp://ftp.pmel.noaa.gov/newport/lau/tphase/data/css_wfdisc.pdf

Functions and Classes
---------------------
"""
import unidecode

from nordb.nordic.instrument import Instrument
from nordb.core import usernameUtilities
from nordb.core.utils import stringToDate

INSTRUMENT_INSERT = (   
                        "INSERT INTO instrument " +
                            "(  instrument_name, instrument_type, " +
                            "   band, digital, samprate, ncalib, " +
                            "   ncalper, dir, dfile, rsptype, " +
                            "   lddate) " +
                        "VALUES " +
                            "(  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " +
                        "RETURNING " +
                            "id"
                    )

def insertInstrument2Database(instrument):
    """ 
    Function for inserting the instrument array to the database

    :param Instrument instrument: instrument that will be inserted to the database
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(INSTRUMENT_INSERT, instrument.getAsList())

    db_id = cur.fetchone()[0]

    cur.execute("INSERT INTO instrument_css_link (css_id, instrument_id) VALUES (%s, %s)", (instrument.css_id, db_id))

    conn.commit()
    conn.close()

def readInstrumentStringToInstrument(ins_line):
    """
    Function for reading instrument info to a Instrument object 

    :param str ins_line: css intrument line
    :returns: Instrument object
    """
    instrument = [None]*13

    instrument[Instrument.INSTRUMENT_NAME]  = unidecode.unidecode(ins_line[8:58].strip())
    instrument[Instrument.INSTRUMENT_TYPE]  = unidecode.unidecode(ins_line[60:67].strip())
    instrument[Instrument.BAND]             = unidecode.unidecode(ins_line[67].strip())
    instrument[Instrument.DIGITAL]          = unidecode.unidecode(ins_line[69].strip())
    instrument[Instrument.SAMPRATE]         = unidecode.unidecode(ins_line[70:82].strip())
    instrument[Instrument.NCALIB]           = unidecode.unidecode(ins_line[82:100].strip())
    instrument[Instrument.NCALPER]          = unidecode.unidecode(ins_line[101:116].strip())
    instrument[Instrument.RESP_DIR]         = unidecode.unidecode(ins_line[117:182].strip())
    instrument[Instrument.DFILE]            = unidecode.unidecode(ins_line[182:215].strip())
    instrument[Instrument.RSPTYPE]          = unidecode.unidecode(ins_line[215:228].strip())
    instrument[Instrument.LDDATE]           = unidecode.unidecode(stringToDate(ins_line[228:].strip()))
    instrument[Instrument.I_ID]             = -1
    instrument[Instrument.CSS_ID]           = unidecode.unidecode(ins_line[:8].strip())

    return Instrument(instrument)

def readInstruments(f_instruments):
    """
    Function for reading instrument in css format and inserting them to the database

    :param file f_instruments: the file that will be read into the database
    """
    instruments = []

    for line in f_instruments:
        instruments.append(readInstrumentStringToInstrument(line))
   
    for ins in instruments:
        insertInstrument2Database(ins)

