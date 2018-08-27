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

def sensors2sitechans(sitechans, station_date=datetime.datetime.now(), db_conn = None):
    """
    Function for getting all sensors quickly attached to a array of sitechans.
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    sitechan_ids = []

    for site in sitechans:
        sitechan_ids.append(site.s_id)

    sitechan_ids = tuple(sitechan_ids)

    unix_time = time.mktime(station_date.timetuple())

    cur = conn.cursor()
    cur.execute(SELECT_SENSORS, {'sitechan_ids':sitechan_ids,
                                'station_date':unix_time})

    ans = cur.fetchall()

    sensors = []

    for a in ans:
        sensor = Sensor(a[:-1])
        sensors.append(sensor)
        for chan in sitechans:
            if chan.s_id == sensor.channel_id:
                chan.sensors.append(sensor)

    if len(ans) != 0:
        sql2instrument.instruments2sensors( sensors,
                                            db_conn=conn)

    if db_conn is None:
        conn.close()

