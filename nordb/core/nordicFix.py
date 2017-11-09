import math
from nordb.core.nordic import NordicMain, NordicError, NordicData
def fixMainData(header):
    """
    Method for fixing some of the common errors in main header.

    Args:
        header: main header that needs to be fixed
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
   
    Args:
        header: error header that need to be fixed
    """
    try:
        if math.isnan(float(header.header[NordicError.MAGNITUDE_ERROR])):
            header.header[NordicError.MAGNITUDE_ERROR] = ""
    except ValueError:
        pass


def fixPhaseData(data):
    """
    Method for fixing some of the common errors in phase data.
   
    Args:
        data: phase data that need to be fixed
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

def fixNordicEvent(nordicEvent):
    """
    Method for fixing an whole nordic event before validation. Only fixes couple of common errors like rounding errors with angles or seconds and such.

    Args:
        nordicEvent: Nordic Event Class object before validation.

    """
    
    for h in nordicEvent.headers[1]:
        fixMainData(h)

    for h in nordicEvent.headers[5]:
        fixErrorData(h)

    for data in nordicEvent.data:
        fixPhaseData(data)
