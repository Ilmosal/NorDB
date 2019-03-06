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
                        "   lddate, response_id) "
                    "VALUES "
                        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                    )

FIND_RESPONSE =     (
                    "SELECT "
                    "   response.id "
                    "FROM "
                    "   response "
                    "WHERE "
                    "   response.file_name = %s "
                    )

def getResponseId(response_file_name):
    """
    Function for finding the correct response for the instrument

    :param String response_file_name: filename of the response
    :returns: id of the response in the database
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    response_id = -1
    try:
        cur.execute(FIND_RESPONSE, (response_file_name,))
        response_id = cur.fetchone()[0]
    except Exception as e:
        conn.close()
        raise e
    return response_id

def insertInstrument2Database(instrument):
    """
    Function for inserting the instrument array to the database

    :param Instrument instrument: instrument that will be inserted to the database
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    if instrument.css_id == -1:
        cur.execute("SELECT MAX(css_id) FROM instrument")
        ans = cur.fetchone()
        if ans[0] is None:
            instrument.css_id = 1
        else:
            instrument.css_id = ans[0] + 1
    try:
        instrument.response_id = getResponseId(instrument.dfile)
        cur.execute(INSTRUMENT_INSERT, instrument.getAsList())
    except Exception as e:
        conn.close()
        raise e

    conn.commit()
    conn.close()

