"""
This module contains the validation function for validating an :class:`.Instrument`.

Functions and Classes
---------------------
"""

from nordb.validation.validationTools import *

def validateInstrument(instrument):
    """
    Function for validating Instrument data for one line.
    
    :param Instrument instrument: a array of string that contain the data to be validated
    :return: True or False depending on if the data goes through validation or not
    """
    validation = True
    mstat = 12

    if not validateString(  instrument.data[instrument.INSTRUMENT_NAME],
                            "instrument name",
                            0,
                            50,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateString(  instrument.data[instrument.INSTRUMENT_TYPE],
                            "instrument type",
                            0,
                            6,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateString(  instrument.data[instrument.BAND],
                            "band",
                            0,
                            1,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateString(  instrument.data[instrument.DIGITAL],
                            "digital",
                            0,
                            1,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateFloat(   instrument.data[instrument.SAMPRATE],
                            "samprate",
                            0.0,
                            1000.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   instrument.data[instrument.NCALIB],
                            "ncalib",
                            -1.0,
                            10000.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   instrument.data[instrument.NCALPER],
                            "ncalper",
                            -1.0,
                            10000.0,
                            True,
                            mstat):
        validation = False

    if not validateString(  instrument.data[instrument.DIR],
                            "dir",
                            0,
                            64,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateString(  instrument.data[instrument.DFILE],
                            "dfile",
                            0,
                            32,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateString(  instrument.data[instrument.RSPTYPE],
                            "rsptype",
                            0,
                            6,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateDate(    instrument.data[instrument.LDDATE],
                            "lddate",
                            mstat):
        validation = False

    return validation
