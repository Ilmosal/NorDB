from nordb.validation import validationTools
import nordb.io.station2sql

def validateStation(station):
    """
    Method for validating the Station data for one line.

    Args:
        station (str[]): a array of strings that contain the data to be validated

    Returns:
        True or False depending on if the data goes through validation or not        
    """
    validation = True
    mstat = 10
 
    s2s = nordb.io.station2sql

    if not validationTools.validateString(station[s2s.Station.STATION_CODE],
                                            "station code",
                                            0,  
                                            6,
                                            None,
                                            False,
                                            mstat):
        validation = False
   
    if not validationTools.validateDate(station[s2s.Station.ON_DATE],
                                            " on date",
                                            mstat):
        validation = False

    if not validationTools.validateDate(station[s2s.Station.OFF_DATE],
                                            "off date",
                                            mstat):
        validation = False

    if not validationTools.validateFloat(station[s2s.Station.LATITUDE],
                                            "latitude",
                                            -90.0,  
                                            90.0,
                                            True,
                                            mstat):
        validation = False

    if not validationTools.validateFloat(station[s2s.Station.LONGITUDE],
                                            "longitude",
                                            -180.0,  
                                            180.0,
                                            True,
                                            mstat):
        validation = False    

    if not validationTools.validateFloat(station[s2s.Station.ELEVATION],
                                            "elevation",
                                            -10.0,  
                                            10.0,
                                            True,
                                            mstat):
        validation = False

    if not validationTools.validateString(station[s2s.Station.STATION_NAME],
                                            "station name",
                                            0,  
                                            50,
                                            None,
                                            False,
                                            mstat):
        validation = False

    if not validationTools.validateString(station[s2s.Station.STATION_TYPE],
                                            "station type",
                                            2,  
                                            2,
                                            ["ss","bb","ll", "ar"],
                                            True,
                                            mstat):
        validation = False

    if not validationTools.validateString(station[s2s.Station.REFERENCE_STATION],
                                            "reference station",
                                            0,  
                                            6,
                                            None,
                                            False,
                                            mstat):
        validation = False

    if not validationTools.validateFloat(station[s2s.Station.NORTH_OFFSET],
                                            "north offset",
                                            -10.0,  
                                            10.0,
                                            True,
                                            mstat):
        validation = False

    if not validationTools.validateFloat(station[s2s.Station.EAST_OFFSET],
                                            "east offset",
                                            -10.0,  
                                            10.0,
                                            True,
                                            mstat):
        validation = False

    if not validationTools.validateDate(station[s2s.Station.LOAD_DATE],
                                            "load date",
                                            mstat):
        validation = False

    return validation
