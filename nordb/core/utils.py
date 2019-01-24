"""
Module that contains helpper functions for all over the program

Functions and Classes
---------------------
"""

from datetime import date
from datetime import timedelta

MONTH_CONV = {
                "Jan": "01",
                "Feb": "02",
                "Mar": "03",
                "Apr": "04",
                "May": "05",
                "Jun": "06",
                "Jul": "07",
                "Aug": "08",
                "Sep": "09",
                "Oct": "10",
                "Nov": "11",
                "Dec": "12"
            }

def stringToDate(sDate):
    """
    Function for converting a date in string format "YYYYDDD" or "YYYY-MMM-DD" to "YYYY-MM-DD".

    :param str sDate: date string
    :returns: the date in correct format as a string
    """
    if len(sDate) == 7:
        ndate = date(day=1, month=1, year=int(sDate[:4]))
        ndate += timedelta(days= int(sDate[4:]) - 1)
        rdate = ndate.strftime("%Y-%m-%d")
    elif len(sDate) == 11:
        rdate = sDate[:4] + "-" + MONTH_CONV[sDate[5:8]] + "-" + sDate[9:]
    elif sDate == "-1":
        rdate = ""
    else:
        rdate = ""

    return rdate

def xstr(s):
    """
    Function for casting a value to string and None to a empty string

    :param s: Value to be converted
    :return: a string value
    """
    if s is None:
        return ""
    else:
        return str(s)

def addString2String(value, val_len, front):
    """
    Function for parsing a string into correct format. Front works as the parser character which tells how the string has to be formatted. Only formatters you can give for the function are '<' and '>'.
    
    **Examples**::

        >> add_string_to_string("test", 6, '<')
            "test  "
    
    :param str value: string value that will be formatted
    :param int val_len: int on how long the string needs to be
    :param str front: formatting character
    :return: formatted string
    :raises: ValueError
    """
    if value is None:
        return val_len * " "

    string = ""
    parser = "{:" + front + str(val_len) + "s}"

    if len(value) > val_len:
        raise ValueError
    
    string += parser.format(value)

    return string

def addInteger2String(value, val_len, front):
    """
    Function for parsing a integer into a correct string format. Front works as the parser character which tells the program how the string has to be formatted.

    **Examples**::

        >> addInteger2String(3, 5, 0)
            "00003"

    :param int value: integer that will be formatted
    :param int val_len: int on how long the string needs to be
    :param str front: formatting character
    :return: formatted string
    :raises: ValueError
    """

    if value is None:
        return val_len * " "

    string = ""

    if len(str(value)) > val_len:
        raise ValueError

    parser = "{:" + front + str(val_len) + "d}"
    string += parser.format(value)

    return string

def addFloat2String(value, val_len, decimal_len, front):
    """
    Function for parsing a float into a correct string format. Front works as the parser character which tells the program how the string has to be formatted.

    **Examples**::

        >> addFloat2String(0.71, 6, 3, '>')
            " 0.710"

    :param float value: integer that will be formatted
    :param int val_len: value that tells how long the string needs to be
    :param int decimal_len: value that tells how many of the letters will be allocated for the fraction
    :param str front: formatting character
    :return: formatted string
    """
    if value is None:
        return val_len * " "

    if len(str(value)) > val_len:
        value = float(("{:."+ str(decimal_len) +"f}").format(value))
        if value < 1.0 and value > -1.0 and val_len == len(str(value)) - 1:
            pass
        elif len(str(value)) > val_len:
            raise ValueError

    string = ""
    parser = "{:" + front + str(val_len) + "." + str(decimal_len)  + "f}"

    string += parser.format(value)

    if float(value) < 0 and val_len == len(string) - 1:
        string = string[0] + string[2:]

    return string

