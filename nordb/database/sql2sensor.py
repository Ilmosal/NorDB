"""
This module contains all information for getting the sensor information out of the database. 

Functions and Classes
---------------------
"""


from nordb.database import sql2instrument
from nordb.core import usernameUtilities
from nordb.nordic.sensor import Sensor

SELECT_SENSOR = (   
                    "SELECT " 
                    "   time, endtime, jdate, calratio, calper, " 
                    "   tshift, instant, sensor.lddate, sitechan.css_id, " 
                    "   instrument.css_id, sensor.id, station_code, channel_code, " 
                    "   sitechan.id, instrument.id "
                    "FROM " 
                    "   sensor, instrument, station, sitechan " 
                    "WHERE " 
                    "   sensor.id = %s " 
                    "AND " 
                    "   sitechan.id = sensor.sitechan_id " 
                    "AND "
                    "   instrument.id = sensor.instrument_id "
                    "AND " 
                    "   station.id = sitechan.station_id " 
                    "ORDER BY " 
                    "   station_code "
                )

ALL_SENSORS = (   
                    "SELECT " 
                    "   time, endtime, jdate, calratio, calper, " 
                    "   tshift, instant, sensor.lddate, sitechan.css_id, " 
                    "   instrument.css_id, sensor.id, station_code, channel_code, " 
                    "   sitechan.id, instrument.id "
                    "FROM " 
                    "    sensor, instrument, station, sitechan " 
                    "WHERE "  
                    "   sensor.instrument_id = instrument.id " 
                    "AND " 
                    "   sensor.sitechan_id = sitechan.id " 
                    "AND " 
                    "   station.id = sitechan.station_id " 
                    "ORDER BY " 
                    "   station_code "
                )

SELECT_SENSORS_TO_SITECHAN =    (
                                "SELECT "
                                "   sensor.id "
                                "FROM "
                                "   sensor, sitechan "
                                "WHERE "
                                "   sitechan.id = %s "
                                "AND "
                                "   sitechan.id = sensor.sitechan_id"
                                )

def getAllSensors():
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
        sen = Sensor(a)
        sql2instrument.instruments2sensor(sen)
        sensors.append(sen) 

    return sensors

def sensors2sitechan(sitechan):
    """
    Function for attaching all sensors related to a sitechan to the sitechan 

    :param SiteChan sitechan: sitechan to which the sensors will be attached to
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(SELECT_SENSORS_TO_SITECHAN, (sitechan.s_id,))
    sensor_ids = cur.fetchall()

    if sensor_ids:
        for sensor_id in sensor_ids:
            sitechan.sensors.append(getSensor(sensor_id,))

    conn.close()

def getSensor(sensor_id):
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
    sen = Sensor(ans)
    
    sql2instrument.instruments2sensor(sen)

    return sen
