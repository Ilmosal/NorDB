"""
This module contains tools to convert a nordic file to a `SC3 file`_. This is done by converting the nordic first to a quakeml etree.XML object and then converting it to SC3 from there using the schema in the geofon website.

.. _SC3 file: http://geofon.gfz-potsdam.de/schema/0.9/

Functions and Classes
---------------------
"""

from lxml import etree
import logging
import sys
import os

import psycopg2

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))

from nordb.core import usernameUtilities
from nordb.core.nordic import NordicMain
from nordb.database import getNordic
from nordb.database import sql2quakeml

def writeSC3(nordic_event_ids, usr_path, output):
    """
    A function for writing sc3 file based on a nordic event with id of nordicEventId. The file is created by converting the nordic event to a quakeml etree object then parsing it into a sc3 etree object with the transformation stylesheet quakeml_1.2__sc3ml_0.9.xsl.

    :param array nordic_event_ids: list of ids wanted
    :param str usr_path: path to where the file is written to
    :param str output: output file name
    :returns: True or False depending on if the write was succesful or not
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    
    nordics = []

    for n_id in nordic_event_ids:
        nordics.append(getNordic.readNordicEvent(cur, n_id))

    [n for n in nordics if n is not None]

    if nordics is None or len(nordics) < 0:
        return False
    
    qmls = sql2quakeml.nordicEventToQuakeMl(nordics, True)

    if qmls == None:
        return False

    f = open(MODULE_PATH + "../xml/quakeml_1.2__sc3ml_0.9.xsl") #Raises exception if file is missing
       
    qml2scc3 = etree.parse(f)
    f.close()

    qml2sc3_transform = etree.XSLT(qml2scc3)

    sc3doc = qml2sc3_transform(qmls)

    if len(nordics) == 1 and output is None:
        nordic = nordics[0]
        main = nordic.headers[1][0]

        filename = "{:d}{:03d}{:02d}{:02d}{:02d}".format(   main.header[NordicMain.DATE].year, 
                                                            main.header[NordicMain.DATE].timetuple().tm_yday, 
                                                            main.header[NordicMain.HOUR], 
                                                            main.header[NordicMain.MINUTE], 
                                                            int(main.header[NordicMain.SECOND])) + ".xml"
    else:
        filename = output

    f = open(usr_path + os.sep + filename, "wb")

    print(filename + " has been created")

    f.write(etree.tostring(sc3doc, pretty_print=True))

    f.close()
    conn.close()

    return True
