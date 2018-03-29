"""
This module contains all functions for converting a nordic file to a quakeml file. Description of quakeml format is found `here`_.

.. _here: https://quake.ethz.ch/quakeml/QuakeML

Functions and Classes
---------------------
"""

from lxml import etree

import math
import datetime
import os

MODULE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep

QUAKEML_ROOT_STRING =   (
    '<?xml version="1.0" encoding="utf-8" standalone="yes"?>'
    '<q:quakeml xmlns:q="http://quakeml.org/xmlns/quakeml/1.2" xmlns="http://quakeml.org/xmlns/bed/1.2" xmlns:ingv="http://webservices.ingv.it/fdsnws/event/1">'
    '</q:quakeml>'
                        )

AUTHORITY_ID = "wh.atis.ids"

EVENT_TYPE_CONVERSION = {
                            ' ': "not reported",  
                            '*': "earthquake", 
                            'Q': "earthquake", 
                            'E':"explosion", 
                            'P':"explosion" ,
                            'I':"induced or triggered event" ,
                            'V': "volcanic eruption", 
                            'X':"landslide", 
                            'A':"not reported" 
                        }

PICK_POLARITY_CONVERSION = {'C': "positive", 'D': "negative", "+": "undecidable", "-": "undecidable"}
MAGNITUDE_TYPE_CONVERSION = {'L': 'ML', 'C': 'Mc', 'B': 'mb', 'S': 'Ms', 'W': 'MW'}
INSTRUMENT_TYPE_CONVERSION = {'S': 'SH','B': 'BH', 'L': 'LH', 'H': '?H', 'E':'?E'}
PICK_ONSET_CONVERSION = {'I':"impulsive", 'E':"emergent"}

# Assuming the earth is a sphere with radius of 6371 km which is a totally valid assumption.
MAGIC_KM2DEG_CONSTANT = 111.19

def addEventParameters(quakeml, nordics, long_quakeML):
    """
    Function that adds event parameters to a quakeml etree object.

    :param etree.XML quakeml: quakeml root object
    :param array nordics: array of nordic event objects
    :param bool long_quakeML: flag for if the required file is a long or a short one
    """
    eventParameters = etree.SubElement(quakeml, "eventParameters")
    eventParameters.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/eventParameter"

    for nordic in nordics:
        addEvent(eventParameters, nordic, long_quakeML)

def addEvent(eventParameters, nordic, long_quakeML):
    """
    Function for adding a complete event etree object to a eventParameters object

    :param etree.XML eventParameters: eventParameters object
    :param NordicEvent nordic: nordic event object
    :param bool long_quakeML: flag for if the required file is a long or a short one
    """
    #Add event
    event = etree.SubElement(eventParameters, "event")
    event.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/event/" + str(nordic.main_h[0].h_id)

    #Add preferred OriginID
    event_preferred_origin = etree.SubElement(event, "preferredOriginID")
    event_preferred_origin.text = "smi:" + AUTHORITY_ID + "/origin/" + str(nordic.main_h[0].h_id)

    #Add preferred magnitudeID
    event_preferred_magnitude = etree.SubElement(event, "preferredMagnitudeID")
    event_preferred_magnitude.text = "smi:" + AUTHORITY_ID + "/magnitude/" + str(nordic.main_h[0].h_id)

    #Adding event type  
    event_type_txt = " "
    for header in nordic.main_h:
        if header.event_desc_id is not None:
            event_type_txt = header.event_desc_id

    event_type = etree.SubElement(event, "type")
    event_type.text = EVENT_TYPE_CONVERSION[event_type_txt]

    #Add event description
    event_description = etree.SubElement(event, "description")
    event_description_text = etree.SubElement(event_description, "text")
    if nordic.main_h[0].event_desc_id is None:
        event_description_text.text = nordic.main_h[0].distance_indicator + " "
    else:
        event_description_text.text =   (
                                            nordic.main_h[0].distance_indicator
                                            + nordic.main_h[0].event_desc_id
                                        )
    #Adding event comments
    for header_comment in nordic.comment_h:
        if header_comment.h_comment is not None:
            event_comment = etree.SubElement(event, "comment")
            event_comment_txt = etree.SubElement(event_comment, "text")
            event_comment_txt.text = header_comment.h_comment

    #Creating the all elements and their subelement
    for i in range(0,len(nordic.main_h)):
        addOrigin(event, nordic, nordic.main_h[i])
    
        #Adding preferred OriginID  
    for i in range(0,len(nordic.main_h)):
        if long_quakeML:
            addMagnitude(event, nordic, nordic.main_h[i])
    
    for main in nordic.main_h:
        if main.error_h is not None:
            addFocalMech(event, main.error_h)

    if long_quakeML:
        for phase_data in nordic.data:
            addPick(event, nordic, phase_data)

        for phase_data in nordic.data:
            addAmplitude(event, phase_data)

        for phase_data in nordic.data:
            for origin in event.iter("origin"):
                if origin.get("publicID") == event_preferred_origin.text:
                    addArrival(origin, phase_data)

