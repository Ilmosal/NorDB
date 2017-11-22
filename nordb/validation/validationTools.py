import math
import logging
from datetime import date
from nordb.core.nordic import NordicMain

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

    Args:
        str_id(str): id in a strin format

    Returns:
        True depending on if str_id validates 
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
    
    Args:
        val (str): value to be validated
        valueName (str): name of the parameter for messaging purposes
        low (int): lower limit of the val
        high (int): upper limit of the val
        limits (bool): bool for if the function needs to compare val against low and high
        ntype (int): header name id. Used for messaging purposes
    Returns:
        true or False depending on if the val validates
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
    
    Args:
        val (str): value to be validated
        valueName (str): name of the parameter for messaging purposes
        low (float): lower limit of the val
        high (float): upper limit of the val
        limits (bool): bool for if the function needs to compare val against low and high
        ntype (int): header name id. Used for messaging purposes
    Returns:
        true or False depending on if the val validates
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
    
    Args:
        string (str): value to be validated
        stringName (str): name of the parameter for messaging purposes
        minlen (int): lower limit of the string length
        maxlen (int): upper limit of the string length
        listOfAllowed (list): list of valid string from where the string needs to be found
        isList (bool): boolean value for determining if there is a list to which the string needs to be compared
        ntype (int): header name id. Used for messaging purposes
   
    Returns:
        true or False depending on if the string validates
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
    
    Args:
        dateS (str): value to be validated
        dateName (str): name of the parameter for messaging purposes
        ntype (int): header name id. Used for messaging purposes
   
    Returns:
        true or False depending on if the dateS validates
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
    Functoin for fixing a broken date string to a correct format in a NordicMain Object

    Args:
        nordic_main(NordicMain): nordic main object
    """
    if nordic_main.header[NordicMain.DATE][5] == " ":
        nordic_main.header[NordicMain.DATE] = nordic_main.header[NordicMain.DATE][:5] + "0" + nordic_main.header[NordicMain.DATE][6:]
    if nordic_main.header[NordicMain.DATE][8] == " ":
        nordic_main.header[NordicMain.DATE] = nordic_main.header[NordicMain.DATE][:8] + "0" + nordic_main.header[NordicMain.DATE][9:]

