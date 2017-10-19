import logging
import psycopg2

from datetime import date

#class for the whole event 
class NordicEvent:
    """
    Class that represents the Nordic event. It cannot contain false information as it has been created either from database data or validated Nordic String Event object.

    Args:
        headers (NordicHeader[][]): All the headers in an array where the type of the header determines on which index of the array the headers lie
        data (NordicData[]): Array of Phase Data objects

    Attributes:
        headers (NordicHeader[][]): All the headers in an array where the type of the header determines on which index of the array the headers lie
        data (NordicData[]): Array of Phase Data objects

    """
    def __init__(self, headers, phase_data):
        self.headers = headers
        self.phase_data = phase_data    
    
#Parent class for the header
class NordicHeader:
    """
    Parent class for all the header classes in this file. Contains only the type of the header.

    Args:
        header_type (int): type of the header. 1 - main header, 2 - macroseismic header, 3 - comment header, 5 - error header, 6 - waveform header

    Attributes:
         header_type (int): type of the header. 1 - main header, 2 - macroseismic header, 3 - comment header, 5 - error header, 6 - waveform header
       
    """
    def __init__(self, header_type):
        self.header_type = header_type

class NordicPhaseData:
    """
    Class for nordic phase data. Contains the data of the database query and it's quaranteed that the data is valid.

    Args:
        phase_data (tuple): phase data from the query in tuple from which all data is taken from.
       
    Attributes:
        phase_id (int): the id of the phase data in db
        event_id (int): event id of the relevant Nordic Event
        station_code (str): station code for the station that observed this line
        sp_instrument_type (str): type of the observing instrument
        quality_indicator (str): quality indicator of the phase data line
        phase_type (str): the type of the phase 
        weight (int): the actual weight of the observation
        first motion (str): the direction of the wave
        time_info (str): str that tells which day the observation was made
        hour (int): the hour when the observation was made
        minute (int): the minute when the observation was made
        second (float): the second when the observation was made
        signal_duration (int): the duration of the signal
        max_amplitude (float): maximum amplitude of the signal during its duration
        max_amplitude_period (float): period for the maximum amplitude of the signal
        back_azimuth (float): the back azimuth of the observation
        apparent_velocity (float): apparent velocity for the signal
        signal_to_noise (float): signal to noise ratio of the signal
        azimuth_residual (int): residual of the azimuth of the location
        travel_time_residual (float): the travel time residual of the signal
        location_weight (str): the weight of the location for calculations
        epicenter_distance (int): distance from the epicenter to the station
        epicenter_to_station_azimuth (int): the azimuth of the epicenter to station
    """

    def __init__(self, phase_data):
        self.phase_id = phase_data[0]
        self.event_id = phase_data[1]
        self.station_code = phase_data[2]
        self.sp_instrument_type = phase_data[3]
        self.sp_component = phase_data[4]
        self.quality_indicator = phase_data[5]
        self.phase_type = phase_data[6]
        self.weight = phase_data[7]
        self.first_motion = phase_data[8]
        self.time_info = phase_data[9]
        self.hour = phase_data[10]
        self.minute = phase_data[11]
        self.second = phase_data[12]
        self.signal_duration = phase_data[13]
        self.max_amplitude= phase_data[14]
        self.max_amplitude_period = phase_data[15]
        self.back_azimuth = phase_data[16]
        self.apparent_velocity = phase_data[17]
        self.signal_to_noise = phase_data[18]
        self.azimuth_residual = phase_data[19]
        self.travel_time_residual = phase_data[20]
        self.location_weight = phase_data[21]
        self.epicenter_distance = phase_data[22] 
        self.epicenter_to_station_azimuth = phase_data[23]

