from nordb.validation.validationTools import validateDate, validateString, validateFloat, validateInteger
import nordb.database.station2sql

def validateSiteChan(channel):
    """
    Function fro validating sitechan data for one line.

    Args:
        station(str[]): a array of strings that contain the data

    Returns:
        True or False depending on if the data goes through validation or not
    """
    validation = True
    mstat = 11

    s2s = nordb.database.station2sql

    if not validateDate(    channel[s2s.SiteChan.ON_DATE],
                            "on date",
                            mstat):
        validation = False

    if not validateDate(    channel[s2s.SiteChan.OFF_DATE],
                            "off date",
                            mstat):
        validation = False

    if not validateString(  channel[s2s.SiteChan.CHANNEL_TYPE],
                            "channel type",
                            0,
                            4,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateFloat(   channel[s2s.SiteChan.EMPLACEMENT_DEPTH],
                            "emplacement depth",
                            0.0,
                            1.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   channel[s2s.SiteChan.HORIZONTAL_ANGLE],
                            "horizontal angle",
                            -1.0,
                            360.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   channel[s2s.SiteChan.VERTICAL_ANGLE],
                            "vertical angle",
                            -90.0,
                            90.0,
                            True,
                            mstat):
        validation = False

    if not validateString(  channel[s2s.SiteChan.DESCRIPTION],
                            "description",
                            0,
                            50,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateDate(    channel[s2s.SiteChan.LOAD_DATE],
                            "load date",
                            mstat):
        validation = False

    return validation


