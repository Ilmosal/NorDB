"""
This module is for converting the station information from the database into stationxml format. The most important function of this module is writeNetworkToStationXML(network, output_path) which takes all stations from one network and dumps them to a single stationxml file.

Functions and Classes
---------------------
"""

import os
from datetime import datetime
from lxml import etree

from nordb.database import sql2station, sql2sitechan
from nordb.nordic.station import Station
from nordb.nordic.sitechan import SiteChan
from nordb.core import usernameUtilities

MODULE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep

def station2stationxml(station):
    """
    Method for converting a Station object to a stationxml lxml object
  
    :param Station station: Station object that needs to be converted. 
    :returns: StationXML etree object
    """
    stationXML = etree.Element("Station")    
    stationXML.attrib["code"] = station.station_code   

    latitude = etree.SubElement(stationXML, "Latitude")
    latitude.text = str(station.latitude)

    longitude = etree.SubElement(stationXML, "Longitude")
    longitude.text = str(station.longitude)

    elevation = etree.SubElement(stationXML, "Elevation")
    elevation.text = str(station.elevation)

    site = etree.SubElement(stationXML, "Site")
    siteName = etree.SubElement(site, "Name") 
    siteName.text = station.station_name  
 
    creationDate = etree.SubElement(stationXML, "CreationDate")
    creationDate.text = str(station.on_date) + "T" + "00:00:00+00:00"

    if station.off_date is not None:
        terminationDate = etree.SubElement(stationXML, "TerminationDate")
        terminationDate.text = str(station.off_date) + "T" + "00:00:00+00:00"

    for cha in station.sitechans:
        stationXML.append(channel2stationXML(cha, station))

    return stationXML

def channel2stationXML(sitechan, station):
    """
    Create channel xml and return it

    :param SiteChan sitechan: Sitechan object that will be converted into a xml etree object
    :returns: lxml etree object of a channel defined by FNDS format
    """
    channelXML = etree.Element("Channel")
    channelXML.attrib["code"] = sitechan.channel_code
    channelXML.attrib["locationCode"] = "HE"
    if sitechan.on_date is not None:
        channelXML.attrib["startDate"] = str(sitechan.on_date) + "T" + "00:00:00+00:00"

    if sitechan.off_date is not None:
        channelXML.attrib["endDate"] = str(sitechan.off_date) + "T" + "00:00:00+00:00"

    latitude = etree.SubElement(channelXML, "Latitude")
    latitude.text = str(station.latitude)

    longitude = etree.SubElement(channelXML, "Longitude")
    longitude.text = str(station.longitude)

    elevation = etree.SubElement(channelXML, "Elevation")
    elevation.text = str(station.elevation)

    depth = etree.SubElement(channelXML, "Depth")
    depth.text = str(sitechan.emplacement_depth)   

    azimuth = etree.SubElement(channelXML, "Azimuth")
    azimuth.text = str((int(sitechan.horizontal_angle) + 180) % 360)

    dip = etree.SubElement(channelXML, "Dip")
    dip.text = str(int(sitechan.vertical_angle))

    return channelXML

def stationsToStationXML(stations):
    """
    Method for writing all stations given into a stationXML file.

    :param array stations: Array of stations that need to be put into a stationXLM file
    :returns: lxml etree object or None is stations array is empty
    """
    if stations is []: 
        return None

    stationroot = etree.Element("FDSNStationXML")
    stationroot.attrib["schemaVersion"] = "1.0"
    stationroot.attrib["xmlns"]="http://www.fdsn.org/xml/station/1"

    source = etree.SubElement(stationroot, "Source")
    source.text = "University of Helsinki"
    
    rootCreated = etree.SubElement(stationroot, "Created")
    createdDate = str(datetime.today())
    createdDate = createdDate[:10] + "T" + createdDate[11:]
    rootCreated.text = createdDate
    
    networkXml = etree.SubElement(stationroot, "Network")
    networkXml.attrib["code"] = stations[0].network

    for station in stations:
        networkXml.append(station2stationxml(station))

    f = open(MODULE_PATH + "/xml/fdsn-station-1.0.xsd")
    xmlschema_doc = etree.parse(f)
    f.close()
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xmlstring = etree.tostring(stationroot, pretty_print=True)
    newSchema = etree.XML(xmlstring)
    
    xmlschema.assertValid(newSchema)
       
    return newSchema 
