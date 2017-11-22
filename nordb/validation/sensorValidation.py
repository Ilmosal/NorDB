from nordb.validation.validationTools import *
import nordb.database.station2sql

def validateSensor(sensor):
    """
    Function for validating the Sensor data for one line

    Args:
        sensor (str[]): a array of string that contain the data to be validated

    Returns:
        True or False depending on if the data goes through validation or not
    """
    validation = True
    mstat = 13

    s2s = nordb.database.station2sql

    if not validateFloat(   sensor[s2s.Sensor.TIME],
                            "time",
                            0.00000000000,
                            9999999999.999,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   sensor[s2s.Sensor.ENDTIME],
                            "endtime",
                            0.00000000000,
                            9999999999.999,
                            True,
                            mstat):
        validation = False

    if not validateDate(    sensor[s2s.Sensor.JDATE],
                            "jdate",
                            mstat):
        validation = False

    if not validateFloat(   sensor[s2s.Sensor.CALRATIO],
                            "calratio",
                            -1.0,
                            10.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   sensor[s2s.Sensor.CALPER],
                            "calper",
                            -1.0,
                            50.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   sensor[s2s.Sensor.TSHIFT],
                            "tshift",
                            -1.0,   
                            9.9,
                            True,
                            mstat):
        validation = False

    if not validateString(  sensor[s2s.Sensor.INSTANT],
                            "instant",
                            1,
                            1,
                            "yn",
                            True,
                            mstat):
        validation = False

    if not validateDate(    sensor[s2s.Sensor.LDDATE],
                            "lddate",
                            mstat):
        validation = False


    return validation
