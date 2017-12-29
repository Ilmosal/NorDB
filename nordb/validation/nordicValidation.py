"""
This module contains a function for validating a whole :class:`.NordicEvent`.

Functions and Classes
---------------------
"""

import sys
import os
import logging

MODULE_PATH = os.path.realpath(__file__)[:-len("nordicValidation.py")]

if __name__=="__main__":
    os.chdir("../..")

from nordb.validation import nordicMainValidation
from nordb.validation import nordicMacroseismicValidation
from nordb.validation import nordicErrorValidation
from nordb.validation import nordicCommentValidation
from nordb.validation import nordicWaveformValidation
from nordb.validation import nordicPhaseDataValidation

from nordb.validation import scandiaValidation

eventTypeValues = {"O":1, "A":2, "P":3, "R":4, "F":5, "S":6}
def validateNordic(nordic_event):
    """
    Function for validating a whole nordic event.

    :param NordicEvent noridc_event: nordic event to be validated
    :returns: True or False depending on if the file is valid or not
    """
    validation_error = False

    for header in nordic_event.headers[1]:
            if not nordicMainValidation.validateMainHeader(header):
                validation_error = True
    for header in nordic_event.headers[2]:
            if not nordicMacroseismicValidation.validateMacroseismicHeader(header):
                validation_error = True
    for header in nordic_event.headers[3]:
            if not nordicCommentValidation.validateCommentHeader(header):
                validation_error = True
    for header in nordic_event.headers[5]:
            if not nordicErrorValidation.validateErrorHeader(header):
                validation_error = True
    for header in nordic_event.headers[6]:
            if not nordicWaveformValidation.validateWaveformHeader(header):
                validation_error = True

    for phase_data in nordic_event.data:
        if not nordicPhaseDataValidation.validatePhaseData(phase_data):
            validation_error = True

    return not validation_error
