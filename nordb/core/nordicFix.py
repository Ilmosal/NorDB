"""
This module contains all the functions for fixing some common errors in nordic files before validating the Event. This happens when adding a nordic file into the database with "nordb insert" command using the --fix or -f flag. It wont fix everything, but it's still better than nothing.

Errors that get fixed
^^^^^^^^^^^^^^^^^^^^^
    - When the magnitude of the main header is nAn which is not a possible value in a postgres database, the value will be set to None
    - If the 'second' value of the main header is 60.0, it will be turned into 00.00 and the minutes and hours will be adjusted accordingly
    - When the magnitude error of the error header is nAn which is not a possible value in a postgres database, the value will be set to none
    - If the 'second' value of the data header is 60.0, it will be turned into 00.00 and time info sign will be corrected if necessary
    - If the epicenter_distance is a float, it will be turned into a integer
    - Time_info sign will be added to to the nordic data header if there is need for it
    - Zeros are put into singular dates and months in case they are missing. 

Functions and Classes
---------------------
"""

import math

from nordb.nordic.nordicMain import NordicMain
from nordb.nordic.nordicError import NordicError
from nordb.nordic.nordicData import NordicData

def fixMainData(header):
    """
    Method for fixing some of the common errors in main header.
   
    :param NordicMain header: main header that needs to be fixed
    """
    if header[NordicMain.DATE][5] == " ":
        header[NordicMain.DATE] = header[NordicMain.DATE][:5] + "0" + header[NordicMain.DATE][6:]
    if header[NordicMain.DATE][8] == " ":
        header[NordicMain.DATE] = header[NordicMain.DATE][:8] + "0" + header[NordicMain.DATE][9:]

    try:
        if math.isnan(float(header[NordicMain.MAGNITUDE_1])):
            header[NordicMain.MAGNITUDE_1] = ""
    except ValueError:
        pass

    try:
        if math.isnan(float(header[NordicMain.MAGNITUDE_2])):
            header[NordicMain.MAGNITUDE_2] = ""
    except ValueError:
        pass

    try:
        if math.isnan(float(header[NordicMain.MAGNITUDE_3])):
            header[NordicMain.MAGNITUDE_3] = ""
    except ValueError:
        pass

    if header[NordicMain.SECOND] == "60.0":
        header[NordicMain.SECOND] = "0.0"
        header[NordicMain.MINUTE] = str(int(header[NordicMain.MINUTE]) + 1)
        if header[NordicMain.MINUTE] == "60":
            header[NordicMain.MINUTE] = "0"
            header[NordicMain.HOUR] = str(int(header[NordicMain.HOUR]) + 1)
            if header[NordicMain.HOUR] == "23":
                raise ValueError #TODO OWN ERROR

def fixErrorData(header):
    """
    Method for fixing some of the common errors in error header.
   
    :param NordicError header: error header that need to be fixed
    """
    try:
        if math.isnan(float(header[NordicError.MAGNITUDE_ERROR])):
            header[NordicError.MAGNITUDE_ERROR] = ""
    except ValueError:
        pass


def fixPhaseData(data, mhour):
    """
    Method for fixing some of the common errors in phase data.
   
    :param NordicData data: phase data that need to be fixed
    :param int mhour: The hour value of the main header
    """
    if data[NordicData.EPICENTER_TO_STATION_AZIMUTH] == "360":
        data[NordicData.EPICENTER_TO_STATION_AZIMUTH] = "0"

    if data[NordicData.BACK_AZIMUTH] == "360.0":
        data[NordicData.BACK_AZIMUTH] = "0.0"

    if data[NordicData.SECOND] == "60.00":
        data[NordicData.SECOND] = "0.00"
        if data[NordicData.MINUTE] == "60":
            data[NordicData.MINUTE] = 0
            if data[NordicData.HOUR] == "23":
                data[NordicData.HOUR] = "0"
                data[NordicData.TIME_INFO] = "+"
            else:
                data[NordicData.HOUR] = str(int(data[NordicData.HOUR]) + 1)
        else:
            data[NordicData.MINUTE] = str(int(data[NordicData.MINUTE]) + 1)

    try:
        data[NordicData.EPICENTER_DISTANCE] = str(int(float(data[NordicData.EPICENTER_DISTANCE])))
    except:
        pass

    try:
        if int(mhour) > int(data[NordicData.HOUR]):
            data[NordicData.TIME_INFO] = "+"
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
        fixPhaseData(data, nordicEvent.headers[1][0].hour)

