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

