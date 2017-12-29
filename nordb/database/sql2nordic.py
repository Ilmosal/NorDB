"""
This module contains functions for getting nordic events out from the database. The most important function here is writeNordicEvent().

Functions and Classes
---------------------
"""

import logging
import os
import sys
import psycopg2

MODULE_PATH = os.path.realpath(__file__)[:-len("sql2nordic.py")]

username = ""

from nordb.core.nordic import NordicMain, NordicMacroseismic, NordicComment
from nordb.core.nordic import NordicError, NordicWaveform, NordicData
from nordb.core import usernameUtilities
from nordb.database import getNordic

def nordicEventToNordic(nordic):
    """
    Method that converts a nordic event object to a nordic file string

    :param NordicEvent nordic: event to be converted into a string
    :read: nordic file as a string array
    """
    nordic_string = []

    nordic_string.append(str(nordic.headers[1][0])+"\n")

    if len(nordic.headers[5]) > 0:
        nordic_string.append(str(nordic.headers[5][0]) + "\n")

    if len(nordic.headers[6]) > 0:
        nordic_string.append(str(nordic.headers[6][0]) + "\n")

    for hd in nordic.headers[3]:
        nordic_string.append(str(hd) + "\n")

    for i in range(1,len(nordic.headers[1])):
        nordic_string.append(str(nordic.headers[1][i]) + "\n")
        for h_error in nordic.headers[5]:
            if h_error.header[NordicError.HEADER_ID] == nordic.headers[1][i].header[NordicMain.ID]:
                nordic_string.append(str(h_error) + "\n")

    nordic_string.append(create_help_header_string())

    for pd in nordic.data:
        nordic_string.append(str(pd) + "\n")      

    nordic_string.append("\n")

    return nordic_string

def create_help_header_string():
    """
    Function that returns the help header of type 7 as a string. 
    
    Header::
        
        " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\\n"

    :return: The help header as a string
    """
    h_string = " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n"
    return h_string

def writeNordicEvent(nordicEventId, usr_path, output):
    """
    Function that writes a :class:`.NordicEvent` to a file

    :param int nordicEventId: id of the event that is wanted
    :param str usr_path: path to user
    :param str output: name of the file. If None given, program will name the file according to it's timestamp
    :returns: True or False depending on if the operation was successful
    """
    username = usernameUtilities.readUsername()

    try:
        int(nordicEventId)
    except:
        logging.error("Argument {0} is not a valid event id!".format(nordicEventId))
        return False

    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid")
        return

    cur = conn.cursor()

    nordic = getNordic.readNordicEvent(cur, nordicEventId)
   
    if nordic == None:
        return False
    
    nordicString = nordicEventToNordic(nordic)

    if output is None:

        filename = "{:d}{:03d}{:02d}{:02d}{:02d}".format(
                        nordic.headers[1][0].header[NordicMain.DATE].year, 
                        nordic.headers[1][0].header[NordicMain.DATE].timetuple().tm_yday, 
                        nordic.headers[1][0].header[NordicMain.HOUR], 
                        nordic.headers[1][0].header[NordicMain.MINUTE], 
                        int(nordic.headers[1][0].header[NordicMain.SECOND])) + ".nordic"
        
        print(filename + " has been created!")
    
        f = open(usr_path + '/' + filename, 'w')
        
        for line in nordicString:   
            f.write(line)

        f.close()
    else:
        f = open(usr_path + "/" + output, "a")

        for line in nordicString:
            f.write(line)

        f.close()

    conn.commit()
    conn.close()

    return True
