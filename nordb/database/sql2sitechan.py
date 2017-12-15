import logging
import psycopg2

from nordb.database.station2sql import SiteChan
from nordb.core import usernameUtilities
from nordb.database.sql2nordic import add_float_to_string, add_integer_to_string, add_string_to_string

username = ""

SELECT_SITECHAN =  ("SELECT"                                                            +
                    "   station.station_code, sitechan.channel_code, sitechan.on_date, sitechan.off_date, "    +
                    "   sitechan.channel_type, sitechan.emplacement_depth,"             +
                    "   sitechan.horizontal_angle, sitechan.vertical_angle,"            +
                    "   sitechan.description, sitechan.load_date, sitechan.id, "        +
                    "   sitechan_css_link.css_id "                                      +
                    "FROM "                                                             +
                    "   sitechan, station, sitechan_css_link "                          +
                    "WHERE "                                                            +
                    "   sitechan.id = %s "                                              +
                    "AND "                                                              +
                    "   station.id = sitechan.station_id "                              +
                    "AND "                                                              +
                    "   sitechan_css_link.sitechan_id = sitechan.id")


def createSiteChanString(channel):
    """
    Function for creating a sitechan string from a list of it's attributes

    Args:
        channel(list): list of attributes of the channel
    
    Returns:
        A sitechan line
    """
    sitechanString = ""

    sitechanString += add_string_to_string(channel[SiteChan.STATION_ID], 7, '<')
    sitechanString += add_string_to_string(channel[SiteChan.CHANNEL_CODE].strip(), 8, '<')
    sitechanString += "  "
    if channel[SiteChan.ON_DATE] is None:
        sitechanString += add_integer_to_string(-1, 7, '>')
    else:
        sitechanString += add_integer_to_string(channel[SiteChan.ON_DATE].year, 4, '<') 
        sitechanString += add_integer_to_string(channel[SiteChan.ON_DATE].timetuple().tm_yday, 3, '0') 
    
    sitechanString += "  "

    sitechanString += add_integer_to_string(channel[SiteChan.CSS_ID], 7, '>')

    sitechanString += "  "

    if channel[SiteChan.OFF_DATE] is None:
        sitechanString += add_integer_to_string(-1, 7, '>')
    else:
        sitechanString += add_integer_to_string(channel[SiteChan.OFF_DATE].year, 4, '<') 
        sitechanString += add_integer_to_string(channel[SiteChan.OFF_DATE].timetuple().tm_yday, 3, '0') 

    sitechanString += " "
    sitechanString += add_string_to_string(channel[SiteChan.CHANNEL_TYPE], 4, '<')

    sitechanString += add_float_to_string(channel[SiteChan.EMPLACEMENT_DEPTH], 10, 4, '>')
    sitechanString += "  "
    sitechanString += add_float_to_string(channel[SiteChan.HORIZONTAL_ANGLE], 5, 1, '>')
    sitechanString += "  "
    sitechanString += add_float_to_string(channel[SiteChan.VERTICAL_ANGLE], 5, 1, '>')
    sitechanString += " "
    sitechanString += add_string_to_string(channel[SiteChan.DESCRIPTION], 50, '<')
    sitechanString += " "

    if channel[SiteChan.LOAD_DATE] is None:
        sitechanString += add_integer_to_string(-1, 10, '>')
    else:
        sitechanString += add_string_to_string(channel[SiteChan.LOAD_DATE].strftime("%Y-%b-%d"), 10, '<')

    return sitechanString

def readSitechan(sitechan_id):
    """
    Method for reading a sitechan from database by id.
    
    Args:
        sitechan_id(int): id of the sitechan wanted
    
    Seturns:
        sitechan as a list
    """
    try: 
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except psycopg.Error as e:
        logging.error(e.pgerror)
        return None

    cur = conn.cursor()

    cur.execute(SELECT_SITECHAN, (sitechan_id,))
    ans = cur.fetchone()

    conn.close()

    return ans

def sql2sitechan(sitechan_ids, output_path):
    """
    Function for creating a sitechan file from all the sitechans with ids in station_ids in the db

    Args:
        sitechan_ids (int[]): Array of integers
        output_path (str): Path to the output file
    """
    sitechans = []

    for sitechan_id in sitechan_ids:
        sitechans.append(readSitechan(sitechan_id))

    f = open(output_path, 'w')

    for chan in sitechans:
        f.write(createSiteChanString(chan) + "\n")

def writeAllSitechans(output_path):
    """
    Function for writing all sitechans into a sitechan file

    Args:
        output_path (str): path to outputfile
    """
    username = usernameUtilities.readUsername()

    try: 
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return None

    cur = conn.cursor()

    cur.execute("SELECT id FROM sitechan")
    ans = cur.fetchall()

    conn.close()
  
    if not ans:
        logging.error("No sitechans in the database")
        return
 
    sitechan_ids = []

    for a in ans: 
        sitechan_ids.append(a[0])

    sql2sitechan(sitechan_ids, output_path)
