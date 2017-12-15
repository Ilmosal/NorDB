import psycopg2
import logging

from nordb.core import usernameUtilities
from nordb.database.sql2nordic import add_float_to_string, add_integer_to_string, add_string_to_string
from nordb.database.station2sql import Sensor

username = ""

SELECT_SENSOR = (   
                    "SELECT " +
                        "time, endtime, jdate, calratio, calper, " +
                        "tshift, instant, lddate, sitechan_css_link.css_id, " +
                        "instrument_css_link.css_id, sensor.id, station_code, channel_code " +

                    "FROM " +
                        "sensor, instrument_css_link, sitechan_css_link, station, sitechan " +
                    "WHERE " + 
                        "sensor.instrument_id = instrument_css_link.instrument_id " +
                    "AND " +
                        "sensor.channel_id = sitechan_css_link.sitechan_id " +
                    "AND " +
                        "sensor.id = %s " +
                    "AND " +
                        "sitechan.id = channel_id " +
                    "AND " +
                        "station.id = sitechan.station_id " +
                    "ORDER BY " +
                        "station_code "
                )

def createSensorString(sensor):
    """
    Function for creating a css sensor string from a sensor object.

    Args:
        sensor (list()): sensor array described by Sensor object

    Returns:
        The sensor string in a css format
    """
    sensorString = ""

    sensorString += add_string_to_string(sensor[Sensor.STATION_CODE], 6, '<')
    sensorString += add_string_to_string(sensor[Sensor.CHANNEL_CODE], 8, '<')
    sensorString += "   "
    sensorString += add_float_to_string(sensor[Sensor.TIME], 16, 5, '>')
    sensorString += "  "
    sensorString += add_float_to_string(sensor[Sensor.ENDTIME], 16, 5, '>')
    sensorString += " "
    sensorString += add_integer_to_string(sensor[Sensor.INSTRUMENT_ID], 8, '>')
    sensorString += " "
    sensorString += add_integer_to_string(sensor[Sensor.CHANNEL_ID], 8, '>')
    sensorString += "  "
    
    if sensor[Sensor.JDATE] is None:
        sensorString += add_integer_to_string(-1, 7, '>')
    else:
        sensorString += add_integer_to_string(sensor[Sensor.JDATE].year, 4, '<')
        sensorString += add_integer_to_string(sensor[Sensor.JDATE].timetuple().tm_yday, 3, '0')
    
    sensorString += " "
    sensorString += add_float_to_string(sensor[Sensor.CALRATIO], 16, 6, '>')
    sensorString += " "
    sensorString += add_float_to_string(sensor[Sensor.CALPER], 16, 6, '>')
    sensorString += " "
    sensorString += add_float_to_string(sensor[Sensor.TSHIFT], 6, 4, '>') 
    sensorString += " "
    sensorString += add_string_to_string(sensor[Sensor.INSTANT], 1, '>')
    sensorString += "       "

    if sensor[Sensor.LDDATE] is None:
        sensorString += add_integer_to_string(-1, 10, '>')
    else:
        sensorString += add_string_to_string(sensor[Sensor.LDDATE].strftime("%Y-%b-%d"), 10, '<')

    return sensorString

def readSensor(sensor_id):
    """
    Function for reading a sensor from database by id 

    Args:
        sensor_id(int): id of the sensor wanted

    Returns:
        sensor(lis): sensor list
    """
    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return None

    cur = conn.cursor()

    cur.execute(SELECT_SENSOR, (sensor_id, ))
    ans = cur.fetchone()
    
    conn.close()

    return ans

def sql2Sensor(sensor_ids, output_path):
    """
    Function for reading sensors from database and dumping them into a sensors.sensor file

    Args:
        sensor_ids (int[]): Array of integers
        output_path (str[]): path to output file
    """
    username = usernameUtilities.readUsername()

    sensors = []

    for sensor_id in sensor_ids:
        sensors.append(readSensor(sensor_id))

    f = open(output_path, "w")

    for sensor in sensors:
        f.write(createSensorString(sensor) + '\n')

def writeAllSensors(output_path):
    """
    Function for writing all sensors to a sensor file

    Args:
        output_path(str): path to output_file
    """
    username = usernameUtilities.readUsername()

    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        print ("Error connecting to the database")
        return

    cur = conn.cursor()

    cur.execute("SELECT sensor.id FROM sensor, station, sitechan WHERE sensor.channel_id = sitechan.id AND station.id = station_id ORDER BY station_code;")
    ans = cur.fetchall()

    conn.close()

    sensor_ids = []

    if not ans:
        print ("No stations in the database")
        return

    for a in ans:
        sensor_ids.append(a[0])

    sql2Sensor(sensor_ids, output_path)