class NordicHeaderMain(NordicHeader):
    """
    Class for nordic main header. Contains the data of the database query and it's quaranteed that the data is valid.

    Args:
        header_data ([]): header data tuple from the database query from which all data is taken from

    Attributes:
        header_id(int): header id of the main header in the database
        event_id(int): event id of the event of the main header
        date (date): date of the event
        hour (minute): hour when the event occurred
        minute (minute): minute when the event occurred
        second (float): seconc when the event occurred
        location_model (str): location model used in locating the event
        distance_indicator (str): distance indicator of the event
        event_desc_id (str): the description id of the event
        epicenter_latitude (float): latitude of the event
        epicenter_longitude (float): longitude of the event
        depth (float): depth of the event
        depth_control (str): depth cotrol flag
        locating_indicator (str): locating indicator of the event
        epicenter_reporting_agency (str): agency that reported the event
        stations_used (int): stations used in the locating process
        rms_time_residuals (float): rms of time residuals
        magnitude_1 (float): magnitude from the first magnitude reporting agency
        type_of_magnitude_1 (str): type of first magnitude 
        magnitude_reporting_agency_1 (str): the reporting agency of the first magnitude
        magnitude_2 (float): magnitude from the second magnitude reporting agency
        type_of_magnitude_2 (str): type of the second magnitude 
        magnitude_reporting_agency_2 (str):  the reporting agency of the second magnitude
        magnitude_3 (float): magnitude from the third magnitude reporting agency
        type_of_magnitude_3 (str): type of the second magnitude
        magnitude_reporting_agency_3 (str): the reporting agency of the third magnitude
    """

    def __init__(self, header_data):
        NordicHeader.__init__(self, 1)
        self.header_id = header_data[0]
        self.event_id = header_data[1]
        self.date = header_data[2]
        self.hour = header_data[3]
        self.minute = header_data[4]
        self.second =  header_data[5]
        self.location_model =  header_data[6]
        self.distance_indicator = header_data[7]
        self.event_desc_id = header_data[8]
        self.epicenter_latitude = header_data[9]
        self.epicenter_longitude = header_data[10]
        self.depth = header_data[11]
        self.depth_control = header_data[12]
        self.locating_indicator = header_data[13]
        self.epicenter_reporting_agency = header_data[14]
        self.stations_used = header_data[15]
        self.rms_time_residuals = header_data[16]
        self.magnitude_1 = header_data[17]
        self.type_of_magnitude_1 = header_data[18]
        self.magnitude_reporting_agency_1 = header_data[19]
        self.magnitude_2 = header_data[20]
        self.type_of_magnitude_2 = header_data[21]
        self.magnitude_reporting_agency_2 = header_data[22]
        self.magnitude_3 = header_data[23]
        self.type_of_magnitude_3 = header_data[24]
        self.magnitude_reporting_agency_3 = header_data[25]

class NordicHeaderMacroseismic(NordicHeader):
    """
    Class for nordic macroseismic header. Contains the data of the database query and it's quaranteed that the data is valid.

    Args:
        header_data ([]): header data array from which all data is taken from

    Attributes:
        header_id(int): header id of the main header in the database
        event_id(int): event id of the event of the main header
        description (str): description of the event
        diastrophism_code (str): diastrophism code of the event
        tsunami_code (str): tsunami code of the event
        seiche_code (str): seiche code of the event
        cultural_effects (str): cultural effetcs code of the event
        unusual_effects (str): unusual effetcs code of the event
        maximum_observed_intensity (float): maximum observed intensity of the event
        maximum_intensity_qualifier (str): maximum intensity qualifier of the event
        intensity_scale (str): intensity scale of the event
        macroseismic_latitude (float): macroseismic latitude of the event
        macroseismic_longitude (float): macroseismic longitude of the event
        macroseismic_magnitude (float): macroseismic magnitude of the event
        type_of_magnitude (str): type of magnitude
        logarithm_of_radius (float): logarithm of radius
        logarithm_of_area_1 (float): logarithm of area 1 
        bordering_intensity_1 (float): bordering intensity 1
        logarithm_of_area_2 (float): logarithm of area 2
        bordering_intensity_2 (float): bordering intensity 2
        quality_rank (str): quality rank of the header
        reporting_agency (str): reporting agency
    """
    def __init__(self, header_data):
        NordicHeader.__init__(self, 2)
        self.header_id = header_data[0]
        self.event_id = header_data[1]
        self.description = header_data[2]
        self.diastrophism_code = header_data[3]
        self.tsunami_code = header_data[4]
        self.seiche_code = header_data[5]
        self.cultural_effects = header_data[6]
        self.unusual_effects = header_data[7]
        self.maximum_observed_intensity = header_data[8]
        self.maximum_intensity_qualifier = header_data[9]
        self.intensity_scale = header_data[10]
        self.macroseismic_latitude = header_data[11]
        self.macroseismic_longitude = header_data[12]
        self.macroseismic_magnitude = header_data[13]
        self.type_of_magnitude = header_data[14]
        self.logarithm_of_radius = header_data[15]
        self.logarithm_of_area_1 = header_data[16]
        self.bordering_intensity_1 = header_data[17]
        self.logarithm_of_area_2 = header_data[18]
        self.bordering_intensity_2 = header_data[19]
        self.quality_rank = header_data[20]
        self.reporting_agency = header_data[21]

