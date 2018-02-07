"""
This module contains all functions for getting sitechan information form the database and writing the to a file.

Functions and Classes
---------------------
"""

import logging
import psycopg2

from nordb.nordic.sitechan import SiteChan
from nordb.core import usernameUtilities
from nordb.core.utils import addFloat2String 
from nordb.core.utils import addInteger2String
from nordb.core.utils import addString2String

SELECT_SITECHAN =  ("SELECT"                                                            +
                    "   station.station_code, sitechan.channel_code, sitechan.on_date, sitechan.off_date, "    +
                    "   sitechan.channel_type, sitechan.emplacement_depth,"             +
                    "   sitechan.horizontal_angle, sitechan.vertical_angle,"            +
                    "   sitechan.description, sitechan.load_date, sitechan_css_link.css_id, " +
                    "   station.id, sitechan.id "                                      +
                    "FROM "                                                             +
                    "   sitechan, station, sitechan_css_link "                          +
                    "WHERE "                                                            +
                    "   sitechan.id = %s "                                              +
                    "AND "                                                              +
                    "   station.id = sitechan.station_id "                              +
                    "AND "                                                              +
                    "   sitechan_css_link.sitechan_id = sitechan.id")

ALL_SITECHANS =    ("SELECT"                                                            +
                    "   station.station_code, sitechan.channel_code, sitechan.on_date, sitechan.off_date, "    +
                    "   sitechan.channel_type, sitechan.emplacement_depth,"             +
                    "   sitechan.horizontal_angle, sitechan.vertical_angle,"            +
                    "   sitechan.description, sitechan.load_date, sitechan_css_link.css_id, " +
                    "   station.id, sitechan.id "                                       +
                    "FROM "                                                             +
                    "   sitechan, station, sitechan_css_link "                          +
                    "WHERE "                                                            +
                    "   station.id = sitechan.station_id "                              +
                    "AND "                                                              +
                    "   sitechan_css_link.sitechan_id = sitechan.id")

def readAllSitechans():
    """
    Function for reading all sitehchans from database and returning them to user.

    :returns: Array of Sitechan objects
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(ALL_SITECHANS)
    ans = cur.fetchall()
    conn.close()

    sitechans = []

    for a in ans:
        sitechans.append(SiteChan(a))

    return sitechans

def readSitechan(sitechan_id):
    """
    Method for reading a sitechan from database by id.
    
    :param int sitechan_id: id of the sitechan wanted
    :returns: Sitechan object
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(SELECT_SITECHAN, (sitechan_id,))
    ans = cur.fetchone()

    conn.close()

    return SiteChan(ans)
