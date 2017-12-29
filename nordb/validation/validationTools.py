"""
Module containing all the tools for validation.

Functions and Classes
---------------------
"""

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
        9: "Scandic Header",
        10: "Station Data",
        11: "Sitechan Data",
        12: "Instrument Data",
        13: "Sensor Data"}

class values():
    maxInt = 9223372036854775807 

def validateId(str_id):
    """
    Function for validating a id in a string format. Id must be a whole number.

    :param str str_id: id in a strin format
    :returns: true depending on if str_id validates 
    """
    try:
        if int(str_id) < 0:
            return False
        else:
            return True
    except:
        return False

def validateInteger(val, valueName, low, high, limits, nType):
    """
    Function that determines if val is valid integer and falls between given parameters.
    
    :param str val: value to be validated
    :param str valueName: name of the parameter for messaging purposes
    :param int low: lower limit of the val
    :param int high: upper limit of the val
    :param bool limits: bool for if the function needs to compare val against low and high
    :param int ntype: header name id. Used for messaging purposes
    :returns: true or false depending on if the val validates
    """ 
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
    """
    Function that determines if val is valid float, falls between given parameters and is not nAn or inf.
    
    :param str val: value to be validated
    :param str valueName: name of the parameter for messaging purposes
    :param float low: lower limit of the val
    :param float high: upper limit of the val
    :param bool limits: bool for if the function needs to compare val against low and high
    :param int ntype: header name id. Used for messaging purposes
    :returns: true or false depending on if the val validates
    """
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
    """
    Function that determines if val is empty, falls between given parameters or can be found from a given list.
    
    :param str string: value to be validated
    :param str stringName: name of the parameter for messaging purposes
    :param int minlen: lower limit of the string length
    :param int maxlen: upper limit of the string length
    :param array listOfAllowed: list of valid string from where the string needs to be found
    :param bool isList: boolean value for determining if there is a list to which the string needs to be compared
    :param int ntype: header name id. Used for messaging purposes
    :returns: true or false depending on if the string validates
    """

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
    """
    Function that determines if dateS is a valid date or empty.
    
    :param str dateS: value to be validated
    :param str dateName: name of the parameter for messaging purposes
    :param int ntype: header name id. Used for messaging purposes
    :returns: true or false depending on if the dateS validates
    """
    if dateS == "":
        return True
    
    try:
        date(year=int(dateS[:4].strip()), month=int(dateS[5:7].strip()), day=int(dateS[8:].strip()))
    except:
        msg = "Validation Error - {0}: {1} is not parsable into date!({2})"
        logging.error(msg.format(nTypes[nType], dateName, dateS))
        return False

    return True


def fixDate(nordic_main):
    """
    Function for fixing a broken date string to a correct format in a NordicMain Object

    :param NordicMain nordic_main: nordic main object
    """
    if nordic_main.header[nordic_main.DATE][5] == " ":
        nordic_main.header[nordic_main.DATE] = nordic_main.header[nordic_main.DATE][:5] + "0" + nordic_main.header[nordic_main.DATE][6:]
    if nordic_main.header[nordic_main.DATE][8] == " ":
        nordic_main.header[nordic_main.DATE] = nordic_main.header[nordic_main.DATE][:8] + "0" + nordic_main.header[nordic_main.DATE][9:]

