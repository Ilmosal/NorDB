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
    Function that determines and returns a string as integer or None if the given value is valid integer and falls between given parameters or is empty. 
    
    :param str val: value to be validated
    :param str valueName: name of the parameter for messaging purposes
    :param int low: lower limit of the val
    :param int high: upper limit of the val
    :param bool limits: bool for if the function needs to compare val against low and high
    :param int ntype: header name id. Used for messaging purposes
    :returns: correct value as a integer or None if it's empty
    """ 
    
    if val == "" or val is None:
        return None
    value = -9

    if type(val) is str:
        try:
            value = int(val)
        except:     
            msg = "Validation Error - {0}: {1} is not an integer! ({2})"
            raise Exception(msg.format(nTypes[nType], valueName, val))
    elif type(val) is not int:
        msg = "Validation Error - {0}: {1} is of wrong type! ({2})"
        raise Exception(msg.format(nTypes[nType], valueName, type(val)))
    else:
        value = val


    if limits and value < low:
        msg = "Validation Error - {0}: {1} is smaller than {2}! ({3})"
        raise Exception(msg.format(nTypes[nType], valueName, low, val))

    if limits and value > high:
        msg = "Validation Error - {0}: {1} is larger than {2}! ({3})"
        raise Exception(msg.format(nTypes[nType], valueName, high, val))

    return value

def validateFloat(val, valueName, low, high, limits, nType):
    """
    Function that determines and returns string as float if the given value is valid float, falls between given parameters and is not nAn or inf.
    
    :param str val: value to be validated
    :param str valueName: name of the parameter for messaging purposes
    :param float low: lower limit of the val
    :param float high: upper limit of the val
    :param bool limits: bool for if the function needs to compare val against low and high
    :param int ntype: header name id. Used for messaging purposes
    :returns: correct value as a float or None if it's empty
    """
    if val == "" or val is None:
        return None

    value = -9.9

    if type(val) is str:
        try:
            value = float(val)
        except:     
            msg = "Validation Error - {0}: {1} is not an float! ({2})"
            raise Exception(msg.format(nTypes[nType], valueName, val))
    elif type(val) is not float:
        msg = "Validation Error - {0}: {1} is of wrong type! ({2})"
        raise Exception(msg.format(nTypes[nType], valueName, type(val)))
    else:
        value = val

    if math.isnan(value):
        msg = "Validation Error - {0}: {1} is {2} which is not allowed!"
        raise Exception(msg.format(nTypes[nType], valueName, val))

    if math.isinf(value):
        msg = "Validation Error - {0}: {1} is {2} which is not allowed!"
        raise Exception(msg.format(nTypes[nType], valueName, val))

    if value < low and limits:
        msg = "Validation Error - {0}: {1} is smaller than {2}! ({3})"
        raise Exception(msg.format(nTypes[nType], valueName, low, val))

    if value > high and limits:
        msg = "Validation Error - {0}: {1} is larger than {2}! ({3})"
        raise Exception(msg.format(nTypes[nType], valueName, high, val))

    return value

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
    :returns: the same string or None if it's empty
    """

    if string is "" or string is None:
        return None
    if type(string) is not str:
        msg = "Validation Error - {0}: {1} is of wrong type! ({2})"
        raise Exception(msg.format(nTypes[nType], stringName, type(string)))

    if isList and string not in listOfAllowed:
        msg = "Validation Error - {0}: {1} not in the list of allowed strings! ({2})\nAllowed:\n"
        for allowed in listOfAllowed:
            msg += "  -" + allowed + "\n"
        raise Exception(msg.format(nTypes[nType], stringName, string))
    
    if minlen >= -1  and len(string) < minlen:
        msg = "Validation Error - {0}: {1} is shorter than the minimum allowed length {2}! ({3})"
        raise Exception(msg.format(nTypes[nType], stringName, minlen, string))
    if minlen >= -1  and len(string) > maxlen:
        msg = "Validation Error - {0}: {1} is longer than the maximum allowed length {2}! ({3})"
        raise Exception(msg.format(nTypes[nType], stringName, maxlen, string))

    return string

def validateDate(dateS, dateName, nType):
    """
    Function that determines if dateS is a valid date or empty.
    
    :param str dateS: value to be validated
    :param str dateName: name of the parameter for messaging purposes
    :param int ntype: header name id. Used for messaging purposes
    :returns: correct value as a date or None if it's empty
    """
    if dateS == "" or dateS == None:
        return None
    if type(dateS) is date:
        return dateS

    try:
        new_date = date(year=int(dateS[:4].strip()), month=int(dateS[5:7].strip()), day=int(dateS[8:].strip()))
    except:
        msg = "Validation Error - {0}: {1} is not parsable into date!({2})"
        raise Exception(msg.format(nTypes[nType], dateName, dateS))

    return new_date
