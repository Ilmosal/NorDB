"""
This module contains all functions and classes for reading a station file in `CSS3.0 format`_ and pushing it into the database

.. _CSS3.0 format: ftp://ftp.pmel.noaa.gov/newport/lau/tphase/data/css_wfdisc.pdf

Functions and Classes
---------------------
"""

import unidecode

from nordb.nordic.station import Station
from nordb.core import usernameUtilities
from nordb.database import creationInfo
STATION_INSERT =    (  
                    "INSERT INTO station " 
                        "(   station_code, on_date, off_date, " 
                            "latitude, longitude, elevation, " 
                            "station_name, station_type," 
                            "reference_station, north_offset, " 
                            "east_offset, load_date, network_id) " 
                    "VALUES " 
                        "(   %s, %s, %s, %s, %s, %s, %s, %s, " 
                            "%s, %s, %s, %s, %s);" 
                    )

STATION_UPDATE =    (
                    "UPDATE "
                    "   station "
                    "SET "
                    "   station_code = %s, "
                    "   on_date = %s, "
                    "   off_date = %s, "
                    "   latitude = %s, "
                    "   longitude = %s, "
                    "   elevation = %s, "
                    "   station_name = %s, "
                    "   station_type = %s, "
                    "   reference_station = %s, "
                    "   north_offset = %s, "
                    "   east_offset = %s, "
                    "   load_date = %s, "
                    "   network_id = %s "
                    "WHERE "
                    "   id = %s;"
                    )

SEARCH_STATIONS =   ( 
                    "SELECT " 
                    "   id "
                    "FROM "
                    "   station "
                    "WHERE "
                    "   station_code = %s "
                    "AND "
                    "   (off_date is null OR (off_date < %s OR on_date > %s ));"
                    )   

def getNetworkID(network, privacy_level):
    """
    Function for inserting the information to the database. If network doesn't already exist, the function adds the network to the database.

    :param array station: Array of all station related information in their correct spaces
    :return: network id inserted to the database
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM network WHERE network = %s", (network.strip(),))
        ans = cur.fetchone()

        if ans is None:
            c_id = creationInfo.createCreationInfo(privacy_level)
            cur.execute("INSERT INTO network (network, creation_id) VALUES (%s, %s) RETURNING id", (network.strip(), c_id))
            ans = cur.fetchone()
    except Exception as e:
        conn.close()
        raise e
    conn.commit()
    conn.close()

    return ans[0]

def insertStation2Database(station, network, privacy_level = 'public'):
    """
    Function for inserting the station to the database. If the station with the given code already exists the function will replace the old one.

    :param station Station: station that will be inserted to the database
    :param network str: network to which this station belongs to
    :param privacy_level str: The privacy level of the network if it is going to be a new one
    """
    if privacy_level not in ['public', 'secure', 'private']:
        raise Exception("Privacy level not a valid one. Has to be one of: 'public', 'secure', 'private'. ({0})".format(privacy_level))

    network_id = getNetworkID(network, privacy_level)
    station.network_id = network_id

    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    try:
        cur.execute(SEARCH_STATIONS, (  station.station_code, 
                                        station.on_date,
                                        station.off_date))
        ans = cur.fetchone()

        if ans is not None:
            update_list = station.getAsList()
            update_list.append(ans[0])
            cur.execute(STATION_UPDATE, update_list)
        else:
            cur.execute(STATION_INSERT, station.getAsList())
    except Exception as e:
        conn.close()
        raise e

    conn.commit()
    conn.close()
