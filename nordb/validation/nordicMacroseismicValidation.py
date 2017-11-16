import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values
from nordb.core.nordic import NordicMacroseismic
def validateMacroseismicHeader(header):
    """
    Function for validating that the macroseismic header line is in correct format.

    Args:
        header(NordicMacroseismic): nordic macroseismic header to be validated

    Returns:
        True if the file is valid, false if not
   
    """

    validation = True
    mheader = 2

    if not validationTools.validateString(header.header[NordicMacroseismic.DESCRIPTION],
                                            "description",
                                            0,
                                            15,
                                            "",
                                            False,
                                            mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMacroseismic.DIASTROPHISM_CODE],
                                            "diastrophism code",
                                            0,
                                            1,
                                            "FUD ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMacroseismic.TSUNAMI_CODE],
                                            "tsunami code",
                                            0,
                                            1,
                                            "TQ ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMacroseismic.SEICHE_CODE],
                                            "seiche code",
                                            0,
                                            1,
                                            "SQF ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMacroseismic.CULTURAL_EFFECTS],
                                            "cultural effects",
                                            0,
                                            1,
                                            "CDFH ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMacroseismic.UNUSUAL_EFFECTS],
                                            "unusual effects",
                                            0,
                                            1,
                                            "LGSBCVOM ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateInteger(header.header[NordicMacroseismic.MAXIMUM_OBSERVED_INTENSITY],
                                            "maximum observed intensity",
                                            0,
                                            20,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMacroseismic.MAXIMUM_INTENSITY_QUALIFIER],
                                            "maximum intensity qualifier",
                                            0,
                                            1,
                                            "+- ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMacroseismic.INTENSITY_SCALE],
                                            "intensity scale",
                                            0,
                                            2,
                                            {"MM", "RF", "CS", "SK"},
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMacroseismic.MACROSEISMIC_LATITUDE],
                                            "macroseismic latitude",
                                            -90.0,
                                            90.0,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMacroseismic.MACROSEISMIC_LONGITUDE],
                                            "macroseismic longitude",
                                            -180.0,
                                            180.0,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMacroseismic.MACROSEISMIC_MAGNITUDE],
                                            "macroseismic magnitude",
                                            0.0,
                                            20.0,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMacroseismic.TYPE_OF_MAGNITUDE],
                                            "type of magnitude",
                                            0,
                                            1,
                                            "IAR* ",
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMacroseismic.LOGARITHM_OF_RADIUS],
                                            "logarithm of radius",
                                            0.0,
                                            99.9,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMacroseismic.LOGARITHM_OF_AREA_1],
                                            "logarithm of area 1",
                                            0.0,
                                            99.99,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateInteger(header.header[NordicMacroseismic.BORDERING_INTENSITY_1],
                                            "bordering intensity 1",
                                            0,
                                            99,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicMacroseismic.LOGARITHM_OF_AREA_2],
                                            "logarithm of area 2",
                                            0.0,
                                            99.99,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateInteger(header.header[NordicMacroseismic.BORDERING_INTENSITY_2],
                                            "bordering intensity 2",
                                            0,
                                            99,
                                            True,
                                            mheader):
        validation = False

    if not validationTools.validateString(header.header[NordicMacroseismic.REPORTING_AGENCY],
                                            "reporting agency",
                                            3,
                                            3,
                                            None,
                                            False,
                                            mheader):
        validation = False

    return validation   
