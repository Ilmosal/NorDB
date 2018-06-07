"""
This module contains all functions and classes for reading a sitechan file in `CSS3.0 format`_ and pushing it into the database

.. _CSS3.0 format: ftp://ftp.pmel.noaa.gov/newport/lau/tphase/data/css_wfdisc.pdf

Functions and Classes
---------------------
"""
import unidecode

from nordb.nordic.sitechan import SiteChan
from nordb.core import usernameUtilities
from nordb.core.utils import stringToDate

CHANNEL_INSERT = (  "INSERT INTO sitechan" +
                        "(      station_id, css_id, channel_code, on_date, off_date, " +
                        "       channel_type, emplacement_depth, " +
                        "       horizontal_angle, vertical_angle," +
                        "       description, load_date)" + 
                    "VALUES " +
                        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "  +
                    "RETURNING " +
                    "   id" )

def insertSiteChan2Database(channel):
    """
    Function for inserting the sitechan array to the database.

    :param SiteChan channel: sitechan that will be inserted to the database
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM station WHERE STATION_CODE = %s", (channel.station_code,))
        ans = cur.fetchone()

        if ans is None:
            raise Exception("No station for channel!")

        channel.station_id = ans[0]

        cur.execute(CHANNEL_INSERT, channel.getAsList())
    except Exception as e:
        conn.close()
        raise e
    conn.commit()
    conn.close()