def addPick(event, nordic, phase_data):
    """
    Function for adding a pick etree object to a event object

    :param etree.XML event: event object
    :param NordicEvent nordic: nordic event_file
    :param NordicData phase_data: nordic phase data object
    """
    pick = etree.SubElement(event, "pick")
    pick.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/pick/" + str(phase_data.d_id)

    time = etree.SubElement(pick, "time")
    value = etree.SubElement(time, "value")
    value.text = phase_data.observation_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    #Pick waveform ID
    waveform_id = etree.SubElement(pick, "waveformID")
    waveform_id.attrib["networkCode"] = "" + nordic.main_h[0].magnitude_reporting_agency_1
    waveform_id.attrib["stationCode"] = phase_data.station_code
    if phase_data.sp_instrument_type is not None and phase_data.sp_component is not None:
        waveform_id.attrib["channelCode"] = INSTRUMENT_TYPE_CONVERSION[phase_data.sp_instrument_type] + phase_data.sp_component

    #Quality indicator
    if phase_data.quality_indicator is not None:
        onset = etree.SubElement(pick, "onset")
        onset.text = PICK_ONSET_CONVERSION[phase_data.quality_indicator]

    #Phase_type
    if phase_data.phase_type is not None:
        phaseHint = etree.SubElement(pick, "phaseHint")
        phaseHint.text = phase_data.phase_type

    #Pick first motion
    if phase_data.first_motion is not None and phase_data.first_motion in PICK_POLARITY_CONVERSION:
        pick_polarity = etree.SubElement(pick, "polarity")  
        pick_polarity.text = PICK_POLARITY_CONVERSION[phase_data.first_motion]

    #Pick backazimuth
    if phase_data.back_azimuth is not None:
        pick_back_azimuth = etree.SubElement(pick, "backazimuth")
        pick_back_azimuth_value = etree.SubElement(pick_back_azimuth, "value")
        pick_back_azimuth_value.text = str(phase_data.back_azimuth)

    pick_evaluation_mode = etree.SubElement(pick, "evaluationMode")
    pick_evaluation_mode.text = "manual"

def addAmplitude(event, phase_data):
    """
    :param etree.XML event: event object
    :param NordicData phase_data: nordic phase data object
    """
    if phase_data.max_amplitude is not None:
        amplitude = etree.SubElement(event, "amplitude")
        amplitude.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/amplitude/" + str(phase_data.d_id)

        #adding generic amplitude
        generic_amplitude = etree.SubElement(amplitude, "genericAmplitude")
        generic_amplitude_value = etree.SubElement(generic_amplitude, "value")
        generic_amplitude_value.text = str(math.pow(phase_data.max_amplitude, -9)) #Convert to meters from nanometers

        amplitude_type = etree.SubElement(amplitude, "type")
        amplitude_type.text = "A"

        #Adding amplitude period
        if phase_data.max_amplitude_period is not None:
            amplitude_period = etree.SubElement(amplitude, "period")
            amplitude_period_value = etree.SubElement(amplitude_period, "value")
            amplitude_period_value.text = str(phase_data.max_amplitude_period)

        #Adding amplitude unit
        amplitude_unit = etree.SubElement(amplitude, "unit")
        amplitude_unit.text = "m"

        #Adding time window
        if phase_data.signal_duration is not None:
            time_window = etree.SubElement(amplitude, "timeWindow")
            time_window_value = etree.SubElement(time_window, "value")
            time_window_value.text = str(phase_data.signal_duration)

        if phase_data.signal_to_noise is not None:
            snr = etree.SubElement(amplitude, "snr")
            snr.text = str(phase_data.signal_to_noise)

