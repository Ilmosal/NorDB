"""
This module contains a function for validating a :class:`.Sensor`.

Functions and Classes
---------------------
"""

from nordb.validation.validationTools import *
import nordb.database.station2sql

def validateSensor(sensor):
    """
    Function for validating the Sensor data for one line

    :param Sensor sensor: a array of string that contain the data to be validated
    :returns: true or false depending on if the data goes through validation or not
    """
    validation = True
    mstat = 13

    s2s = nordb.database.station2sql

    if not validateFloat(   sensor.data[sensor.TIME],
                            "time",
                            0.00000000000,
                            9999999999.999,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   sensor.data[sensor.ENDTIME],
                            "endtime",
                            0.00000000000,
                            9999999999.999,
                            True,
                            mstat):
        validation = False

    if not validateDate(    sensor.data[sensor.JDATE],
                            "jdate",
                            mstat):
        validation = False

    if not validateFloat(   sensor.data[sensor.CALRATIO],
                            "calratio",
                            -1.0,
                            10.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   sensor.data[sensor.CALPER],
                            "calper",
                            -1.0,
                            50.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   sensor.data[sensor.TSHIFT],
                            "tshift",
                            -1.0,   
                            9.9,
                            True,
                            mstat):
        validation = False

    if not validateString(  sensor.data[sensor.INSTANT],
                            "instant",
                            1,
                            1,
                            "yn",
                            True,
                            mstat):
        validation = False

    if not validateDate(    sensor.data[sensor.LDDATE],
                            "lddate",
                            mstat):
        validation = False

    return validation
