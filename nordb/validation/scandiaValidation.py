"""
This module contains a function for validating a scandia file.

Functions and Classes
---------------------
"""

import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values
from nordb.validation import abbreviations

def validateScandiaHeader(scandia):
    """
    Function for validating a scandia header.
    
    :param scandia: scandia for validating
    :return: true or false depending on if the scandia goes through validation
    """
    validation = True
    mheader = 9
    global source_reference
    global magnitude_scale
    global region_code
    global macroseismic_reference
    
    if not validationTools.validateInteger(scandia.scandia_id,
                                            "scandia id",
                                            0,
                                            values.maxInt,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(scandia.source_ref,
                                            "source ref",
                                            3,
                                            3,
                                            source_reference.keys,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(scandia.origin_questionability,
                                            "origin questionability",
                                            0,
                                            1,
                                            "? ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateDate(scandia.date,
                                            "date",
                                            mheader):
        validation = False

    if not validationTools.validateString(scandia.event_desc,
                                            "event desc",
                                            "0",
                                            "1",
                                            "?dmsafrc ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateInteger(scandia.hour,
                                        "hour",
                                        0,
                                        23,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateInteger(scandia.minute,
                                        "minute",
                                        0,
                                        59,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(scandia.second,
                                        "second",
                                        0,
                                        59.999,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(scandia.epicenter_latitude,
                                        "epicenter latitude",
                                        -90.0,
                                        90.0,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(scandia.epicenter_longitude,
                                        "epicenter longitude",
                                        -180.0,
                                        180.0,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.origin_time_uncertainty,
                                        "origin time uncertainty",
                                        0,
                                        1,
                                        "ABCD ",
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.location_uncertainty,
                                        "location uncertainty",
                                        0,
                                        1,
                                        "ABCD ",
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateInteger(scandia.focal_depth,
                                        "focal depth",
                                        0,
                                        99,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.depth_identification_code,
                                        "depth identification code",
                                        0,
                                        1,
                                        "m?Habc ",
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(scandia.magnitude_1,
                                        "magnitude 1",
                                        0.0,
                                        99.9,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.magnitude_scale_1,
                                        "magnitude scale 1",
                                        0,
                                        2,
                                        ["M", "I", "R", "L", "LB", "LW", 
                                        "LN", "LU", "LH", "LA", "LF", ""],
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(scandia.magnitude_2,
                                        "magnitude 2",
                                        0.0,
                                        99.9,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.magnitude_scale_2,
                                        "magnitude scale 2",
                                        0,
                                        2,
                                        ["M", "I", "R", "L", "LB", "LW", 
                                        "LN", "LU", "LH", "LA", "LF", ""],
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(scandia.magnitude_3,
                                        "magnitude 3",
                                        0.0,
                                        99.9,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.magnitude_scale_3,
                                        "magnitude scale 3",
                                        0,
                                        2,
                                        magnitude_scale.keys,
                                        True,
                                        mheader):
        validation = False
    
    if not validationTools.validateString(scandia.maximum_intensity,
                                        "maximum intensity",
                                        0,
                                        4,
                                        None,
                                        False,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.macroseismic_observation_flag,
                                        "macroseismic observation flag",
                                        0,
                                        1,
                                        "*?o ",
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.macroseismic_reference,
                                        "macroseismic reference",
                                        0,
                                        3,
                                        macroseismic_reference.keys,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateInteger(scandia.mean_radius_of_area_percetibility,
                                        "mean radius of area percebility",
                                        0,
                                        999,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.region_code,
                                        "region code",
                                        1,
                                        1,
                                        region_code.keys,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateInteger(scandia.number_of_stations_used,
                                        "number of stations used",
                                        0,
                                        999,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.max_azimuth_gap,
                                        "max azimuth gap",
                                        0,
                                        3,
                                        None,
                                        False,
                                        mheader):
        validation = False

    if not validationTools.validateString(scandia.min_epicenter_to_station_distance,
                                        "min epicenter to station distance",
                                        0,
                                        3,
                                        None,
                                        False,
                                        mheader):
        validation = False

    return validation   
