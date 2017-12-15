"""
This module is for converting the station information from the database into stationxml format. The most important function of this module is writeNetworkToStationXML(network, output_path) which takes all stations from one network and dumps them to a single stationxml file.
"""

import os
import logging
import psycopg2
from datetime import datetime
from lxml import etree

MODULE_PATH = os.path.realpath(__file__)[:-len("sql2stationxml.py")]

username = ""

from nordb.database import sql2station, sql2sitechan
from nordb.database.station2sql import Station, SiteChan
from nordb.core import usernameUtilities

def station2stationxml(station):
    """
    Method for converting a Station list, sitechan list and network_code to a stationxml lxml object
  
    **Args:**
        * station (list) -- Station list that needs to be converted. 

    **Returns:**
        * StationXML etree object
    """

    stationXML = etree.Element("Station")    
    stationXML.attrib["code"] = station[Station.STATION_CODE]   

    latitude = etree.SubElement(stationXML, "Latitude")
    latitude.text = str(station[Station.LATITUDE])

    longitude = etree.SubElement(stationXML, "Longitude")
    longitude.text = str(station[Station.LONGITUDE])

    elevation = etree.SubElement(stationXML, "Elevation")
    elevation.text = str(station[Station.ELEVATION])

    site = etree.SubElement(stationXML, "Site")
    siteName = etree.SubElement(site, "Name") 
    siteName.text = station[Station.STATION_NAME]  
 
    creationDate = etree.SubElement(stationXML, "CreationDate")
    creationDate.text = str(station[Station.ON_DATE]) + "T" + "00:00:00+00:00"

    if station[Station.OFF_DATE] is not None:
        terminationDate = etree.SubElement(stationXML, "TerminationDate")
        terminationDate.text = str(station[Station.OFF_DATE]) + "T" + "00:00:00+00:00"

    conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    cur = conn.cursor()

    cur.execute("SELECT sitechan.id FROM sitechan, station WHERE station_code = %s AND sitechan.station_id = station.id", (station[Station.STATION_CODE],))
    channel_ids = cur.fetchall()

    for cha in channel_ids:
        channel = sql2sitechan.readSitechan(cha[0])
        stationXML.append(channel2stationXML(channel, station))

    conn.close()
 
    return stationXML

def channel2stationXML(sitechan, station):
    """
    Create channel xml and return it

    **Args:**
        * sitechan(list) -- Sitechan object that will be converted into a xml etree object
    
    **Returns:**
        * Lxml etree object of a channel defined by FNDS format
    """
    channelXML = etree.Element("Channel")
    channelXML.attrib["code"] = sitechan[SiteChan.CHANNEL_CODE]
    channelXML.attrib["locationCode"] = "HE"
    channelXML.attrib["startDate"] = str(sitechan[SiteChan.ON_DATE]) + "T" + "00:00:00+00:00"
    if sitechan[SiteChan.OFF_DATE] is not None:
        channelXML.attrib["endDate"] = str(sitechan[SiteChan.OFF_DATE]) + "T" + "00:00:00+00:00"

    
    latitude = etree.SubElement(channelXML, "Latitude")
    latitude.text = str(station[Station.LATITUDE])

    longitude = etree.SubElement(channelXML, "Longitude")
    longitude.text = str(station[Station.LONGITUDE])

    elevation = etree.SubElement(channelXML, "Elevation")
    elevation.text = str(station[Station.ELEVATION])

    depth = etree.SubElement(channelXML, "Depth")
    depth.text = str(sitechan[SiteChan.EMPLACEMENT_DEPTH])   

    azimuth = etree.SubElement(channelXML, "Azimuth")
    azimuth.text = str((int(sitechan[SiteChan.HORIZONTAL_ANGLE]) + 180) % 360)

    dip = etree.SubElement(channelXML, "Dip")
    dip.text = str(int(sitechan[SiteChan.VERTICAL_ANGLE]))

    return channelXML

def writeNetworkToStationXML(network, output_path):
    """
    Method for writing all stations of a network in database into a stationXML file.

    **Args:**
       * network (str) -- Network from which all the stations are taken from.
       * output_path(str) -- Path to output file.
    """
    username = usernameUtilities.readUsername() 

    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return None

    cur = conn.cursor()

    cur.execute("SELECT station.id FROM station, network where network.id = station.network_id AND network.network = %s;", (network,))

    ans = cur.fetchall()
    
    station_ids = []

    if not ans:
        logging.error("No stations with network {0} in the database!".format(network))
        return

    for a in ans:
        station_ids.append(a[0])
  
    conn.close()

    stations = []

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
    networkXml.attrib["code"] = network

    for station_id in station_ids:
        networkXml.append(station2stationxml(sql2station.readStation(station_id)))

    f = open(MODULE_PATH + "../xml/fdsn-station-1.0.xsd")
    xmlschema_doc = etree.parse(f)
    f.close()
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xmlstring = etree.tostring(stationroot, pretty_print=True)
    newSchema = etree.XML(xmlstring)
    
    if not xmlschema.validate(newSchema):
        log = xmlschema.error_log.last_error
        logging.error("StationXML file did not go through validation: ")
        logging.error(log)
        return

    fout = open(output_path, "w")
    fout.write(xmlstring.decode("ascii"))