class NordicHeaderComment(NordicHeader):
    """
    Class for nordic comment header. Contains the data of the database query and it's quaranteed that the data is valid.

    Args:
        header_data ([]): header data array from which all data is taken from

    Attributes:
        h_comment (str): the comment in the header
        event_id (int): event id of relevant nordic event
        header_id (int): header id of this header in database
    """

    def __init__(self, header_data):
        NordicHeader.__init__(self, 3)
        self.header_id = header_data[0]
        self.event_id = header_data[1]
        self.h_comment = header_data[2]

class NordicHeaderError(NordicHeader):
    """
    Class for nordic error header. Contains the data of the database query and it's quaranteed that the data is valid.

    Args:
        header_data ([]): header data array from which all data is taken from

    Attributes:
        gap (int): Azimuthal gap of the event
        second_error (float): margin of error in the main headers second
        epicenter_latitude_error (float): margin of error in epicenter latitude 
        epicenter_longitude_error (float): margin of error in epicenter longitude
        depth_error (float): margin of error in depth evaluation
        magnitude_error (float): margin of error in magnitude
        header_id (int): id of this header in database
        header_main_id (int): id of the main header where this error header refers to
    """

    def __init__(self, header_data):
        NordicHeader.__init__(self, 5)
        self.header_id = header_data[0]
        self.header_main_id = header_data[1]
        self.gap = header_data[2]
        self.second_error = header_data[3]
        self.epicenter_latitude_error = header_data[4]
        self.epicenter_longitude_error = header_data[5]
        self.depth_error = header_data[6]
        self.magnitude_error = header_data[7]

    def return_as_string(self):
        output_string = ""
        return output_string


class NordicHeaderWaveform(NordicHeader):
    """
    Class for nordic waveform header. Contains the data of the database query and it's quaranteed that the data is valid.

    Args:
        header_data ([]): header data string from which all data is cut from

    Attributes:
        waveform_info (str): the waveform location of the event
        event_id (int): event id of relevant nordic event
        header_id (int): id of this header in database
    """

    def __init__(self, header_data):
        NordicHeader.__init__(self, 6)
        self.header_id = header_data[0]
        self.event_id = header_data[1]  
        self.waveform_info = header_data[2]

def addIntToData(data, int_string):
    """
    This method adds int_string as a int to the data array if the int_string is a valid integer. Otherwise it will add None to the data array

    Args:
        data ([]): data array where the data needs to be added
        int_string (str): the value that needs to be converted to integer if possible

    Returns:
        the data array with int_string in it as a integer or None
    """
    try:
        int(int_string)
        data += (int(int_string), )
    except:
        data += (None, )

    return data

def addFloatToData(data, float_string):
    """
    This method adds float_string as a float to the data array if the float_string is a valid float. Otherwise it will add None to the data array

    Args:
        data ([]): data array where the data needs to be added
        float_string (str): the value that needs to be converted to float if possible

    Returns:
        the data array with float_string in it as a float or None
    """

    try:
        float(float_string)
        data += (float(float_string), )
    except:
        data += (None, )

    return data

