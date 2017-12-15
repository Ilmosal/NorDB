import logging
import psycopg2

from nordb.core import usernameUtilities
username = ""

FIND_STATION_QUERY =    (
                            "SELECT " +
                                "id " +
                            "FROM " +
                                "station " +
                            "WHERE " +
                                "station_code = %s " +
                            "AND " +
                                "network_id = %s " +
                            "AND " +
                                "on_date = %s " +
                            "AND " +
                                "off_date = %s " +
                            "AND " +
                                "latitude = %s " +
                            "AND " +
                                "longitude = %s " +
                            "AND " +
                                "elevation = %s " +
                            "AND " +
                                "station_name = %s " +
                            "AND " +
                                "station_type = %s " +
                            "AND " +
                                "reference_station = %s " +
                            "AND " +
                                "north_offset = %s " +
                            "AND " +
                                "east_offset = %s " +
                            "AND " +
                                "load_date= %s " +
                        )

def checkForSameStation(site):
    """
    Function that Tries to find stations with exactly same information and skip adding these sites if they exist.

    Returns:
        True or False depending on if a same event was found
    """
    cur = usernameUtilities.log2Database() 
   
    try:
        cur.execute(FIND_STATION_QUERY, (site[:13])) 
    except psycopg2.Error as e:
        logging.error("Problems with postgres query! Error: {0}".format(e))
        
    ans = cur.fetchall()

    
    
    pass

def checkForSameChannel(sitechan):
    """

    """
    pass

def checkForSameInstrument(instrument):
    """
    """
    pass

def checkForSameSensor(sensor):
    """

    """
    pass

    
