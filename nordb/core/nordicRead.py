"""
NordicRead module contains a function readNordicFile that reads a single file and separates all separate events inside it to different string arrays.

Functions and Classes
---------------------
"""
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
        if line.strip() == "" or line is None:
            if len(nordics[i]) == 0:
                continue
            i += 1;
            nordics.append([])
        elif(len(line) < 81):
            raise Exception("Line not long enough (len:{0}):\n{1}".format(len(line), line))
        elif (line[79] == "7"):
            continue 
        else:
            nordics[i].append(line)

    if not nordics[-1]:
        return nordics[:-1]
    else:
        return nordics
