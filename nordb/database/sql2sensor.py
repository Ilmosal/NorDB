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
from nordb.nordic.sensor import Sensor

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

ALL_SENSORS = (   
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
                        "sitechan.id = channel_id " +
                    "AND " +
                        "station.id = sitechan.station_id " +
                    "ORDER BY " +
                        "station_code "
                )

def readAllSensors():
    """
    Function for reading all sensors from the database and returning them to user.

    :returns: Array of :class:`Sensor` objects
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(ALL_SENSORS)

    ans = cur.fetchall()    
    conn.close()
    sensors = []
    for a in ans:
       sensors.append(Sensor(a)) 

    return sensors

def readSensor(sensor_id):
    """
    Function for reading a sensor from database by id 

    :param int sensor_id: id of the sensor wanted
    :returns: :class:`Sensor` object
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(SELECT_SENSOR, (sensor_id, ))
    ans = cur.fetchone()
    
    conn.close()

    return Sensor(ans)
