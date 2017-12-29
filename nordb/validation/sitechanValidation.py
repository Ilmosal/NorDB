"""
This module contains functions for validating :class:`.SiteChan`.

Functions and Classes
---------------------
"""

from nordb.validation.validationTools import validateDate
from nordb.validation.validationTools import validateString
from nordb.validation.validationTools import validateFloat
from nordb.validation.validationTools import validateInteger

def validateSiteChan(channel):
    """
    Function fro validating sitechan data for one line.

    :param SiteChan channel: a array of strings that contain the data
    :returns: true or false depending on if the data goes through validation or not
    """
    validation = True
    mstat = 11

    if not validateDate(    channel.data[channel.ON_DATE],
                            "on date",
                            mstat):
        validation = False

    if not validateDate(    channel.data[channel.OFF_DATE],
                            "off date",
                            mstat):
        validation = False

    if not validateString(  channel.data[channel.CHANNEL_TYPE],
                            "channel type",
                            0,
                            4,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateFloat(   channel.data[channel.EMPLACEMENT_DEPTH],
                            "emplacement depth",
                            0.0,
                            5.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   channel.data[channel.HORIZONTAL_ANGLE],
                            "horizontal angle",
                            -1.0,
                            360.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   channel.data[channel.VERTICAL_ANGLE],
                            "vertical angle",
                            -1.0,
                            180.0,
                            True,
                            mstat):
        validation = False

    if not validateString(  channel.data[channel.DESCRIPTION],
                            "description",
                            0,
                            50,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateDate(    channel.data[channel.LOAD_DATE],
                            "load date",
                            mstat):
        validation = False

    return validation


