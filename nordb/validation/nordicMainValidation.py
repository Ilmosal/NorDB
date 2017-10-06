import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values

def validateMainHeader(nordic_main):
    validation = True
    mheader = 1

    validationTools.fixDate(nordic_main)

    if not validationTools.validateDate(nordic_main.date,
                                                "date",
                                                mheader):
        validation = False

    
    if not validationTools.validateInteger(nordic_main.hour,
                                                "hour",
                                                0,
                                                23,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateInteger(nordic_main.minute,
                                                "minute",
                                                0,
                                                59,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(nordic_main.second,
                                                "second",
                                                0.0,
                                                59.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(nordic_main.location_model,
                                                "location model",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(nordic_main.distance_indicator,
                                                "distance indicator",
                                                0,
                                                1,
                                                "LRD",
                                                True,
                                                mheader):
        validation = False

    #TODO these limitations
    if not validationTools.validateString(nordic_main.event_desc_id,
                                                "event description id",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(nordic_main.epicenter_latitude,
                                                "epicenter latitude",
                                                -90.0,
                                                90.0,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(nordic_main.epicenter_longitude,
                                                "epicenter longitude",
                                                -180.0,
                                                180.0,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(nordic_main.depth,
                                                "depth",
                                                0.0,
                                                999.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(nordic_main.depth_control,
                                                "depth control",
                                                0,
                                                1,
                                                "FSG",
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(nordic_main.locating_indicator,
                                                "locating indicator",
                                                0,
                                                1,
                                                "FS",
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(nordic_main.epicenter_reporting_agency,
                                                "epicenter reporting agency",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateInteger(nordic_main.stations_used,
                                                "stations used",
                                                0,
                                                999,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(nordic_main.rms_time_residuals,
                                                "rms time residuals",
                                                -9.9,
                                                99.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(nordic_main.magnitude_1,
                                                "magnitude 1",
                                                0.0,
                                                9.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(nordic_main.type_of_magnitude_1,
                                                "type of magnitude 1",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(nordic_main.magnitude_reporting_agency_1,
                                                "magnitude reporting agency 1",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(nordic_main.magnitude_2,
                                                "magnitude 2",
                                                0.0,
                                                9.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(nordic_main.type_of_magnitude_2,
                                                "type of magnitude 2",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(nordic_main.magnitude_reporting_agency_2,
                                                "magnitude reporting agency 2",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False

    if not validationTools.validateFloat(nordic_main.magnitude_3,
                                                "magnitude 3",
                                                0.0,
                                                9.9,
                                                True,
                                                mheader):
        validation = False

    if not validationTools.validateString(nordic_main.type_of_magnitude_3,
                                                "type of magnitude 3",
                                                0,
                                                1,
                                                "",
                                                False,
                                                mheader):
        validation = False
    
    if not validationTools.validateString(nordic_main.magnitude_reporting_agency_3,
                                                "magnitude reporting agency 3",
                                                0,
                                                3,
                                                "",
                                                False,
                                                mheader):
        validation = False

    return validation   