def addStringToData(data, string):
    """
    This method adds string to the dataarray if the string is not empty. Otherwise it will add None to the data array

    Args:
        data ([]): data array where the data needs to be added
       _string (str): the value that needs to be put to data

    Returns:
        the data array with string in it as a string or None
    """

    if (string.strip() == ""):
        data += (None,)
    else:
        data += (string,)

    return data
    
def addDateToData(data, date_string):
    """
    This method adds date_string as a date to the data array if the date_string is a valid date. Otherwise it will add None to the data array

    Args:
        data ([]): data array where the data needs to be added
        date_string (str): the value that needs to be converted to date if possible

    Returns:
        the data array with datee_string in it as a date or None
    """

    try:
        date(year=int(date_string[:4].strip()), 
                    month=int(date_string[5:7].strip()), 
                    day=int(date_string[8:].strip()))

        data += (date(year=int(date_string[:4].strip()), 
                    month=int(date_string[5:7].strip()), 
                    day=int(date_string[8:].strip())), )
        
    except:

        data += (None,)
    
    return data

def createPhaseDataList(phase_data_string):
    """ 
    Method that creates Phase Data list from phase data string object.

    Args:
        phase_data_string: Phase data string object from nordicStringClassModule

    Returns:
        The generated list
    """
    phaseData = ()

    phaseData = addIntToData(phaseData, phase_data_string.event_id)
    phaseData = addStringToData(phaseData, phase_data_string.station_code)
    phaseData = addStringToData(phaseData, phase_data_string.sp_instrument_type)
    phaseData = addStringToData(phaseData, phase_data_string.sp_component)
    phaseData = addStringToData(phaseData, phase_data_string.quality_indicator)
    phaseData = addStringToData(phaseData, phase_data_string.phase_type)
    phaseData = addIntToData(phaseData, phase_data_string.weight)
    phaseData = addStringToData(phaseData, phase_data_string.first_motion)
    phaseData = addStringToData(phaseData, phase_data_string.time_info)
    phaseData = addIntToData(phaseData, phase_data_string.hour)
    phaseData = addIntToData(phaseData, phase_data_string.minute)
    phaseData = addFloatToData(phaseData, phase_data_string.second)
    phaseData = addIntToData(phaseData, phase_data_string.signal_duration)
    phaseData = addFloatToData(phaseData, phase_data_string.max_amplitude)
    phaseData = addFloatToData(phaseData, phase_data_string.max_amplitude_period)
    phaseData = addFloatToData(phaseData, phase_data_string.back_azimuth)
    phaseData = addFloatToData(phaseData, phase_data_string.apparent_velocity)
    phaseData = addFloatToData(phaseData, phase_data_string.signal_to_noise)
    phaseData = addIntToData(phaseData, phase_data_string.azimuth_residual)
    phaseData = addFloatToData(phaseData, phase_data_string.travel_time_residual)
    phaseData = addIntToData(phaseData, phase_data_string.location_weight)
    phaseData = addIntToData(phaseData, phase_data_string.epicenter_distance)
    phaseData = addIntToData(phaseData, phase_data_string.epicenter_to_station_azimuth)

    return phaseData

