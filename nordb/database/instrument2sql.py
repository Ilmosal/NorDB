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
                        "INSERT INTO instrument " 
                            "(  css_id, instrument_name, instrument_type, " 
                            "   band, digital, samprate, ncalib, " 
                            "   ncalper, dir, dfile, rsptype, " 
                            "   lddate) " 
                        "VALUES " 
                            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " 
                    )

def insertInstrument2Database(instrument):
    """ 
    Function for inserting the instrument array to the database

    :param Instrument instrument: instrument that will be inserted to the database
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    try:
        cur.execute(INSTRUMENT_INSERT, instrument.getAsList())
    except Exception as e:
        conn.close()
        raise e
    conn.commit()
    conn.close()

