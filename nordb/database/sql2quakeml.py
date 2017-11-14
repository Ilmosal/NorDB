from lxml import etree

import math
import sys
import time
import os
import logging

MODULE_PATH = os.path.realpath(__file__)[:-len("sql2quakeml.py")]

username = ""

from nordb.core.nordic import NordicEvent, NordicMain, NordicMacroseismic, NordicComment
from nordb.core.nordic import NordicError, NordicWaveform, NordicData
from nordb.core import usernameUtilities
from nordb.database import getNordic
import psycopg2

QUAKEML_ROOT_STRING = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?><q:quakeml xmlns:q="http://quakeml.org/xmlns/quakeml/1.2" xmlns="http://quakeml.org/xmlns/bed/1.2" xmlns:ingv="http://webservices.ingv.it/fdsnws/event/1"></q:quakeml>'''

AUTHORITY_ID = "wh.atis.ids"
NETWORK_CODE = "netcode"

EVENT_TYPE_CONVERSION = {' ': "not reported",  '*': "earthquake", 'Q': "earthquake", 'E':"explosion", 'P':"explosion" ,'I':"induced or triggered event" ,'V': "volcanic eruption", 'X':"landslide", 'A':"not reported" }
PICK_POLARITY_CONVERSION = {'C': "positive", 'D': "negative", "+": "undecidable", "-": "undecidable"}
MAGNITUDE_TYPE_CONVERSION = {'L': 'ML', 'C': 'Mc', 'B': 'mb', 'S': 'Ms', 'W': 'MW'}
INSTRUMENT_TYPE_CONVERSION = {'S': 'SH','B': 'BH', 'L': 'LH', 'H': '?H', 'E':'?E'}

def addEventParameters(quakeml, nordic, long_quakeML):
    """
    Function that adds event parameters to a quakeml etree object.

    Args:
        quakeml(etree.XML): quakeml root object
        nordic (NordicEvent): nordic event object
        long_quakeML(bool): flag for if the required file is a long or a short one
    """
    eventParameters = etree.SubElement(quakeml, "eventParameters")
    eventParameters.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/eventParameter"
    
    addEvent(eventParameters, nordic, long_quakeML)

def addEvent(eventParameters, nordic, long_quakeML):
    """
    Function for adding a complete event etree object to a eventParameters object

    Args:
        eventParameters(etree.XML): eventParameters object
        nordic (NordicEvent): nordic event_file
        long_quakeML(bool): flag for if the required file is a long or a short one
    """
    #Add event
    event = etree.SubElement(eventParameters, "event")
    event.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/event/" + str(nordic.headers[1][0].header[NordicMain.ID])

    #Adding event type  
    event_type_txt = " "
    for header in nordic.headers[1]:
        if header.header[NordicMain.EVENT_DESC_ID] is not None:
            event_type_txt = header.header[NordicMain.EVENT_DESC_ID]

    event_type = etree.SubElement(event, "type")
    event_type.text = EVENT_TYPE_CONVERSION[event_type_txt]

    #Adding event comments
    for header_comment in nordic.headers[3]:
        if header_comment.header[NordicComment.H_COMMENT] is not None:
            event_comment = etree.SubElement(event, "comment")
            event_comment_txt = etree.SubElement(event_comment, "text")
            event_comment_txt.text = header_comment.header[NordicComment.H_COMMENT]

    #Creating the all elements and their subelement
    for i in range(0,len(nordic.headers[1])):
        addOrigin(event, nordic, nordic.headers[1][i])
    
        #Adding preferred OriginID  
        if long_quakeML:
            addMagnitude(event, nordic, nordic.headers[1][i])
    
    for i in range(0, len(nordic.headers[5])):
        addFocalMech(event, nordic.headers[5][i])

    if long_quakeML:
        for phase_data in nordic.data:
            addPick(event, nordic, phase_data)
            addAmplitude(event, nordic, phase_data)
            for origin in event.iter("origin"):
                addArrival(origin, phase_data, nordic)

def addPick(event, nordic, phase_data):
    """
    Function for adding a complete event etree object to a eventParameters object

    Args:
        evemt (etree.XML): event object
        nordic (NordicEvent): nordic event_file
        phase_data(NordicData): nordic phase data object
    """
    pick = etree.SubElement(event, "pick")
    pick.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/pick/" + str(phase_data.data[NordicData.ID])

    time_value = ""
    #time value for the pick    
    if phase_data.data[NordicData.HOUR] < nordic.headers[1][0].header[NordicMain.HOUR]:
        time_value = str(nordic.headers[1][0].header[NordicMain.DATE] + datetime.timedelta(days=1)) + "T"
    else:
        time_value = str(nordic.headers[1][0].header[NordicMain.DATE]) + "T"

    if phase_data.data[NordicData.HOUR] < 10:
        time_value = time_value + "0" + str(phase_data.data[NordicData.HOUR]) + ":"
    else:
        time_value = time_value + str(phase_data.data[NordicData.HOUR]) + ":"

    if phase_data.data[NordicData.MINUTE] < 10:
        time_value = time_value + "0" + str(phase_data.data[NordicData.MINUTE]) + ":"
    else:
        time_value = time_value + str(phase_data.data[NordicData.MINUTE]) + ":"

    if phase_data.data[NordicData.SECOND] < 10:
        time_value = time_value + "0" + str(int(phase_data.data[NordicData.SECOND])) + "Z"
    else:
        time_value = time_value + str(int(phase_data.data[NordicData.SECOND])) + "Z" 

    addTime(pick, time_value, 0)

    #Pick waveform ID
    waveform_id = etree.SubElement(pick, "waveformID")
    waveform_id.attrib["networkCode"] = "" + NETWORK_CODE
    waveform_id.attrib["stationCode"] = phase_data.data[NordicData.STATION_CODE]
    if phase_data.data[NordicData.SP_INSTRUMENT_TYPE] is not None and phase_data.data[NordicData.SP_COMPONENT] is not None:
        waveform_id.attrib["channelCode"] = INSTRUMENT_TYPE_CONVERSION[phase_data.data[NordicData.SP_INSTRUMENT_TYPE]] + phase_data.data[NordicData.SP_COMPONENT]

    #Pick first motion
    if phase_data.data[NordicData.FIRST_MOTION] is not None and phase_data.data[NordicData.FIRST_MOTION] in PICK_POLARITY_CONVERSION:
        pick_polarity = etree.SubElement(pick, "polarity")  
        pick_polarity.text = PICK_POLARITY_CONVERSION[phase_data.data[NordicData.FIRST_MOTION]]

    #Pick backazimuth
    if phase_data.data[NordicData.BACK_AZIMUTH] is not None:
        pick_back_azimuth = etree.SubElement(pick, "backazimuth")
        pick_back_azimuth_value = etree.SubElement(pick_back_azimuth, "value")
        pick_back_azimuth_value.text = str(phase_data.data[NordicData.BACK_AZIMUTH])

def addAmplitude(event, nordic, phase_data):
    if phase_data.data[NordicData.MAX_AMPLITUDE] is not None:
        amplitude = etree.SubElement(event, "amplitude")
        amplitude.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/amplitude/" + str(phase_data.data[NordicData.ID])

        #adding generic amplitude
        generic_amplitude = etree.SubElement(amplitude, "genericAmplitude")
        generic_amplitude_value = etree.SubElement(generic_amplitude, "value")
        generic_amplitude_value.text = str(math.pow(phase_data.data[NordicData.MAX_AMPLITUDE], -9)) #Convert to meters from nanometers

        #Adding amplitude period
        if phase_data.data[NordicData.MAX_AMPLITUDE_PERIOD] is not None:
            amplitude_period = etree.SubElement(amplitude, "period")
            amplitude_period_value = etree.SubElement(amplitude_period, "value")
            amplitude_period_value.text = str(phase_data.data[NordicData.MAX_AMPLITUDE_PERIOD])

        #Adding amplitude unit
        amplitude_unit = etree.SubElement(amplitude, "unit")
        amplitude_unit.text = "m"

        #Adding time window
        if phase_data.data[NordicData.SIGNAL_DURATION] is not None:
            time_window = etree.SubElement(amplitude, "timeWindow")
            time_window_value = etree.SubElement(time_window, "value")
            time_window_value.text = str(phase_data.data[NordicData.SIGNAL_DURATION])

        if phase_data.data[NordicData.SIGNAL_TO_NOISE] is not None:
            snr = etree.SubElement(amplitude, "snr")
            snr.text = str(phase_data.data[NordicMain.SIGNAL_TO_NOISE])

def addOrigin(event, nordic, main):
    origin = etree.SubElement(event, "origin")
    origin.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/origin/" + str(main.header[NordicMain.ID])

    #time value for the origin
    time_value = ""
    time_value = str(main.header[NordicMain.DATE]) + "T"

    if main.header[NordicMain.HOUR] is not None:
        if main.header[NordicMain.HOUR] < 10:
            time_value = time_value + "0" + str(main.header[NordicMain.HOUR]) + ":"
        else:
            time_value = time_value + str(main.header[NordicMain.HOUR]) + ":"
    else:
        time_value = time_value + "00:"

    if main.header[NordicMain.MINUTE] is not None:
        if main.header[NordicMain.MINUTE] < 10:
            time_value = time_value + "0" + str(main.header[NordicMain.MINUTE]) + ":"
        else:
            time_value = time_value + str(main.header[NordicMain.MINUTE]) + ":"
    else:
        time_value = time_value + "00:"
    
    if main.header[NordicMain.SECOND] is not None:
        if main.header[NordicMain.SECOND] < 10:
            time_value = time_value + "0" + str(int(main.header[NordicMain.SECOND])) + "Z"
        else:
            time_value = time_value + str(int(main.header[NordicMain.SECOND])) + "Z" 
    else:
        time_value = time_value + "00Z"

    #time uncertainty   
    time_uncertainty = 1
    for h_error in nordic.headers[5]:
        if h_error.header[NordicError.ID] == main.header[NordicMain.ID]:
            time_uncertainty = h_error.second_error
            break

    addTime(origin, time_value, time_uncertainty)

    #Adding value for epicenter latitude
    if main.header[NordicMain.EPICENTER_LATITUDE] is not None:
        origin_latitude = etree.SubElement(origin, "latitude")
        origin_latitude_value = etree.SubElement(origin_latitude, "value")
        origin_latitude_value.text = str(main.header[NordicMain.EPICENTER_LATITUDE])
        for h_error in nordic.headers[5]:
            if h_error.header[NordicError.ID] == main.header[NordicMain.ID]:
                if h_error.header[NordicError.EPICENTER_LATITUDE_ERROR] is not None:
                    origin_latitude_uncertainty = etree.SubElement(origin_latitude, "uncertainty")
                    origin_latitude_uncertainty.text = str(h_error.header[NordicError.EPICENTER_LATITUDE_ERROR])
                break

    #Adding value for epicenter longitude
    if main.header[NordicMain.EPICENTER_LONGITUDE] is not None:
        origin_longitude = etree.SubElement(origin, "longitude")
        origin_longitude_value = etree.SubElement(origin_longitude, "value")
        origin_longitude_value.text = str(main.header[NordicMain.EPICENTER_LONGITUDE])
        for h_error in nordic.headers[5]:
            if h_error.header[NordicError.ID] == main.header[NordicMain.ID]:
                if h_error.header[NordicError.EPICENTER_LONGITUDE_ERROR] is not None:
                    origin_longitude_uncertainty = etree.SubElement(origin_longitude, "uncertainty")
                    origin_longitude_uncertainty.text = str(h_error.header[NordicError.EPICENTER_LONGITUDE_ERROR])
                break

    #Adding value for depth
    if main.header[NordicMain.DEPTH] is not None:
        origin_depth = etree.SubElement(origin, "depth")
        origin_depth_value = etree.SubElement(origin_depth, "value")
        origin_depth_value.text = str(main.header[NordicMain.DEPTH] * 1000)
        for h_error in nordic.headers[5]:
            if h_error.header[NordicError.ID] == main.header[NordicMain.ID]:
                if h_error.header[NordicError.DEPTH_ERROR] is not None:
                    origin_depth_uncertainty = etree.SubElement(origin_depth, "uncertainty")
                    origin_depth_uncertainty.text = str(h_error.header[NordicError.HEADER][NordicError.DEPTH_ERROR] * 1000)
                break

    #Adding value for rms time residuals
    if main.header[NordicMain.RMS_TIME_RESIDUALS] is not None:
        origin_quality = etree.SubElement(origin, "quality")
        origin_quality_standard_error = etree.SubElement(origin_quality, "standardError")
        origin_quality_standard_error.text = str(main.header[NordicMain.RMS_TIME_RESIDUALS])

def addMagnitude(event, nordic, main):
    if main.header[NordicMain.MAGNITUDE_1] is not None:
        magnitude = etree.SubElement(event, "magnitude")
        magnitude.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/magnitude/" + str(main.header[NordicMain.ID])
        
        #Adding a value for magnitude
        magnitude_mag = etree.SubElement(magnitude, "mag")
        magnitude_mag_value = etree.SubElement(magnitude_mag, "value")
        magnitude_mag_value.text = str(main.header[NordicMain.MAGNITUDE_1])
        if len(nordic.headers[5]) > 0:
            for h_error in nordic.headers[5]:
                if h_error.header[NordicError.HEADER_ID] == main.header[NordicMain.ID]:
                    if h_error.header[NordicError.MAGNITUDE_ERROR] is not None:
                        magnitude_mag_uncertainty = etree.SubElement(magnitude_mag, "uncertainty")
                        magnitude_mag_uncertainty.text = str(h_error.header[NordicError.MAGNITUDE_ERROR])
                    break

        #Adding magnitude type 
        if main.header[NordicMain.TYPE_OF_MAGNITUDE_1] is not None and main.header[NordicMain.TYPE_OF_MAGNITUDE_1] in MAGNITUDE_TYPE_CONVERSION:
            magnitude_type = etree.SubElement(magnitude, "type")
            magnitude_type.text = MAGNITUDE_TYPE_CONVERSION[main.header[NordicMain.TYPE_OF_MAGNITUDE_1]]
        
        #Adding number of stations 
        if main.header[NordicMain.STATIONS_USED] is not None:
            magnitude_station_count = etree.SubElement(magnitude, "stationCount")
            magnitude_station_count.text = str(main.header[NordicMain.STATIONS_USED])

        if main.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_1] is not None:
            magnitude_creation_info = etree.SubElement(magnitude, "creationInfo")
            magnitude_creation_info_agency = etree.SubElement(magnitude_creation_info, "agencyID")
            magnitude_creation_info_agency.text = main.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_1]
            magnitude_creation_info_agency_uri = etree.SubElement(magnitude_creation_info, "agencyURI")
            magnitude_creation_info_agency_uri.text = "smi:" + AUTHORITY_ID + "/agency/"

        magnitude_origin_id = etree.SubElement(magnitude, "originID")
        magnitude_origin_id.text =  "smi:" + AUTHORITY_ID + "/origin"

def addArrival(origin, phase_data, nordic):
    if phase_data.data[NordicData.PHASE_TYPE] is not None:
        arrival = etree.SubElement(origin, "arrival")
        arrival.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/arrival/" + str(phase_data.data[NordicData.ID])

        #Adding pick reference
        arrival_pick_id = etree.SubElement(arrival, "pickID")
        arrival_pick_id.text = "smi:" + AUTHORITY_ID + "/pick/" + str(phase_data.data[NordicData.ID])

        #Adding phase
        arrival_phase = etree.SubElement(arrival, "phase")
        arrival_phase.text = phase_data.data[NordicData.PHASE_TYPE]
    
        #Adding azimuth
        if phase_data.data[NordicData.EPICENTER_TO_STATION_AZIMUTH] is not None:
            arrival_azimuth = etree.SubElement(arrival, "azimuth")
            arrival_azimuth.text = str(phase_data.data[NordicData.EPICENTER_TO_STATION_AZIMUTH])
    
        #Adding time residual
        if phase_data.data[NordicData.TRAVEL_TIME_RESIDUAL] is not None:
            arrival_time_residual = etree.SubElement(arrival, "timeResidual")
            arrival_time_residual.text = str(phase_data.data[NordicData.TRAVEL_TIME_RESIDUAL])

        #Adding arrival distance
        if phase_data.data[NordicData.EPICENTER_DISTANCE] is not None:
            arrival_distance = etree.SubElement(arrival, "distance")
            arrival_distance.text = str(phase_data.data[NordicData.EPICENTER_DISTANCE])

#TODO: See if station magnitude information can be found from somewhere. Without it stationMagnitude and staionMagnitudeContribution elements are useless.

#TODO: addStationMag
#def addStationMag(event, phase_data.data[NordicData.] nordic):
#   if phase_data.data[NordicData.MAX_AMPLITUDE] is not None:
#       station_magnitude = etree.SubElement(event, "stationMagnitude")
#       station_magnitude.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/path/to/stationmag/"
#TODO: addStationMagContribution

#TODO: addFocalMech
def addFocalMech(event, h_error):
    if (h_error.header[NordicError.GAP] is not None):
        focal_mechanism = etree.SubElement(event, "focalMechanism")
        focal_mechanism.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/path/to/focalMech"
        
        #Adding Gap
        focal_mechanism_gap = etree.SubElement(focal_mechanism, "azimuthalGap")
        focal_mechanism_gap.text = str(h_error.header[NordicError.GAP])

def addTime(container, time_value, time_uncertainty):
    time = etree.SubElement(container, "time")
    value = etree.SubElement(time, "value")
    value.text = time_value

    if time_uncertainty != 0:
        uncertainty = etree.SubElement(time, "uncertainty")
        uncertainty.text = str(time_uncertainty)

def validateQuakeMlFile(test, xmlschema):
    try:
        xmlschema.assertValid(test)
        return True
    except:
        log = xmlschema.error_log.last_error
        logging.error("QuakeML file did not go through the validation:")
        logging.error(log.domain_name + ": " + log.type_name)
        return False

def nordicEventToQuakeMl(nordicEvent, long_quakeML):
    f = open(MODULE_PATH + "../xml/QuakeML-1.2.xsd")
    xmlschema_doc = etree.parse(f)
    f.close()

    utf8_parser = etree.XMLParser(encoding='utf-8')
    quakeml = etree.fromstring(QUAKEML_ROOT_STRING.encode('utf-8'), utf8_parser)

    addEventParameters(quakeml, nordicEvent, long_quakeML)

    xmlschema = etree.XMLSchema(xmlschema_doc)

    #Parse the tree to a string and back to the object because of a weird bug on validating the tree...
    test = etree.tostring(quakeml)
    quakeml = etree.XML(test)

    if not validateQuakeMlFile(quakeml, xmlschema):
        sys.exit(-1)

    return quakeml

def writeQuakeML(nordicEventId, usr_path, output):
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
        return False

    cur = conn.cursor()

    nordic = getNordic.readNordicEvent(cur, nordicEventId)
 
    if nordic == None:
        return False

    main = nordic.headers[1][0]
    
    filename = "{:d}{:03d}{:02d}{:02d}{:02d}".format(   main.header[NordicMain.DATE].year, 
                                                        main.header[NordicMain.DATE].timetuple().tm_yday, 
                                                        main.header[NordicMain.HOUR], 
                                                        main.header[NordicMain.MINUTE], 
                                                        int(main.header[NordicMain.SECOND])) + ".xml"

    quakeMLString = etree.tostring(nordicEventToQuakeMl(nordic, True), pretty_print=True)   

    print(filename + " has been created!")
    
    f = open(usr_path + "/" + filename, 'wb')
    
    f.write(quakeMLString)

    f.close()
    conn.close()

    return True