def createMainHeaderList(main_header_string):
    """ 
    Method that creates Main Header list from main header string object.

    Args:
        main_header_string: Main header string object from nordicStringClassModule

    Returns:
        The generated list
    """

    mainData = ()

    mainData = addIntToData(mainData, main_header_string.event_id)
    mainData = addDateToData(mainData, main_header_string.date)
    mainData = addIntToData(mainData, main_header_string.hour)
    mainData = addIntToData(mainData, main_header_string.minute)
    mainData = addFloatToData(mainData, main_header_string.second)
    mainData = addStringToData(mainData, main_header_string.location_model)
    mainData = addStringToData(mainData, main_header_string.distance_indicator)
    mainData = addStringToData(mainData, main_header_string.event_desc_id)
    mainData = addFloatToData(mainData, main_header_string.epicenter_latitude)
    mainData = addFloatToData(mainData, main_header_string.epicenter_longitude)
    mainData = addFloatToData(mainData, main_header_string.depth)
    mainData = addStringToData(mainData, main_header_string.depth_control)
    mainData = addStringToData(mainData, main_header_string.locating_indicator)
    mainData = addStringToData(mainData, main_header_string.epicenter_reporting_agency)
    mainData = addIntToData(mainData, main_header_string.stations_used)
    mainData = addFloatToData(mainData, main_header_string.rms_time_residuals)
    mainData = addFloatToData(mainData, main_header_string.magnitude_1)
    mainData = addStringToData(mainData, main_header_string.type_of_magnitude_1)
    mainData = addStringToData(mainData, main_header_string.magnitude_reporting_agency_1)
    mainData = addFloatToData(mainData, main_header_string.magnitude_2)
    mainData = addStringToData(mainData, main_header_string.type_of_magnitude_2)
    mainData = addStringToData(mainData, main_header_string.magnitude_reporting_agency_2)
    mainData = addFloatToData(mainData, main_header_string.magnitude_3)
    mainData = addStringToData(mainData, main_header_string.type_of_magnitude_3)
    mainData = addStringToData(mainData, main_header_string.magnitude_reporting_agency_3)

    return mainData

def createMacroseismicHeaderList(macroseismic_header_string):
    """ 
    Method that creates Macroseismic Heder list from macroseismic header string object.

    Args:
        macroseismic_header_string: macroseismic header string object from nordicStringClassModule

    Returns:
        The generated list
    """

    macroData = ()

    macroData = addIntToData(macroData, macroseismic_header_string.event_id)
    macroData = addStringToData(macroData, macroseismic_header_string.description)
    macroData = addStringToData(macroData, macroseismic_header_string.diastrophism_code)
    macroData = addStringToData(macroData, macroseismic_header_string.tsunami_code)
    macroData = addStringToData(macroData, macroseismic_header_string.seiche_code)
    macroData = addStringToData(macroData, macroseismic_header_string.cultural_effects)
    macroData = addStringToData(macroData, macroseismic_header_string.unusual_effects)
    macroData = addIntToData(macroData, macroseismic_header_string.maximum_observed_intensity)
    macroData = addStringToData(macroData, macroseismic_header_string.maximum_intensity_qualifier)
    macroData = addStringToData(macroData, macroseismic_header_string.intensity_scale)
    macroData = addFloatToData(macroData, macroseismic_header_string.macroseismic_latitude)
    macroData = addFloatToData(macroData, macroseismic_header_string.macroseismic_longitude)
    macroData = addFloatToData(macroData, macroseismic_header_string.macroseismic_magnitude)
    macroData = addStringToData(macroData, macroseismic_header_string.type_of_magnitude)
    macroData = addFloatToData(macroData, macroseismic_header_string.logarithm_of_radius)
    macroData = addFloatToData(macroData, macroseismic_header_string.logarithm_of_area_1)
    macroData = addIntToData(macroData, macroseismic_header_string.bordering_intensity_1)
    macroData = addFloatToData(macroData, macroseismic_header_string.logarithm_of_area_2)
    macroData = addIntToData(macroData, macroseismic_header_string.bordering_intensity_2)
    macroData = addStringToData(macroData, macroseismic_header_string.quality_rank)
    macroData = addStringToData(macroData, macroseismic_header_string.reporting_agency)

    return macroData

def createCommentHeaderList(comment_header_string):
    """ 
    Method that creates comment header list from comment header string object.

    Args:
        comment_header_string: comment header string object from nordicStringClassModule

    Returns:
        The generated list
    """

    commentData = () 

    commentData = addIntToData(commentData, comment_header_string.event_id)
    commentData = addStringToData(commentData, comment_header_string.h_comment)

    return commentData

