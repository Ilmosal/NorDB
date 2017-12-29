"""
Module containing a function for validating a :class:`.Station`.

Functions and Classes
---------------------
"""

from nordb.validation import validationTools

def validateStation(station):
    """
    Method for validating the Station data for one line.

    :param Station station: Station object that will be validated
    :returns: true or false depending on if the data goes through validation or not        
    """
    validation = True
    mstat = 10
 
    if not validationTools.validateString(station.data[station.STATION_CODE],
                                            "station code",
                                            0,  
                                            6,
                                            None,
                                            False,
                                            mstat):
        validation = False
   
    if not validationTools.validateDate(station.data[station.ON_DATE],
                                            " on date",
                                            mstat):
        validation = False

    if not validationTools.validateDate(station.data[station.OFF_DATE],
                                            "off date",
                                            mstat):
        validation = False

    if not validationTools.validateFloat(station.data[station.LATITUDE],
                                            "latitude",
                                            -90.0,  
                                            90.0,
                                            True,
                                            mstat):
        validation = False

    if not validationTools.validateFloat(station.data[station.LONGITUDE],
                                            "longitude",
                                            -180.0,  
                                            180.0,
                                            True,
                                            mstat):
        validation = False    

    if not validationTools.validateFloat(station.data[station.ELEVATION],
                                            "elevation",
                                            -10.0,  
                                            10.0,
                                            True,
                                            mstat):
        validation = False

    if not validationTools.validateString(station.data[station.STATION_NAME],
                                            "station name",
                                            0,  
                                            50,
                                            None,
                                            False,
                                            mstat):
        validation = False

    if not validationTools.validateString(station.data[station.STATION_TYPE],
                                            "station type",
                                            1,  
                                            2,
                                            ["b", "ss","bb","ll", "ar"],
                                            True,
                                            mstat):
        validation = False

    if not validationTools.validateString(station.data[station.REFERENCE_STATION],
                                            "reference station",
                                            0,  
                                            6,
                                            None,
                                            False,
                                            mstat):
        validation = False

    if not validationTools.validateFloat(station.data[station.NORTH_OFFSET],
                                            "north offset",
                                            -100.0,  
                                            100.0,
                                            True,
                                            mstat):
        validation = False

    if not validationTools.validateFloat(station.data[station.EAST_OFFSET],
                                            "east offset",
                                            -100.0,  
                                            100.0,
                                            True,
                                            mstat):
        validation = False

    if not validationTools.validateDate(station.data[station.LOAD_DATE],
                                            "load date",
                                            mstat):
        validation = False

    return validation
