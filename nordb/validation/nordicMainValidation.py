import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values
from nordb.core.nordic import NordicMain

def validateMainHeader(header):
    """
    Function for validating that the main header line is in correct format.

    Args:
        header(NordicMain): nordic main header to be validated

    Returns:
        True if the file is valid, false if not
   
    """
    validation = True
    mheader = 1

    validationTools.fixDate(header)

    if not validationTools.validateDate(header.header[NordicMain.DATE],
                                                "date",
                                                mheader):
        validation = False

    
    if not validationTools.validateInteger(header.header[NordicMain.HOUR],
                                                "hour",
                                                0,
                                                23,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateInteger(header.header[NordicMain.MINUTE],
                                                "minute",
                                                0,
                                                59,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMain.SECOND],
                                                "second",
                                                0.0,
                                                59.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMain.LOCATION_MODEL],
                                                "location model",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(header.header[NordicMain.DISTANCE_INDICATOR],
                                                "distance indicator",
                                                0,
                                                1,
                                                "LRD",
                                                True,
                                                mheader):
        validation = False

    #TODO these limitations
    if not validationTools.validateString(header.header[NordicMain.EVENT_DESC_ID],
                                                "event description id",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMain.EPICENTER_LATITUDE],
                                                "epicenter latitude",
                                                -90.0,
                                                90.0,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMain.EPICENTER_LONGITUDE],
                                                "epicenter longitude",
                                                -180.0,
                                                180.0,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMain.DEPTH],
                                                "depth",
                                                0.0,
                                                999.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMain.DEPTH_CONTROL],
                                                "depth control",
                                                0,
                                                1,
                                                "FSGA",
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMain.LOCATING_INDICATOR],
                                                "locating indicator",
                                                0,
                                                1,
                                                "FS",
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMain.EPICENTER_REPORTING_AGENCY],
                                                "epicenter reporting agency",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateInteger(header.header[NordicMain.STATIONS_USED],
                                                "stations used",
                                                0,
                                                999,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMain.RMS_TIME_RESIDUALS],
                                                "rms time residuals",
                                                -9.9,
                                                99.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMain.MAGNITUDE_1],
                                                "magnitude 1",
                                                -1.0,
                                                9.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMain.TYPE_OF_MAGNITUDE_1],
                                                "type of magnitude 1",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(header.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_1],
                                                "magnitude reporting agency 1",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMain.MAGNITUDE_2],
                                                "magnitude 2",
                                                -1.0,
                                                9.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMain.TYPE_OF_MAGNITUDE_2],
                                                "type of magnitude 2",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(header.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_2],
                                                "magnitude reporting agency 2",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMain.MAGNITUDE_3],
                                                "magnitude 3",
                                                -1.0,
                                                9.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMain.TYPE_OF_MAGNITUDE_3],
                                                "type of magnitude 3",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(header.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_3],
                                                "magnitude reporting agency 3",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False

    return validation   
