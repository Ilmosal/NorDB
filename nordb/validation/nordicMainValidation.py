"""
This module contains a function for validating a :class:`.NordicMain`.

Functions and Classes
---------------------
"""

import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values

def validateMainHeader(main):
    """
    Function for validating that the main header line is in correct format.

    :param NordicMain main: nordic main header to be validated
    :returns: true if the file is valid, false if not
   
    """
    validation = True
    mheader = 1

    validationTools.fixDate(main)

    if not validationTools.validateDate(main.header[main.DATE],
                                                "date",
                                                mheader):
        validation = False

    
    if not validationTools.validateInteger(main.header[main.HOUR],
                                                "hour",
                                                0,
                                                23,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateInteger(main.header[main.MINUTE],
                                                "minute",
                                                0,
                                                59,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(main.header[main.SECOND],
                                                "second",
                                                0.0,
                                                59.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(main.header[main.LOCATION_MODEL],
                                                "location model",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(main.header[main.DISTANCE_INDICATOR],
                                                "distance indicator",
                                                0,
                                                1,
                                                "LRD",
                                                True,
                                                mheader):
        validation = False

    #TODO these limitations
    if not validationTools.validateString(main.header[main.EVENT_DESC_ID],
                                                "event description id",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(main.header[main.EPICENTER_LATITUDE],
                                                "epicenter latitude",
                                                -90.0,
                                                90.0,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(main.header[main.EPICENTER_LONGITUDE],
                                                "epicenter longitude",
                                                -180.0,
                                                180.0,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(main.header[main.DEPTH],
                                                "depth",
                                                0.0,
                                                999.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(main.header[main.DEPTH_CONTROL],
                                                "depth control",
                                                0,
                                                1,
                                                "FSGA",
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(main.header[main.LOCATING_INDICATOR],
                                                "locating indicator",
                                                0,
                                                1,
                                                "FS",
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(main.header[main.EPICENTER_REPORTING_AGENCY],
                                                "epicenter reporting agency",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateInteger(main.header[main.STATIONS_USED],
                                                "stations used",
                                                0,
                                                999,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(main.header[main.RMS_TIME_RESIDUALS],
                                                "rms time residuals",
                                                -9.9,
                                                99.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(main.header[main.MAGNITUDE_1],
                                                "magnitude 1",
                                                -1.0,
                                                9.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(main.header[main.TYPE_OF_MAGNITUDE_1],
                                                "type of magnitude 1",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(main.header[main.MAGNITUDE_REPORTING_AGENCY_1],
                                                "magnitude reporting agency 1",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(main.header[main.MAGNITUDE_2],
                                                "magnitude 2",
                                                -1.0,
                                                9.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(main.header[main.TYPE_OF_MAGNITUDE_2],
                                                "type of magnitude 2",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(main.header[main.MAGNITUDE_REPORTING_AGENCY_2],
                                                "magnitude reporting agency 2",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(main.header[main.MAGNITUDE_3],
                                                "magnitude 3",
                                                -1.0,
                                                9.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(main.header[main.TYPE_OF_MAGNITUDE_3],
                                                "type of magnitude 3",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(main.header[main.MAGNITUDE_REPORTING_AGENCY_3],
                                                "magnitude reporting agency 3",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False

    return validation   
