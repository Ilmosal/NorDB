import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values
from nordb.core.nordic import NordicWaveform

def validateWaveformHeader(header):
    """
    Function for validating that the waveform header line is in correct format.

    Args:
        header(NordicWaveform): nordic waveform header to be validated

    Returns:
        True if the file is valid, false if not
    """
    validation = True
    mheader = 6

    if not validationTools.validateString(header.header[NordicWaveform.WAVEFORM_INFO],
                                    "waveform string",
                                    0,
                                    78,
                                    "",
                                    False,
                                    mheader):
        validation = False
    
    return validation   
