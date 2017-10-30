import os
import sys

from nordb.validation import validationTools 
from nordb.validation.validationTools import values
from nordb.core import nordicStringClass
from nordb.core.nordic import NordicData

def validatePhaseData(phase_data):
    validation = True
    phname = 8

    if not validationTools.validateString(phase_data[NordicData.STATION_CODE],
                                                "station code",
                                                0,
                                                4,
                                                "",
                                                False,
                                                phname):    
        validation = False
    
    if not validationTools.validateString(phase_data[NordicData.SP_INSTRUMENT_TYPE],
                                                "instrument type",
                                                0,
                                                1,
                                                "LSBHE ",
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateString(phase_data[NordicData.SP_COMPONENT],
                                                "component",
                                                0,
                                                1,
                                                "ZNEH ",
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateString(phase_data[NordicData.QUALITY_INDICATOR],
                                                "quality indicator",
                                                0,
                                                1,
                                                "",
                                                False,
                                                phname):
        validation = False

    if not validationTools.validateString(phase_data[NordicData.PHASE_TYPE],
                                                "phase type",
                                                0,
                                                4,
                                                "",
                                                False,
                                                phname):
        validation = False

    if not validationTools.validateInteger(phase_data[NordicData.WEIGHT],
                                                "weight",
                                                0,
                                                9,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateString(phase_data[NordicData.FIRST_MOTION],
                                                "first motion",
                                                0,
                                                1,
                                                "CD+- ",
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateString(phase_data[NordicData.TIME_INFO],
                                                "time info",
                                                0,
                                                1,
                                                "-+ ",
                                                True,
                                                phname):
        validation = False
    
    if not validationTools.validateInteger(phase_data[NordicData.HOUR],
                                                "hour",
                                                0,
                                                23,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateInteger(phase_data[NordicData.MINUTE],
                                                "minute",
                                                0,
                                                59,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateFloat(phase_data[NordicData.SECOND],
                                                "second",
                                                0.0,
                                                59.99,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateInteger(phase_data[NordicData.SIGNAL_DURATION],
                                                "signal duration",
                                                0,
                                                9999,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateFloat(phase_data[NordicData.MAX_AMPLITUDE],
                                                "max amplitude",
                                                -1.0,
                                                9999.9,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateFloat(phase_data[NordicData.MAX_AMPLITUDE_PERIOD],
                                                "max amplitude period",
                                                -1.0,
                                                99.9,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateFloat(phase_data[NordicData.BACK_AZIMUTH],
                                                "back azimuth",
                                                0.0,
                                                359.9,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateFloat(phase_data[NordicData.APPARENT_VELOCITY],
                                                "apparent velocity",
                                                0.0,
                                                99.9,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateFloat(phase_data[NordicData.SIGNAL_TO_NOISE],
                                                "signal to noise",
                                                0.0,
                                                99.9,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateInteger(phase_data[NordicData.AZIMUTH_RESIDUAL],
                                                "azimuth residual",
                                                -99,
                                                999,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateFloat(phase_data[NordicData.TRAVEL_TIME_RESIDUAL],
                                                "travel time residual",
                                                -999.9,
                                                9999.9,
                                                True,
                                                phname):    
        validation = False

    if not validationTools.validateInteger(phase_data[NordicData.LOCATION_WEIGHT],
                                                "location weight",
                                                0,
                                                10,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateInteger(phase_data[NordicData.EPICENTER_DISTANCE],
                                                "epicenter distance",
                                                0,
                                                99999,
                                                True,
                                                phname):
        validation = False

    if not validationTools.validateInteger(phase_data[NordicData.EPICENTER_TO_STATION_AZIMUTH],
                                                "epicenter to station azimuth",
                                                0,
                                                359,
                                                True,
                                                phname):
        validation = False

    return validation
