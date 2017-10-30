import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values
from nordb.core.nordic import NordicComment

def validateCommentHeader(header):
    validation = True
    mheader = 3

    if not validationTools.validateString(header[NordicComment.H_COMMENT],
                                    "comment",
                                    0,
                                    78,
                                    "",
                                    False,
                                    mheader):
        validation = False
 
    
    return validation   
