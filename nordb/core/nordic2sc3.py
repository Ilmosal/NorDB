"""
This module contains tools to convert a nordic file to a `SC3 file`_. This is done by converting the nordic first to a quakeml etree.XML object and then converting it to SC3 from there using the schema in the geofon website.

.. _SC3 file: http://geofon.gfz-potsdam.de/schema/0.9/

Functions and Classes
---------------------
"""

from lxml import etree
import os

from nordb.core import nordic2quakeml

def nordic2SC3(nordic_events):
    """
    Function that converts a NordicEvent object array into a lxml etree object in SC3 format.
    
    :param NordicEvent nordic_event: nordicEvent that will be converted
    :returns: SC3 file in lxml Etree object
    """
    if nordic_events is None or not nordic_events:
        return None

    qmls = nordic2quakeml.nordicEvents2QuakeML(nordic_events, True)
    
    f = open(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep +"xml" + os.sep + "quakeml_1.2__sc3ml_0.9.xsl")
    qml2scc3 = etree.parse(f)
    f.close()

    qml2sc3_transform = etree.XSLT(qml2scc3)

    return qml2sc3_transform(qmls)