def createErrorHeaderList(error_header_string):
    """ 
    Method that creates Error header list from error header string object.

    Args:
        error_header_string: Error header string object from nordicStringClassModule

    Returns:
        The generated list
    """

    errorData = ()

    errorData = addIntToData(errorData, error_header_string.header_id)
    errorData = addIntToData(errorData, error_header_string.gap)
    errorData = addFloatToData(errorData, error_header_string.second_error)
    errorData = addFloatToData(errorData, error_header_string.epicenter_latitude_error)
    errorData = addFloatToData(errorData, error_header_string.epicenter_longitude_error)
    errorData = addFloatToData(errorData, error_header_string.depth_error)
    errorData = addFloatToData(errorData, error_header_string.magnitude_error)

    return errorData

def createWaveformHeaderList(waveform_header_string):
    """ 
    Method that creates waveform header list from waveform header string object.

    Args:
        waveform_header_string: Waveform header string object from nordicStringClassModule

    Returns:
        The generated list
    """

    waveData = ()

    waveData = addIntToData(waveData, waveform_header_string.event_id)
    waveData = addStringToData(waveData, waveform_header_string.waveform_info)

    return waveData

def queryNordicEventPhaseData(cur, event_id):
    """
    Method that creates the NordicEventPhaseData object from the database with event id of event_id

    Args:
        cur (psycopg2.connect.cursor): cursor object that makes the queries
        event_id (int): event id of the event that needs to be made

    Returns:
        Phase data object 
    """
    phase_data = []

    cur.execute("SELECT id, event_id, station_code, sp_instrument_type, sp_component, quality_indicator, phase_type, weight, first_motion, time_info, hour, minute, second, signal_duration, max_amplitude, max_amplitude_period, back_azimuth, apparent_velocity, signal_to_noise, azimuth_residual, travel_time_residual, location_weight, epicenter_distance, epicenter_to_station_azimuth FROM nordic_phase_data WHERE event_id = %s", (event_id,))

    query_answers = cur.fetchall()

    for answer in query_answers:
        phase_data.append(NordicPhaseData(answer))

    return phase_data

def queryNordicEventMainHeaders(cur, event_id):
    """
    Method that creates the NordicEventMainHeader object from the database with event id of event_id

    Args:
        cur (psycopg2.connect.cursor): cursor object that makes the queries
        event_id (int): event id of the event that needs to be made

    Returns:
        Main header object
    """

    headers = []

    cur.execute("SELECT id, event_id, date, hour, minute, second, location_model, distance_indicator, event_desc_id, epicenter_latitude, epicenter_longitude, depth, depth_control, locating_indicator, epicenter_reporting_agency, stations_used, rms_time_residuals, magnitude_1, type_of_magnitude_1, magnitude_reporting_agency_1, magnitude_2, type_of_magnitude_2, magnitude_reporting_agency_2, magnitude_3, type_of_magnitude_3, magnitude_reporting_agency_3 FROM nordic_header_main WHERE event_id = %s", (event_id,))

    query_answers = cur.fetchall()

    for answer in query_answers:
        headers.append(NordicHeaderMain(answer))

    return headers

def queryNordicEventMacroseismicHeaders(cur, event_id):
    """
    Method that creates the NordicMacroseimicHeader object from the database with event id of event_id

    Args:
        cur (psycopg2.connect.cursor): cursor object that makes the queries
        event_id (int): event id of the event that needs to be made

    Returns:
        Macroseismic header object
    """

    headers = []

    cur.execute("SELECT id, event_id, description, diastrophism_code, tsunami_code, seiche_code, cultural_effects, unusual_effects, maximum_observed_intensity, maximum_intensity_qualifier, intensity_scale, macroseismic_latitude, macroseismic_longitude, macroseismic_magnitude, type_of_magnitude, logarithm_of_radius, logarithm_of_area_1, bordering_intensity_1, logarithm_of_area_2, bordering_intensity_2, quality_rank, reporting_agency FROM nordic_header_macroseismic WHERE event_id = %s", (event_id,))

    query_answers = cur.fetchall()

    for answer in query_answers:
        headers.append(NordicHeaderMacroseismic(answer))

    return headers

