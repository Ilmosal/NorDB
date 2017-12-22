import os
import sys

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values

def validateCommentHeader(comment):
    """
    Function for validating that the comment header line is in correct format.

    Args:
        header(NordicComment): nordic comment header to be validated

    Returns:
        True if the file is valid, false if not
    """
    validation = True
    mheader = 3

    if not validationTools.validateString(comment.header[comment.H_COMMENT],
                                    "comment",
                                    0,
                                    78,
                                    "",
                                    False,
                                    mheader):
        validation = False
 
    
    return validation   
