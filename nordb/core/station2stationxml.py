"""
This module is for converting the station information from the database into stationxml format. The most important function of this module is writeNetworkToStationXML(network, output_path) which takes all stations from one network and dumps them to a single stationxml file.

Functions and Classes
---------------------
"""

import os
import psycopg2
from datetime import datetime
from lxml import etree

from nordb.database import sql2station, sql2sitechan
from nordb.nordic.station import Station
from nordb.nordic.sitechan import SiteChan
from nordb.core import usernameUtilities

def station2stationxml(station):
    """
    Method for converting a Station object to a stationxml lxml object
  
    :param Station station: Station list that needs to be converted. 
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

    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT sitechan.id FROM sitechan, station WHERE station_code = %s AND sitechan.station_id = station.id", (station.station_code,))
    channel_ids = cur.fetchall()

    for cha in channel_ids:
        channel = sql2sitechan.readSitechan(cha[0])
        stationXML.append(channel2stationXML(channel, station))

    conn.close()
 
    return stationXML

def channel2stationXML(sitechan, station):
    """
    Create channel xml and return it

    :param array sitechan: Sitechan object that will be converted into a xml etree object
    :returns: lxml etree object of a channel defined by FNDS format
    """
    channelXML = etree.Element("Channel")
    channelXML.attrib["code"] = channel.channel_code
    channelXML.attrib["locationCode"] = "HE"
    channelXML.attrib["startDate"] = str(channel.on_date) + "T" + "00:00:00+00:00"

    if channel.off_date is not None:
        channelXML.attrib["endDate"] = str(channel.off_date) + "T" + "00:00:00+00:00"

    latitude = etree.SubElement(channelXML, "Latitude")
    latitude.text = str(station.latitude)

    longitude = etree.SubElement(channelXML, "Longitude")
    longitude.text = str(station.longitude)

    elevation = etree.SubElement(channelXML, "Elevation")
    elevation.text = str(station.elevation)

    depth = etree.SubElement(channelXML, "Depth")
    depth.text = str(channel.emplacement_depth)   

    azimuth = etree.SubElement(channelXML, "Azimuth")
    azimuth.text = str((int(channel.horizontal_angle) + 180) % 360)

    dip = etree.SubElement(channelXML, "Dip")
    dip.text = str(int(channel.vertical_angle))

    return channelXML

#def createStationXML(station):
#    """
#    Function for creating a stationxml etree object from a station
#    
#    :param Station station:
#    """
#    pass

def writeNetworkToStationXML(network, output_path):
    """
    Method for writing all stations of a network in database into a stationXML file.

    :param str network: Network from which all the stations are taken from.
    :param str output_path: path to output file.
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT station.id FROM station, network where network.id = station.network_id AND network.network = %s;", (network,))

    ans = cur.fetchall()
    
    station_ids = []

    if not ans:
        raise Exception("No stations with Network {0} in the database".format(network))

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
        raise Exception("StationXML file did not go through validation:\n{0}".format(log))
        
    fout = open(output_path, "w")
    fout.write(xmlstring.decode("ascii"))
