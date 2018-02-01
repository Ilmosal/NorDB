"""
This module contains all functions and classes for reading a sitechan file in `CSS3.0 format`_ and pushing them into the database

.. _CSS3.0 format: ftp://ftp.pmel.noaa.gov/newport/lau/tphase/data/css_wfdisc.pdf

Functions and Classes
---------------------
"""
import unidecode

from nordb.nordic.sitechan import SiteChan
from nordb.core import usernameUtilities
from nordb.core.utils import stringToDate

CHANNEL_INSERT = (  "INSERT INTO sitechan" +
                        "(      station_id, channel_code, on_date, off_date, " +
                        "       channel_type, emplacement_depth, " +
                        "       horizontal_angle, vertical_angle," +
                        "       description, load_date)" + 
                    "VALUES " +
                        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "  +
                    "RETURNING " +
                    "   id" )

def readSiteChanStringToSiteChan(chan_line):
    """
    Function for reading channel info to string array from css sitechan string

    :param str chan_line: css sitechan string
    :return: sitechan string array and station_code
    """
    channel = [None]*13

    channel[SiteChan.STATION_CODE]      = unidecode.unidecode(chan_line[:7].strip())
    channel[SiteChan.CHANNEL_CODE]      = unidecode.unidecode(chan_line[7:17].strip())
    channel[SiteChan.ON_DATE]           = unidecode.unidecode(stringToDate(chan_line[17:24].strip()))
    channel[SiteChan.OFF_DATE]          = unidecode.unidecode(stringToDate(chan_line[35:42].strip()))
    channel[SiteChan.CHANNEL_TYPE]      = unidecode.unidecode(chan_line[43:48].strip())
    channel[SiteChan.EMPLACEMENT_DEPTH] = unidecode.unidecode(chan_line[49:57].strip())
    channel[SiteChan.HORIZONTAL_ANGLE]  = unidecode.unidecode(chan_line[57:64].strip())
    channel[SiteChan.VERTICAL_ANGLE]    = unidecode.unidecode(chan_line[64:71].strip())
    channel[SiteChan.DESCRIPTION]       = unidecode.unidecode(chan_line[72:122].strip())
    channel[SiteChan.LOAD_DATE]         = unidecode.unidecode(stringToDate(chan_line[123:].strip()))
    channel[SiteChan.S_ID]              = -1
    channel[SiteChan.STATION_ID]        = -1
    channel[SiteChan.CSS_ID]            = unidecode.unidecode(chan_line[25:33].strip())

    return SiteChan(channel)

def insertSiteChan2Database(channel):
    """ 
    Function for inserting the sitechan array to the database.
        
    :param SiteChan channel: sitechan that will be inserted to the database
    :return: true or false depending on if the operation was succesful
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT id FROM station WHERE STATION_CODE = %s", (channel.station_code,))
    ans = cur.fetchone()

    if ans is None:
        raise Exception("No station for channel!")
    
    channel.station_id = ans[0]

    cur.execute(CHANNEL_INSERT, channel.getAsList())
 
    db_id = cur.fetchone()[0]

    cur.execute("INSERT INTO sitechan_css_link (css_id, sitechan_id) VALUES (%s, %s)", (channel.css_id, db_id))

    conn.commit()
    conn.close()

    return True

def readChannels(f_channels):
    """ 
    Function for reading sitechan in css format and inserting them to the database

    :param file f_channels: the file that will be read into the database
    """
    channels = []
    
    for line in f_channels:
        channels.append(readSiteChanStringToSiteChan(line))

    for chan in channels:
        insertSiteChan2Database(chan)
