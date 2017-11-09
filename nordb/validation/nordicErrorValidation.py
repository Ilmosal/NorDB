import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values
from nordb.core.nordic import NordicError
def validateErrorHeader(header):
    validation = True
    mheader = 5
    
    if header.header[NordicError.GAP].strip() != "t":
        if not validationTools.validateInteger(header.header[NordicError.GAP],
                                                "gap",
                                                0,
                                                359,
                                                True,
                                                mheader):
            validation = False
    
    if not validationTools.validateFloat(header.header[NordicError.SECOND_ERROR],   
                                        "second error",
                                        0.0,
                                        99.9,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicError.EPICENTER_LATITUDE_ERROR],
                                        "epicenter latitude error",
                                        0.0,
                                        99.99,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicError.EPICENTER_LONGITUDE_ERROR],
                                        "epicenter longitude error",
                                        0.0,
                                        99.99,
                                        True,
                                        mheader):
        validation = False

    if not validationTools.validateFloat(header.header[NordicError.DEPTH_ERROR],
                                        "depth error",
                                        0.0,
                                        999.9,
                                        True,
                                        mheader):
        validation = False
    
    if not validationTools.validateFloat(header.header[NordicError.MAGNITUDE_ERROR],
                                        "magnitude error",
                                        0.0,
                                        9.9,
                                        True,
                                        mheader):
        validation = False

    return validation   
