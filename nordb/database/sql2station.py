import logging
import psycopg2

from nordb.database.station2sql import Station
from nordb.core import usernameUtilities
from nordb.database.sql2nordic import add_float_to_string, add_integer_to_string, add_string_to_string

username = ""

def createStationString(station):
    """
    Function for creating a css stations string from a Station object.

    Args:
        station (Station): Station object that will be parsed into a string
    Returns:
        The station string in a css format
    """
    stationString = ""
    stationString += add_string_to_string(station[Station.STATION_CODE], 8, '<')

    stationString += add_integer_to_string(station[Station.ON_DATE].year, 5, '<') 
    stationString += add_integer_to_string(station[Station.ON_DATE].timetuple().tm_yday, 3, '0') 
    
    stationString += "  "

    if station[Station.OFF_DATE] is None:
        stationString += add_integer_to_string(-1, 7, '>')
    else:
        stationString += add_integer_to_string(station[Station.OFF_DATE].year, 4, '<') 
        stationString += add_integer_to_string(station[Station.OFF_DATE].timetuple().tm_yday, 3, '0') 

    stationString += "  "
    stationString += add_float_to_string(station[Station.LATITUDE], 8, 4, '>')
    stationString += "  "
    stationString += add_float_to_string(station[Station.LONGITUDE], 8, 4, '>')

    stationString += " "
    stationString += add_float_to_string(station[Station.ELEVATION], 9, 4, '>')

    stationString += " "
    stationString += add_string_to_string(station[Station.STATION_NAME], 50, '<')

    stationString += " "
    stationString += add_string_to_string(station[Station.STATION_TYPE], 2, '<')

    stationString += "   "
    stationString += add_string_to_string(station[Station.REFERENCE_STATION], 8, '<')

    stationString += " "
    stationString += add_float_to_string(station[Station.NORTH_OFFSET], 7, 4, '>')

    stationString += "   "
    stationString += add_float_to_string(station[Station.EAST_OFFSET], 7, 4, '>')

    stationString += " "
    stationString += add_string_to_string(station[Station.LOAD_DATE].strftime("%Y-%b-%d"), 10, '<')

    return stationString

def readStation(station_id):
    """
    Function for reading a station from database by id.

    Args:
        station_id (int): id of the station wanted
    
    Returns:
        station (list): station as a list 
    """
    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return None

    cur = conn.cursor()

    cur.execute("SELECT station_code, on_date, off_date, latitude, longitude, elevation, station_name, station_type, reference_station, north_offset, east_offset, load_date, id FROM station WHERE id = %s", (station_id,))

    ans = cur.fetchone()

    conn.close()

    return ans

def sql2station(station_ids, output_path):
    """
    Function for reading stations from the database and dumping them to a stations.site file

    Args:
        station_ids (int[]): Array of Integers
        output_path (str): path to the output file
    """
    username = usernameUtilities.readUsername() 

    stations = []
    
    for station_id in station_ids:
        stations.append(readStation(station_id))

    f = open(output_path, 'w')

    for station in stations:
        f.write(createStationString(station) + '\n')

def writeAllStations(output_path):
    """
    Function for writing all stations to a site file.

    Args:
        output_path(str): path to output file
    """
    username = usernameUtilities.readUsername() 

    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return 

    cur = conn.cursor()

    cur.execute("SELECT id FROM station;")

    ans = cur.fetchall()

    conn.close()
    
    station_ids = []

    if not ans:
        print("No stations in the database!")
        return

    for a in ans:
        station_ids.append(a[0])

    sql2station(station_ids, output_path)
