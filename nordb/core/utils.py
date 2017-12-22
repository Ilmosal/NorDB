"""
Module that contains helpper functions for all over the program

Functions and Classes
---------------------
"""

def addString2String(value, val_len, front):
    """
    Function for parsing a string into correct format. Front works as the parser character which tells how the string has to be formatted.
    
    Examples::

        >> add_string_to_string("test", 6, '<')
            "test  "
    
    :param str value: string value that will be formatted
    :param int val_len: int on how long the string needs to be
    :param str front: formatting character
    :return: formatted string
    """
    string = ""
    parser = "{:" + front + str(val_len) + "s}"
    if value is not None:
        string += parser.format(value)
    else:
        string = val_len * " "

    return string

def addInteger2String(value, val_len, front):
    """
    Function for parsing a integer into a correct string format. Front works as the parser character which tells the program how the string has to be formatted.

    Examples::
        
        >> addInteger2String(3, 5, 0)
            "00003"

    :param int value: integer that will be formatted
    :param int val_len: int on how long the string needs to be
    :param str front: formatting character
    :return: formatted string
    """
    string = ""
    parser = "{:" + front + str(val_len) + "d}"
    if value is not None:
        string += parser.format(value)
    else:
        string = val_len * " "

    return string

def addFloat2String(value, val_len, decimal_len, front):
    """
    Function for parsing a float into a correct string format. Front works as the parser character which tells the program how the string has to be formatted.

    Examples::
        
        >> addFloat2String(0.71, 6, 3, '>')
            " 0.710"

    :param float value: integer that will be formatted
    :param int val_len: value that tells how long the string needs to be
    :param int decimal_len: value that tells how many of the letters will be allocated for the fraction
    :param str front: formatting character
    :return: formatted string
    """

    string = ""
    parser = "{:" + front + str(val_len) + "." + str(decimal_len)  + "f}"
    if value is not None:
        string += parser.format(value)
    else:
        string = val_len * " "
    if value is None:
        return string 
    if float(value) < 0 and val_len == len(string) - 1:
        string = string[0] + string[2:]
        
    return string

