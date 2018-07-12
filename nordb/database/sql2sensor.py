"""
This module contains all information for getting the sensor information out of the database.

Functions and Classes
---------------------
"""

import datetime
import time

from nordb.database import sql2instrument
from nordb.core import usernameUtilities
from nordb.nordic.sensor import Sensor

SELECT_SENSORS =    (
                    "SELECT "
                    "   time, endtime, jdate, calratio, calper, "
                    "   tshift, instant, sensor.lddate, sitechan.css_id, "
                    "   instrument.css_id, sensor.id, station_code, channel_code, "
                    "   sitechan.id, instrument.id, station.id "
                    "FROM "
                    "   sensor, instrument, station, sitechan "
                    "WHERE "
                    "   sitechan.id IN %(sitechan_ids)s "
                    "AND "
                    "   sitechan.id = sensor.sitechan_id "
                    "AND "
                    "   instrument.id = sensor.instrument_id "
                    "AND "
                    "   station.id = sitechan.station_id "
                    "AND "
                    "   ( "
                    "       (sensor.time <= %(station_date)s AND "
                    "        sensor.endtime >= %(station_date)s) "
                    "   OR "
                    "       (sensor.time <= %(station_date)s AND "
                    "        sensor.endtime = 9999999999.999) "
                    "   ) "
                    )

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
                                "   sitechan.id = sensor.sitechan_id "
                                "AND "
                                "   ( "
                                "       (sensor.time <= %s AND "
                                "        sensor.endtime >= %s) "
                                "   OR "
                                "       (sensor.time <= %s AND "
                                "        sensor.endtime = 9999999999.999) "
                                "   ) "
                                )

def getAllSensors(db_conn = None):
    """
    Function for reading all sensors from the database and returning them to user.

    :returns: Array of :class:`Sensor` objects
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    cur.execute(ALL_SENSORS)

    ans = cur.fetchall()
    sensors = []
    for a in ans:
        sen = Sensor(a)
        sql2instrument.instruments2sensor(sen, db_conn=conn)
        sensors.append(sen)

    if db_conn is None:
        conn.close()

    return sensors

def sensors2stations(stations, station_date=datetime.datetime.now(), db_conn = None):
    """
    Function for getting all sensors quickly attached to a array of stations.
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    sitechan_ids = []

    for stat in stations.values():
        for sitechan in stat.sitechans:
            sitechan_ids.append(sitechan.s_id)

    sitechan_ids = tuple(sitechan_ids)

    unix_time = time.mktime(station_date.timetuple())

    cur = conn.cursor()
    cur.execute(SELECT_SENSORS, {'sitechan_ids':sitechan_ids,
                                'station_date':unix_time})

    ans = cur.fetchall()

    for a in ans:
        sensor = Sensor(a[:-1])
        for chan in stations[a[-1]].sitechans:
            if chan.s_id == sensor.channel_id:
                chan.sensors.append(sensor)

    if len(ans) != 0:
        sql2instrument.instruments2stations(stations,
                                            db_conn=conn)

    if db_conn is None:
        conn.close()

def sensors2sitechan(sitechan, station_date=datetime.datetime.now(), db_conn = None):
    """
    Function for attaching all sensors related to a sitechan to the sitechan

    :param SiteChan sitechan: sitechan to which the sensors will be attached to
    :param datetime station_date: date for getting the right sensor files
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    unix_time = time.mktime(station_date.timetuple())

    cur.execute(SELECT_SENSORS_TO_SITECHAN, (sitechan.s_id, unix_time,
                                             unix_time, unix_time))
    sensor_ids = cur.fetchall()

    if sensor_ids:
        for sensor_id in sensor_ids:
            sitechan.sensors.append(getSensor(sensor_id, station_date, db_conn=conn))

    if db_conn is None:
        conn.close()

def getSensor(sensor_id, station_date=datetime.datetime.now(), db_conn = None):
    """
    Function for reading a sensor from database by id

    :param int sensor_id: id of the sensor wanted
    :param datetime station_date: date for getting the right sensor files
    :returns: :class:`Sensor` object
    """
    unix_time = time.mktime(station_date.timetuple())

    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    cur.execute(SELECT_SENSOR, (sensor_id,))
    ans = cur.fetchone()
    sen = Sensor(ans)

    sql2instrument.instruments2sensor(sen, db_conn=conn)

    if db_conn is None:
        conn.close()
    return sen
