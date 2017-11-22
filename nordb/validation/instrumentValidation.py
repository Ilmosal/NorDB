from nordb.validation.validationTools import *
import nordb.database.station2sql

def validateInstrument(instrument):
    """
    Function for validating Instrument data for one line.
    
    Args:
        instrument (str[]): a array of string that contain the data to be validated

    Returns:
        True or False depending on if the data goes through validation or not
    """
    validation = True
    mstat = 12

    s2s = nordb.database.station2sql

    if not validateString(  instrument[s2s.Instrument.INSTRUMENT_NAME],
                            "instrument name",
                            0,
                            50,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateString(  instrument[s2s.Instrument.INSTRUMENT_TYPE],
                            "instrument type",
                            0,
                            6,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateString(  instrument[s2s.Instrument.BAND],
                            "band",
                            0,
                            1,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateString(  instrument[s2s.Instrument.DIGITAL],
                            "digital",
                            0,
                            1,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateFloat(   instrument[s2s.Instrument.SAMPRATE],
                            "samprate",
                            0.0,
                            1000.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   instrument[s2s.Instrument.NCALIB],
                            "ncalib",
                            -1.0,
                            10000.0,
                            True,
                            mstat):
        validation = False

    if not validateFloat(   instrument[s2s.Instrument.NCALPER],
                            "ncalper",
                            -1.0,
                            10000.0,
                            True,
                            mstat):
        validation = False

    if not validateString(  instrument[s2s.Instrument.DIR],
                            "dir",
                            0,
                            64,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateString(  instrument[s2s.Instrument.DFILE],
                            "dfile",
                            0,
                            32,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateString(  instrument[s2s.Instrument.RSPTYPE],
                            "rsptype",
                            0,
                            6,
                            None,
                            False,
                            mstat):
        validation = False

    if not validateDate(    instrument[s2s.Instrument.LDDATE],
                            "lddate",
                            mstat):
        validation = False

    return validation
