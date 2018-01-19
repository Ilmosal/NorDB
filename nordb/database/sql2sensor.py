"""
This module contains all information for getting the sensor information out of the database. 

Functions and Classes
---------------------
"""

import psycopg2
import logging

from nordb.core import usernameUtilities
from nordb.core.utils import addFloat2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addString2String
from nordb.database.station2sql import Sensor

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

    :param array sensor: sensor array described by Sensor object
    :returns: The sensor string in a css format
    """
    sensorString = ""

    sensorString += addString2String(sensor[Sensor.STATION_CODE], 6, '<')
    sensorString += addString2String(sensor[Sensor.CHANNEL_CODE], 8, '<')
    sensorString += "   "
    sensorString += addFloat2String(sensor[Sensor.TIME], 16, 5, '>')
    sensorString += "  "
    sensorString += addFloat2String(sensor[Sensor.ENDTIME], 16, 5, '>')
    sensorString += " "
    sensorString += addInteger2String(sensor[Sensor.INSTRUMENT_ID], 8, '>')
    sensorString += " "
    sensorString += addInteger2String(sensor[Sensor.CHANNEL_ID], 8, '>')
    sensorString += "  "
    
    if sensor[Sensor.JDATE] is None:
        sensorString += addInteger2String(-1, 7, '>')
    else:
        sensorString += addInteger2String(sensor[Sensor.JDATE].year, 4, '<')
        sensorString += addInteger2String(sensor[Sensor.JDATE].timetuple().tm_yday, 3, '0')
    
    sensorString += " "
    sensorString += addFloat2String(sensor[Sensor.CALRATIO], 16, 6, '>')
    sensorString += " "
    sensorString += addFloat2String(sensor[Sensor.CALPER], 16, 6, '>')
    sensorString += " "
    sensorString += addFloat2String(sensor[Sensor.TSHIFT], 6, 4, '>') 
    sensorString += " "
    sensorString += addString2String(sensor[Sensor.INSTANT], 1, '>')
    sensorString += "       "

    if sensor[Sensor.LDDATE] is None:
        sensorString += addInteger2String(-1, 10, '>')
    else:
        sensorString += addString2String(sensor[Sensor.LDDATE].strftime("%Y-%b-%d"), 10, '<')

    return sensorString

def readSensor(sensor_id):
    """
    Function for reading a sensor from database by id 

    :param int sensor_id: id of the sensor wanted
    :returns: sensor list
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(SELECT_SENSOR, (sensor_id, ))
    ans = cur.fetchone()
    
    conn.close()

    return ans

def sql2Sensor(sensor_ids, output_path):
    """
    Function for reading sensors from database and dumping them into a sensors.sensor file

    :param array sensor_ids: Array of integers
    :param str output_path: path to output file
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

    :param str output_path: path to output_file
    """
    conn = usernameUtilities.log2nordb() 
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
