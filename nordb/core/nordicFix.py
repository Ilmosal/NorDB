import math

def fixMainData(header):
    try:
        if math.isnan(float(header.magnitude_1)):
            header.magnitude_1 = ""
    except ValueError:
        pass

    try:
        if math.isnan(float(header.magnitude_2)):
            header.magnitude_2 = ""
    except ValueError:
        pass

    try:
        if math.isnan(float(header.magnitude_3)):
            header.magnitude_3 = ""
    except ValueError:
        pass

    if header.second == "60.0":
        header.second = "0.0"
        header.minute = str(int(header.minute) + 1)
        if header.minute == "60":
            header.minute = "0"
            header.hour = str(int(header.hour) + 1)
            if header.hour == "23":
                logging.error("Fix Nordic error - rounding error with second 60.0")


def fixErrorData(header):
    if header.gap.strip() == "t":
        header.gap = ""

    try:
        if math.isnan(float(header.magnitude_error)):
            header.magnitude_error = ""
    except ValueError:
        pass


def fixPhaseData(data):
    if data.epicenter_to_station_azimuth == "360":
        data.epicenter_to_station_azimuth = "0"

    if data.back_azimuth == "360.0":
        data.back_azimuth = "0.0"

    if data.second == "60.00":
        data.second = "0.00"
        if data.minute == "60":
            data.minute = 0
            if data.hour == "23":
                data.hour = "0"
                data.time_info = "+"
            else:
                data.hour = str(int(data.hour) + 1)
        else:
            data.minute = str(int(data.minute) + 1)

    try:
        data.epicenter_distance = str(int(float(data.epicenter_distance)))
    except:
        pass

    if data.travel_time_residual == "*****":
        data.travel_time_residual = ""

def fixNordicEvent(nordicEvent):
    for h in nordicEvent.headers:
        if h.tpe == 1:
            fixMainData(h)
        elif h.tpe == 5:
            fixErrorData(h)

    for data in nordicEvent.data:
        fixPhaseData(data)

    return True
