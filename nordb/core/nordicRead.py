"""
NordicRead module contains a function readNordicFile that reads a single file and separates all nordicevents inside it to different string arrays.

Functions and Classes
---------------------
"""
import logging
import sys

def readNordicFile(f):
    """
    Method for reading a nordic file and parsing it to a string array while also checking the integrity of the file(Will give errors when lines are too long). It also wil parse empty space on the file if it is too short.

    :param file f: python file object for the Nordic File
    """
    nordics = []
    emsg = "Nordic Read: The following line is too short: {0}\n{1}"
    i = 0
    nordics.append([])

    for line in f:
        if line.strip() == "" or None:
            i += 1;
            nordics.append([])
        elif(len(line) < 81):
            logging.error(emsg.format(len(line), line))
            sys.exit()
        elif (line[79] == "7"):
            pass
        elif (line[79] == " "):
            nordics[i].append(line)
        else:
            nordics[i].append(line)

    return nordics
