"""
This module contains all the functions for fixing some common errors in nordic files before validating the Event. This happens when adding a nordic file into the database with "nordb insert" command using the --fix or -f flag. It wont fix everything, but it's still better than nothing.

Errors that get fixed
^^^^^^^^^^^^^^^^^^^^^
    - When the magnitude of the main header is nAn which is not a possible value in a postgres database
    - If the main headers second value is 60.0. This will be turned into a 00.0 and the time will be adjusted accordingly
    - When the magnitude error of the error header is nAn which is not a possible value in a postgres database
    - If the main headers second value is 60.0. This will be turned into a 00.0 and the time will be adjusted accordingly
    - Turns epicenter_distance into a integer if it's currently a float
    - Adds time_info sign to the nordic if there is need for it(The event has been observed the day after it has occurred)


Functions and Classes
---------------------
"""

import math
from nordb.core.nordic import NordicMain, NordicError, NordicData
def fixMainData(header):
    """
    Method for fixing some of the common errors in main header.
   
    :param NordicMain header: main header that needs to be fixed
    """
    try:
        if math.isnan(float(header.header[NordicMain.MAGNITUDE_1])):
            header.header[NordicMain.MAGNITUDE_1] = ""
    except ValueError:
        pass

    try:
        if math.isnan(float(header.header[NordicMain.MAGNITUDE_2])):
            header.header[NordicMain.MAGNITUDE_2] = ""
    except ValueError:
        pass

    try:
        if math.isnan(float(header.header[NordicMain.MAGNITUDE_3])):
            header.header[NordicMain.MAGNITUDE_3] = ""
    except ValueError:
        pass

    if header.header[NordicMain.SECOND] == "60.0":
        header.header[NordicMain.SECOND] = "0.0"
        header.header[NordicMain.MINUTE] = str(int(header.header[NordicMain.MINUTE]) + 1)
        if header.header[NordicMain.MINUTE] == "60":
            header.header[NordicMain.MINUTE] = "0"
            header.header[NordicMain.HOUR] = str(int(header.header[NordicMain.HOUR]) + 1)
            if header.header[NordicMain.HOUR] == "23":
                logging.error("Fix Nordic error - rounding error with second 60.0")


def fixErrorData(header):
    """
    Method for fixing some of the common errors in error header.
   
    :param NordicError header: error header that need to be fixed
    """
    try:
        if math.isnan(float(header.header[NordicError.MAGNITUDE_ERROR])):
            header.header[NordicError.MAGNITUDE_ERROR] = ""
    except ValueError:
        pass


def fixPhaseData(data, mhour):
    """
    Method for fixing some of the common errors in phase data.
   
    :param NordicData data: phase data that need to be fixed
    :param int mhour: The hour value of the main header
    """

    if data.data[NordicData.EPICENTER_TO_STATION_AZIMUTH] == "360":
        data.data[NordicData.EPICENTER_TO_STATION_AZIMUTH] = "0"

    if data.data[NordicData.BACK_AZIMUTH] == "360.0":
        data.data[NordicData.BACK_AZIMUTH] = "0.0"

    if data.data[NordicData.SECOND] == "60.00":
        data.data[NordicData.SECOND] = "0.00"
        if data.data[NordicData.MINUTE] == "60":
            data.data[NordicData.MINUTE] = 0
            if data.data[NordicData.HOUR] == "23":
                data.data[NordicData.HOUR] = "0"
                data.data[NordicData.TIME_INFO] = "+"
            else:
                data.data[NordicData.HOUR] = str(int(data.data[NordicData.HOUR]) + 1)
        else:
            data.data[NordicData.MINUTE] = str(int(data.data[NordicData.MINUTE]) + 1)

    try:
        data.data[NordicData.EPICENTER_DISTANCE] = str(int(float(data.data[NordicData.EPICENTER_DISTANCE])))
    except:
        pass

    try:
        if int(mhour) > int(data.data[NordicData.HOUR]):
            data.data[NordicData.TIME_INFO] = "+"
    except:
        pass

def fixNordicEvent(nordicEvent):
    """
    Method for fixing an whole nordic event before validation. Only fixes couple of common errors like rounding errors with angles or seconds and such.

    :param NordicEvent nordicEvent: Nordic Event Class object before validation.
    """
    
    for h in nordicEvent.headers[1]:
        fixMainData(h)

    for h in nordicEvent.headers[5]:
        fixErrorData(h)

    for data in nordicEvent.data:
        fixPhaseData(data, nordicEvent.headers[1][0].header[NordicMain.HOUR])