def addOrigin(event, nordic, main):
    """
    Function for adding a origin etree object to a event object

    :param etree.XML event: event object
    :param NordicEvent nordic: nordic event_file
    :param NordicData phase_data: nordic phase data object
    """
    origin = etree.SubElement(event, "origin")
    origin.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/origin/" + str(main.h_id)

    time = etree.SubElement(origin, "time")
    time_value = etree.SubElement(time, "value")
    time_value.text = main.origin_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if main.error_h:
        time_uncertainty = etree.SubElement(time, "uncertainty") 
        time_uncertainty.text = str(main.error_h.second_error)

    #Adding value for epicenter latitude
    if main.epicenter_latitude is not None:
        origin_latitude = etree.SubElement(origin, "latitude")
        origin_latitude_value = etree.SubElement(origin_latitude, "value")
        origin_latitude_value.text = str(main.epicenter_latitude)

        if main.error_h is not None and main.error_h.epicenter_latitude_error is not None:
            origin_latitude_uncertainty = etree.SubElement(origin_latitude, "uncertainty")
            origin_latitude_uncertainty.text = str(main.error_h.epicenter_latitude_error)

    #Adding value for epicenter longitude
    if main.epicenter_longitude is not None:
        origin_longitude = etree.SubElement(origin, "longitude")
        origin_longitude_value = etree.SubElement(origin_longitude, "value")
        origin_longitude_value.text = str(main.epicenter_longitude)

        if main.error_h is not None and main.error_h.epicenter_longitude_error is not None:
            origin_longitude_uncertainty = etree.SubElement(origin_longitude, "uncertainty")
            origin_longitude_uncertainty.text = str(main.error_h.epicenter_longitude_error)

    #Adding value for depth
    if main.depth is not None:
        origin_depth = etree.SubElement(origin, "depth")
        origin_depth_value = etree.SubElement(origin_depth, "value")
        origin_depth_value.text = str(main.depth * 1000)
        if main.error_h is not None and main.error_h.depth_error is not None:
            origin_depth_uncertainty = etree.SubElement(origin_depth, "uncertainty")
            origin_depth_uncertainty.text = str(main.error_h.epicenter_depth_error)

    #Adding value for rms time residuals
    if main.rms_time_residuals is not None:
        origin_quality = etree.SubElement(origin, "quality")
        origin_quality_standard_error = etree.SubElement(origin_quality, "standardError")
        origin_quality_standard_error.text = str(main.rms_time_residuals)

def addMagnitude(event, nordic, main):
    """
    Function for adding a magnitude etree object to a event object

    :param etree.XML event: event lxml object
    :param NordicEvent nordic: nordic event object
    :param NordicMain main: nordic main header object
    """

    if main.magnitude_1 is not None:
        magnitude = etree.SubElement(event, "magnitude")
        magnitude.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/magnitude/" + str(main.h_id)
        
        #Adding a value for magnitude
        magnitude_mag = etree.SubElement(magnitude, "mag")
        magnitude_mag_value = etree.SubElement(magnitude_mag, "value")
        magnitude_mag_value.text = str(main.magnitude_1)
        if main.error_h is not None and main.error_h.magnitude_error is not None:
            magnitude_mag_uncertainty = etree.SubElement(magnitude_mag, "uncertainty")
            magnitude_mag_uncertainty.text = str(main.error_h.magnitude_error)

        #Adding magnitude type 
        if main.type_of_magnitude_1 is not None and main.type_of_magnitude_1 in MAGNITUDE_TYPE_CONVERSION:
            magnitude_type = etree.SubElement(magnitude, "type")
            magnitude_type.text = MAGNITUDE_TYPE_CONVERSION[main.type_of_magnitude_1]
        
        #Adding number of stations 
        if main.stations_used is not None:
            magnitude_station_count = etree.SubElement(magnitude, "stationCount")
            magnitude_station_count.text = str(main.stations_used)

        if main.magnitude_reporting_agency_1 is not None:
            magnitude_creation_info = etree.SubElement(magnitude, "creationInfo")
            magnitude_creation_info_agency = etree.SubElement(magnitude_creation_info, "agencyID")
            magnitude_creation_info_agency.text = main.magnitude_reporting_agency_1
            magnitude_creation_info_agency_uri = etree.SubElement(magnitude_creation_info, "agencyURI")
            magnitude_creation_info_agency_uri.text = "smi:" + AUTHORITY_ID + "/agency/"

        magnitude_origin_id = etree.SubElement(magnitude, "originID")
        magnitude_origin_id.text =  "smi:" + AUTHORITY_ID + "/origin/" + str(main.h_id)


