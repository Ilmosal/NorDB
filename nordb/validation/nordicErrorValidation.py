"""
This module contains a function for validating a :class:`.NordicError`.

Functions and Classes
---------------------
"""

import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values

def validateErrorHeader(error):
    """
    Function for validating that the error header line is in correct format.

    :param NordicError header: nordic error header to be validated
    :returns: true if the file is valid, false if not
    """
    validation = True
    mheader = 5
    
    if error.header[error.GAP].strip() != "t":
        if not validationTools.validateInteger(error.header[error.GAP],
                                                "gap",
                                                0,
                                                359,
                                                True,
                                                mheader):
            validation = False
    
    if not validationTools.validateFloat(error.header[error.SECOND_ERROR],   
                                        "second error",
                                        0.0,
                                        99.9,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(error.header[error.EPICENTER_LATITUDE_ERROR],
                                        "epicenter latitude error",
                                        0.0,
                                        99.99,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(error.header[error.EPICENTER_LONGITUDE_ERROR],
                                        "epicenter longitude error",
                                        0.0,
                                        99.99,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(error.header[error.DEPTH_ERROR],
                                        "depth error",
                                        0.0,
                                        999.9,
                                        True,
                                        mheader):
        validation = False
    
    if not validationTools.validateFloat(error.header[error.MAGNITUDE_ERROR],
                                        "magnitude error",
                                        0.0,
                                        9.9,
                                        True,
                                        mheader):
        validation = False

    return validation   
