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
from nordb.core.validationTools import validateDatetime
from nordb.core.validationTools import validateTime
from datetime import timedelta

def fixMainData(header):
    """
    Method for fixing some of the common errors in main header.

    :param NordicMain header: main header that needs to be fixed
    """
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

    if header[NordicMain.ORIGIN_TIME][-4:] == "60.0":
        temp = header[NordicMain.ORIGIN_TIME][:-4] + "00.0"

        time = validateDatetime(header[NordicMain.ORIGIN_DATE]+" "+temp, "", "")
        time += timedelta(seconds=60)
        new_time_string = time.strftime("%H%M %S")
        new_time_string += ".{0}".format(round(time.microsecond /100000))
        header[NordicMain.ORIGIN_TIME] = new_time_string

def fixErrorData(header):
    """
    Method for fixing some of the common errors in error header.

    :param NordicError header: error header that need to be fixed
    """
    try:
        if int(header[NordicError.GAP]) == 360:
            header[NordicError.GAP] == 359
    except ValueError:
        pass
    try:
        if math.isnan(float(header[NordicError.MAGNITUDE_ERROR])):
            header[NordicError.MAGNITUDE_ERROR] = ""
    except ValueError:
        pass


def fixPhaseData(data, main_datetime):
    """
    Method for fixing some of the common errors in phase data.

    :param NordicData data: phase data that need to be fixed
    :param main_datetime datetime: datetime of the first main header
    """
    if data[NordicData.EPICENTER_TO_STATION_AZIMUTH] == "360":
        data[NordicData.EPICENTER_TO_STATION_AZIMUTH] = "0"

    if data[NordicData.BACK_AZIMUTH] == "360.0":
        data[NordicData.BACK_AZIMUTH] = "0.0"

    if data[NordicData.OBSERVATION_TIME][-5:] == "60.00":
        temp = data[NordicData.OBSERVATION_TIME][:-5] + "00.00"
        time = validateDatetime(temp)
        time += timedelta(seconds=60)
        new_time_string = time.strftime("%Y %m%d %H%M %S") 
        new_time_string += ".{0}".format(round(time.microsecond /10000))
        data[NordicData.OBSERVATION_TIME] = new_time_string

    if int(data[NordicData.OBSERVATION_TIME][10:12]) < main_datetime.hour:
        time = validateDatetime(data[NordicData.OBSERVATION_TIME])
        time += timedelta(days=1)
        new_time_string = time.strftime("%Y %m%d %H%M %S") 
        new_time_string += ".{0}".format(round(time.microsecond /10000))
        data[NordicData.OBSERVATION_TIME] = new_time_string


    try:
        data[NordicData.EPICENTER_DISTANCE] = str(int(float(data[NordicData.EPICENTER_DISTANCE])))
    except:
        pass

    try:
        if main_datetime.hour > int(data[NordicData.HOUR]):
            data[NordicData.TIME_INFO] = "+"
    except:
        pass

