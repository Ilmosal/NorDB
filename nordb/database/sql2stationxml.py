import os
import logging
import psycopg2
from datetime import datetime
from lxml import etree

MODULE_PATH = os.path.realpath(__file__)[:-len("sql2stationxml.py")]

username = ""

from nordb.database import sql2station
from nordb.database.station2sql import Station
from nordb.core import usernameUtilities

def station2stationxml(station):
    """
    Method for converting a Station object to a stationxml lxml object

    CONVERSIONS:
    Station
    ------------------------------
    Station.station_code - FDSNStationxml.Station.Site.Name 
    Station.network_id   - FDSNStationxml.Source
    Station.on_date      - FDSNStationxml.Station.CreationDate
    Station.off_date     - FDSNStationxml.Station.TerminationDate
    Station.latitude     - FDSNStationxml.Station.Latitude.value
    Station.longitude    - FDSNStationxml.Station.Longitude.value  
    Station.elevation    - FDSNStationxml.Station.Elevation.value
    Station.station_name - FDSNStationxml.Station.Site.Description
    Station.load_date    - FDSNStationxml.Station.loasdads
    
    Args:
        station (Station): station object that needs to be converted.

    Returns:
        StationXML etree object
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
   
    return stationXML

def writeNetworkToStationXML(network, output_path):
    """
    Method for writing all stations of a network in database into a stationXML file.

    Args:
        output_path(str): path to output file
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

    conn.close()
    
    station_ids = []

    if not ans:
        logging.error("No stations with network {0} in the database!".format(network))
        return

    for a in ans:
        station_ids.append(a[0])
  
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
    
    try:
        xmlschema.assertValid(newSchema)
    except:
        log = xmlschema.error_log.last_error
        logging.error("StationXML file did not go through validation: ")
        logging.error(log)
        return

    fout = open(output_path, "w")
    fout.write(xmlstring.decode("ascii"))
