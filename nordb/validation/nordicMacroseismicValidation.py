"""
This module contains a function for validating a :class:`.NordicMacroseismic`.

Functions and Classes
---------------------
"""

import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values

def validateMacroseismicHeader(macro):
    """
    Function for validating that the macroseismic header line is in correct format.

    :param NordicMacroseismic macro: nordic macroseismic header to be validated
    :returns: true if the file is valid, false if not
   
    """

    validation = True
    mheader = 2

    if not validationTools.validateString(macro.header[macro.DESCRIPTION],
                                            "description",
                                            0,
                                            15,
                                            "",
                                            False,
                                            mheader):
        validation = False

    if not validationTools.validateString(macro.header[macro.DIASTROPHISM_CODE],
                                            "diastrophism code",
                                            0,
                                            1,
                                            "FUD ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(macro.header[macro.TSUNAMI_CODE],
                                            "tsunami code",
                                            0,
                                            1,
                                            "TQ ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(macro.header[macro.SEICHE_CODE],
                                            "seiche code",
                                            0,
                                            1,
                                            "SQF ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(macro.header[macro.CULTURAL_EFFECTS],
                                            "cultural effects",
                                            0,
                                            1,
                                            "CDFH ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(macro.header[macro.UNUSUAL_EFFECTS],
                                            "unusual effects",
                                            0,
                                            1,
                                            "LGSBCVOM ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateInteger(macro.header[macro.MAXIMUM_OBSERVED_INTENSITY],
                                            "maximum observed intensity",
                                            0,
                                            20,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(macro.header[macro.MAXIMUM_INTENSITY_QUALIFIER],
                                            "maximum intensity qualifier",
                                            0,
                                            1,
                                            "+- ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(macro.header[macro.INTENSITY_SCALE],
                                            "intensity scale",
                                            0,
                                            2,
                                            {"MM", "RF", "CS", "SK"},
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(macro.header[macro.MACROSEISMIC_LATITUDE],
                                            "macroseismic latitude",
                                            -90.0,
                                            90.0,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(macro.header[macro.MACROSEISMIC_LONGITUDE],
                                            "macroseismic longitude",
                                            -180.0,
                                            180.0,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(macro.header[macro.MACROSEISMIC_MAGNITUDE],
                                            "macroseismic magnitude",
                                            0.0,
                                            20.0,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(macro.header[macro.TYPE_OF_MAGNITUDE],
                                            "type of magnitude",
                                            0,
                                            1,
                                            "IAR* ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(macro.header[macro.LOGARITHM_OF_RADIUS],
                                            "logarithm of radius",
                                            0.0,
                                            99.9,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(macro.header[macro.LOGARITHM_OF_AREA_1],
                                            "logarithm of area 1",
                                            0.0,
                                            99.99,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateInteger(macro.header[macro.BORDERING_INTENSITY_1],
                                            "bordering intensity 1",
                                            0,
                                            99,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(macro.header[macro.LOGARITHM_OF_AREA_2],
                                            "logarithm of area 2",
                                            0.0,
                                            99.99,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateInteger(macro.header[macro.BORDERING_INTENSITY_2],
                                            "bordering intensity 2",
                                            0,
                                            99,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(macro.header[macro.REPORTING_AGENCY],
                                            "reporting agency",
                                            3,
                                            3,
                                            None,
                                            False,
                                            mheader):
        validation = False

    return validation   