def addArrival(origin, phase_data):
    """
    Function that creates an Arrival lxml object and pastes it to origin lxml object

    :param etree.XML origin: origin lxml object to which the arrival is put to
    :param NordicData phase_data: phase data object from which the data is taken from
    """
    if phase_data.phase_type is not None:
        arrival = etree.SubElement(origin, "arrival")
        arrival.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/arrival/" + str(phase_data.d_id)

        #Adding pick reference
        arrival_pick_id = etree.SubElement(arrival, "pickID")
        arrival_pick_id.text = "smi:" + AUTHORITY_ID + "/pick/" + str(phase_data.d_id)

        #Adding phase
        arrival_phase = etree.SubElement(arrival, "phase")
        arrival_phase.text = phase_data.phase_type
    
        #Adding azimuth
        if phase_data.epicenter_to_station_azimuth is not None:
            arrival_azimuth = etree.SubElement(arrival, "azimuth")
            arrival_azimuth.text = str(phase_data.epicenter_to_station_azimuth)
    
        #Adding time residual
        if phase_data.travel_time_residual is not None:
            arrival_time_residual = etree.SubElement(arrival, "timeResidual")
            arrival_time_residual.text = str(phase_data.travel_time_residual)

        #Adding arrival distance
        if phase_data.epicenter_distance is not None:
            arrival_distance = etree.SubElement(arrival, "distance")
            arrival_distance.text = str(phase_data.epicenter_distance/MAGIC_KM2DEG_CONSTANT)

def addFocalMech(event, h_error):
    """
    Function for adding a Focal Mechanism etree object to a event object

    :param etree.XML event: event object
    :param NordicError h_error: nordic error header object
    """

    if h_error.gap is not None:
        focal_mechanism = etree.SubElement(event, "focalMechanism")
        focal_mechanism.attrib["publicID"] = "smi:" + AUTHORITY_ID + "/path/to/focalMech"
        
        #Adding Gap
        focal_mechanism_gap = etree.SubElement(focal_mechanism, "azimuthalGap")
        focal_mechanism_gap.text = str(h_error.gap)

def nordicEvents2QuakeML(nordic_events, long_quakeML=True):
    """
    Function that turns a array of NordicEvent objects into a quakeml etree object, validates it and returns it.
        
    :param array nordic_events: nordic event object array that will be transformed into a quakeml single file
    :param bool long_quakeML: Boolean value for if you want the file to be long
    :return: validated etree object
    """
    if nordic_events is None or not nordic_events:
        return None

    f = open(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep + "xml" + os.sep + "QuakeML-1.2.xsd")
    xmlschema_doc = etree.parse(f)
    f.close()

    utf8_parser = etree.XMLParser(encoding='utf-8')
    quakeml = etree.fromstring(QUAKEML_ROOT_STRING.encode('utf-8'), utf8_parser)

    addEventParameters(quakeml, nordic_events, long_quakeML)

    xmlschema = etree.XMLSchema(xmlschema_doc)

    #Parse the tree to a string and back to the object because of a weird bug on validating the tree. Probably an encoding problem or something
    test = etree.tostring(quakeml)
    quakeml = etree.XML(test)

    xmlschema.assertValid(quakeml)

    return quakeml
