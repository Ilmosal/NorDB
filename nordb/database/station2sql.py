"""
This module contains all functions and classes for reading a station file in `CSS3.0 format`_ and pushing it into the database

.. _CSS3.0 format: ftp://ftp.pmel.noaa.gov/newport/lau/tphase/data/css_wfdisc.pdf

Functions and Classes
---------------------
"""

import unidecode

from nordb.nordic.station import Station
from nordb.core import usernameUtilities
from nordb.core.utils import stringToDate

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



def readStationStringToStation(stat_line):
    """ 
    Function for reading Station object from a css site string

    :param str stat_line: css site string
    :returns: Station object   
    """

    stations = [None]*14
    
    stations[Station.STATION_CODE]      = unidecode.unidecode(stat_line[0:6].strip())
    stations[Station.ON_DATE]           = unidecode.unidecode(stringToDate(stat_line[8:15].strip()))
    stations[Station.OFF_DATE]          = unidecode.unidecode(stringToDate(stat_line[17:24].strip()))
    stations[Station.LATITUDE]          = unidecode.unidecode(stat_line[26:34].strip())
    stations[Station.LONGITUDE]         = unidecode.unidecode(stat_line[36:44].strip())
    stations[Station.ELEVATION]         = unidecode.unidecode(stat_line[47:54].strip())
    stations[Station.STATION_NAME]      = unidecode.unidecode(stat_line[55:106].strip())
    stations[Station.STATION_TYPE]      = unidecode.unidecode(stat_line[106:108].strip())
    stations[Station.REFERENCE_STATION] = unidecode.unidecode(stat_line[111:117].strip())
    stations[Station.NORTH_OFFSET]      = unidecode.unidecode(stat_line[119:127].strip())
    stations[Station.EAST_OFFSET]       = unidecode.unidecode(stat_line[130:137].strip())
    stations[Station.LOAD_DATE]         = unidecode.unidecode(stringToDate(stat_line[138:].strip()))
    stations[Station.NETWORK_ID]        = -1
    stations[Station.S_ID]              = -1

    return Station(stations)

def getNetworkID(network):
    """
    Function for inserting the information to the database. If network doesn't already exist, the function adds the network to the database.

    :param array station: Array of all station related information in their correct spaces
    :return: network id inserted to the database
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT id FROM network WHERE network = %s", (network.strip(),))
    ans = cur.fetchone()

    if ans is None:
        cur.execute("INSERT INTO network (network) VALUES (%s) RETURNING id", (network.strip(),))
        ans = cur.fetchone()

    conn.commit()
    conn.close()

    return ans[0]

def insertStation2Database(station, network):
    """ 
    Function for inserting the station to the database. If the station with the given code already exists the function will replace the old one.

    :param Station station: station that will be inserted to the database
    """
    network_id = getNetworkID(network)
    station.network_id = network_id

    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

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

    conn.commit()
    conn.close()

def readStations(f_station, network):
    """
    Function for reading a station file in css format and inserting them to the database
    
    :param file f_station: Station CSS file
    :param string network: name of the network
    """
    stations = []

    for line in f_station:
        stations.append(readStationStringToStation(line))

    for stat in stations:
        insertStation2Database(stat, network)
