import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values
from nordb.core.nordic import NordicWaveform

def validateWaveformHeader(header):
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
