import math
import logging
from datetime import date

nTypes = {0: "Nordic Event",
        1: "Nordic Main Header",
        2: "Nordic Macroseismic Header",
        3: "Nordic Comment Header",
        5: "Nordic Error Header",
        6: "Nordic Waveform Header",
        8: "Nordic Phase Data",
        9: "Scandic Header"}

class values():
    maxInt = 9223372036854775807 

def validateInteger(val, valueName, low, high, limits, nType):
    if val == "":
        return True

    try:
        int(val)
    except:     
        msg = "Validation Error - {0}: {1} is not an integer! ({2})"
        logging.error(msg.format(nTypes[nType], valueName, val))
        return False

    if int(val) < low and limits:
        msg = "Validation Error - {0}: {1} is smaller than {2}! ({3})"
        logging.error(msg.format(nTypes[nType], valueName, low, val))
        return False

    if int(val) > high and limits:
        msg = "Validation Error - {0}: {1} is larger than {2}! ({3})"
        logging.error(msg.format(nTypes[nType], valueName, high, val))
        return False

    return True

def validateFloat(val, valueName, low, high, limits, nType):
    if val == "":
        return True

    try:
        float(val)
    except:     
        msg = "Validation Error - {0}: {1} is not an float! ({2})"
        logging.error(msg.format(nTypes[nType], valueName, val))
        return False

    if math.isnan(float(val)):
        msg = "Validation Error - {0}: {1} is {2} which is not allowed!"
        logging.error(msg.format(nTypes[nType], valueName, val))
        return False

    if math.isinf(float(val)):
        msg = "Validation Error - {0}: {1} is {2} which is not allowed!"
        logging.error(msg.format(nTypes[nType], valueName, val))
        return False

    if float(val) < low and limits:
        msg = "Validation Error - {0}: {1} is smaller than {2}! ({3})"
        logging.error(msg.format(nTypes[nType], valueName, low, val))
        return False

    if float(val) > high and limits:
        msg = "Validation Error - {0}: {1} is larger than {2}! ({3})"
        logging.error(msg.format(nTypes[nType], valueName, high, val))
        return False

    return True

def validateString(string, stringName, minlen, maxlen, listOfAllowed, isList, nType):   
    if string is "":
        return True

    if isList and string not in listOfAllowed:
        msg = "Validation Error - {0}: {1} not in the list of allowed strings! ({2})\nAllowed:\n"
        for allowed in listOfAllowed:
            msg += "  -" + allowed + "\n"
        logging.error(msg.format(nTypes[nType], stringName, string))
        return False

    if minlen > -1  and len(string) < minlen:
        msg = "Validation Error - {0}: {1} is shorter than the minimum allowed length {2}! ({3})"
        logging.error(msg.format(nTypes[nType], stringName, minlen, string))
        return False

    if minlen > -1  and len(string) > maxlen:
        msg = "Validation Error - {0}: {1} is longer than the maximum allowed length {2}! ({3})"
        logging.error(msg.format(nTypes[nType], stringName, maxlen, string))
        return False

    return True

def validateDate(dateS, dateName, nType):
    if dateS == "":
        return True
    
    try:
        date(year=int(dateS[:4].strip()), month=int(dateS[5:7].strip()), day=int(dateS[8:].strip()))
    except:
        msg = "Validation Error - {0}: {1} is not parsable into date!({2})"
        logging.error(msg.format(nTypes[nType], dateName, dateS))
        return False

    return True


def fixDate(nordic):
    if nordic.date[5] == " ":
        nordic.date = nordic.date[:5] + "0" + nordic.date[6:]
    if nordic.date[8] == " ":
        nordic.date = nordic.date[:8] + "0" + nordic.date[9:]