def queryNordicEventCommentHeaders(cur, event_id):
    """
    Method that creates the NordicCommentHeader object from the database with event id of event_id

    Args:
        cur (psycopg2.connect.cursor): cursor object that makes the queries
        event_id (int): event id of the event that needs to be made

    Returns:
        Comment header object 
    """

    headers = []

    cur.execute("SELECT id, event_id, h_comment FROM nordic_header_comment WHERE event_id = %s", (event_id,))

    query_answers = cur.fetchall()

    for answer in query_answers:
        headers.append(NordicHeaderComment(answer))

    return headers

def queryNordicEventErrorHeaders(cur, event_id):
    """
    Method that creates the NordicErrorHeader object from the database with event id of event_id


    Args:
        cur (psycopg2.connect.cursor): cursor object that makes the queries
        event_id (int): event id of the event that needs to be made

    Returns:
        Error Header object 
    """

    headers = []

    cur.execute("SELECT nordic_header_error.id, nordic_header_error.header_id, gap, second_error, epicenter_latitude_error, epicenter_longitude_error, depth_error, magnitude_error FROM nordic_header_error INNER JOIN nordic_header_main ON nordic_header_main.id = nordic_header_error.header_id WHERE nordic_header_main.event_id = %s", (event_id,))
    query_answers = cur.fetchall()

    for answer in query_answers:
        headers.append(NordicHeaderError(answer))

    return headers

def queryNordicEventWaveformHeaders(cur, event_id):
    """
    Method that creates the NordicWaveformHeader object from the database with event id of event_id

    Args:
        cur (psycopg2.connect.cursor): cursor object that makes the queries
        event_id (int): event id of the event that needs to be made

    Returns:
        Waveform header object
    """

    headers = []

    cur.execute("SELECT id, event_id, waveform_info FROM nordic_header_waveform WHERE event_id = %s", (event_id,))

    query_answers = cur.fetchall()

    for answer in query_answers:
        headers.append(NordicHeaderWaveform(answer))

    return headers

def createNordicEvent(nordic_string_event):
    """
    Method that creates a nordicEvent object from nordicEventString object

    Args:
        nordic_string_event: NordicEventString object

    returns:
        A NordicEvent object
    """
    headers = {}
    phase_data = []

    for h in nordic_string_event.headers:
        if h.tpe == 1:
            headers[1].append(createMainHeaderList(h))
        elif h.tpe == 2:
            headers[2].append(createMacroseismicHeaderList(h))
        elif h.tpe == 3:
            headers[3].append(createCommentHeaderList(h))
        elif h.tpe == 5:
            headers[5].append(createErrorHeaderList(h))
        elif h.tpe == 6:
            headers[6].append(createWaveformHeaderList(h))

    for d in phase_data:
        phase_data.append(createPhaseDataList(d))

    nordic_event = NordicEvent(headers, phase_data)

    return nordic_event

def readNordicEvent(cur, event_id):
    """
    Method that reads the nordic event from the database and creates a NordicEvent object from the queries.

    Args:
        cur (psycopg2.connect.cursor): cursor object that makes the queries
        event_id (int): event id of the event that needs to be made

    Returns:
        A NordicEvent object
    """
    headers = {}
    phase_data = []

    cur.execute("SELECT id from nordic_event WHERE id = %s", (event_id,))
    ans = cur.fetchone()

    if not ans:
        logging.error("Event with id {0} does not exist!".format(event_id))
        return None
    
    headers[1] = queryNordicEventMainHeaders(cur, event_id)
    headers[2] = queryNordicEventMacroseismicHeaders(cur, event_id)
    headers[3] = queryNordicEventCommentHeaders(cur, event_id)
    headers[5] = queryNordicEventErrorHeaders(cur, event_id)
    headers[6] = queryNordicEventWaveformHeaders(cur, event_id)

    phase_data = queryNordicEventPhaseData(cur, event_id)

    nordic_event = NordicEvent(headers, phase_data)

    return nordic_event
