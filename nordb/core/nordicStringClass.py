class NordicEvent:
    """
    Class for represeting Nordic Event with all the values in it being string. It can contain erroneus information which can be found by running it through nordicValidation.

    Args:
        headers (NordicHeader[]): A headers array which contains all the headers of the event in their respective container formats
        data (NordicData[]): A data array which contains all the phase data information of the event
        event_type (str): a event type string which identifies if the event is for example automatic event information or final event information
        author_id (str): author of the nordic event in a three letter format
        locating_program (str): string for the locating program used to locate the event

    Attributes:
        event_id (str): Id of the event in the database. Defaults to -1 but will be added later
        root_id (str) Id of the root event in the database. Defaults to -1 but will be added later
        headers (NordicHeader[]): A headers array which contains all the headers of the event in their respective container formats
        data (NordicData[]): A data array which contains all the phase data information of the event
        event_type (str): a event type string which identifies if the event is for example automatic event information or final event information
        author_id (str): author of the nordic event in a three letter format
        locating_program (str): string for the locating program used to locate the event
       
    """
    def __init__(self, headers, data, event_type, author_id, locating_program):
        self.event_id = "-1"
        self.root_id = "-1"
        self.headers = headers
        self.data = data
        self.event_type = event_type.strip()
        self.author_id = author_id.strip()
        self.locating_program = locating_program.strip()

class NordicHeader:
    """
    A parent class for header lines of the nordic file. Other headers will inherit this class.
    
    Args:
        tpe (int): type of the header: 1 - main header, 2 - macroseismic header, 3 - comment header, 5 - error header, 6 - waveform header

    Attributes:
        tpe (int): type of the header: 1 - main header, 2 - macroseismic header, 3 - comment header, 5 - error header, 6 - waveform header

    """
    def __init__(self, tpe):
        self.tpe = tpe

#Class for nordic data lines of the nordic file.
class NordicData:
    """
    Class for nordic phase data line. Contains the raw data of the nordic file without any quarantees that the data is valid. This will be validated with the nordicValidation library afterwards.

    Args:
        data (str): phase data string from which all data is cut from.
       
    Attributes:
        event_id (str): event id of the relevant Nordic Event
        station_code (str): station code for the station that observed this line
        sp_instrument_type (str): type of the observing instrument
        quality_indicator (str): quality indicator of the phase data line
        phase_type (str): the type of the phase 
        weight (str): the actual weight of the observation
        first motion (str): the direction of the wave
        time_info (str): str that tells which day the observation was made
        hour (str): the hour when the observation was made
        minute (str): the minute when the observation was made
        second (str): the second when the observation was made
        signal_duration (str): the duration of the signal
        max_amplitude (str): maximum amplitude of the signal during its duration
        max_amplitude_period (str): period for the maximum amplitude of the signal
        back_azimuth (str): the back azimuth of the observation
        apparent_velocity (str): apparent velocity for the signal
        signal_to_noise (str): signal to noise ratio of the signal
        azimuth_residual (str): residual of the azimuth of the location
        travel_time_residual (str): the travel time residual of the signal
        location_weight (str): the weight of the location for calculations
        epicenter_distance (str): distance from the epicenter to the station
        epicenter_to_station_azimuth (str): the azimuth of the epicenter to station
    """
    def __init__(self, data):
        self.event_id = "-1"
        self.station_code = data[1:5].strip()
        self.sp_instrument_type = data[6].strip()
        self.sp_component = data[7].strip()
        self.quality_indicator = data[9].strip()
        self.phase_type = data[10:14].strip()
        self.weight = data[14].strip()
        self.first_motion = data[16].strip()
        self.time_info = data[17].strip()
        self.hour = data[18:20].strip()
        self.minute = data[20:22].strip()
        self.second = data[23:28].strip()
        self.signal_duration = data[29:33].strip()
        self.max_amplitude = data[34:40].strip()
        self.max_amplitude_period = data[41:45].strip()
        self.back_azimuth = data[46:52].strip()
        self.apparent_velocity = data[52:56].strip()
        self.signal_to_noise = data[56:60].strip()
        self.azimuth_residual = data[60:63].strip()
        self.travel_time_residual = data[63:68].strip()
        self.location_weight = data[68:70].strip()
        self.epicenter_distance = data[70:75].strip()
        self.epicenter_to_station_azimuth = data[76:79].strip()

class NordicHeaderMain(NordicHeader):
    """
    Class for nordic header line of type 1. Contains main information from the event. Inherits class Nordic Header. Contains the raw data of the nordic file without any quarantees that the data is valid. This will be validated with the nordicValidation library afterwards.

    Args:
        header (str): header data string from which all data is cut from

    Attributes:
        o_string (str): The header string of the header. Used in user header comparison
        date (str): date of the event
        hour (str): hour when the event occurred
        minute (str): minute when the event occurred
        second (str): seconc when the event occurred
        location_model (str): location model used in locating the event
        distance_indicator (str): distance indicator of the event
        event_desc_id (str): the description id of the event
        epicenter_latitude (str): latitude of the event
        epicenter_longitude (str): longitude of the event
        depth (str): depth of the event
        depth_control (str): depth cotrol flag
        locating_indicator (str): locating indicator of the event
        epicenter_reporting_agency (str): agency that reported the event
        stations_used (str): stations used in the locating process
        rms_time_residuals (str): rms of time residuals
        magnitude_1 (str): magnitude from the first magnitude reporting agency
        type_of_magnitude_1 (str): type of first magnitude 
        magnitude_reporting_agency_1 (str): the reporting agency of the first magnitude
        magnitude_2 (str): magnitude from the second magnitude reporting agency
        type_of_magnitude_2 (str): type of the second magnitude 
        magnitude_reporting_agency_2 (str):  the reporting agency of the second magnitude
        magnitude_3 (str): magnitude from the third magnitude reporting agency
        type_of_magnitude_3 (str): type of the second magnitude
        magnitude_reporting_agency_3 (str): the reporting agency of the third magnitude
    """
    def __init__(self, header):
        NordicHeader.__init__(self, 1)
        self.o_string = header
        self.event_id = "-1"
        self.date = header[1:5] + "-" + header[6:8] + "-" + header[8:10]
        self.hour = header[11:13].strip()
        self.minute = header[13:15].strip()
        self.second = header[16:20].strip()
        self.location_model = header[20].strip()
        self.distance_indicator = header[21].strip()
        self.event_desc_id = header[22].strip()
        self.epicenter_latitude = header[23:30].strip()
        self.epicenter_longitude = header[30:38].strip()
        self.depth = header[38:43].strip()
        self.depth_control = header[43].strip()
        self.locating_indicator = header[44].strip()
        self.epicenter_reporting_agency = header[45:48] .strip()
        self.stations_used = header[48:51].strip()
        self.rms_time_residuals = header[51:55].strip()
        self.magnitude_1 = header[56:59].strip()
        self.type_of_magnitude_1 = header[59].strip()
        self.magnitude_reporting_agency_1 = header[60:63].strip()
        self.magnitude_2 = header[64:67].strip()
        self.type_of_magnitude_2 = header[67].strip()
        self.magnitude_reporting_agency_2 = header[68:71].strip()
        self.magnitude_3 = header[72:75].strip()
        self.type_of_magnitude_3 = header[75].strip()
        self.magnitude_reporting_agency_3 = header[76:79].strip()

#Class for the nordic header line of type 2. Contains macroseismic information of the event
class NordicHeaderMacroseismic(NordicHeader):
    """
    Class for nordic header line of type 2. Contains macroseismic information from the event. Inherits class Nordic Header. Contains the raw data of the nordic file without any quarantees that the data is valid. This will be validated with the nordicValidation library afterwards.

    Args:
        header (str): header data string from which all data is cut from

    Attributes:
        description (str): description of the event
        diastrophism_code (str): diastrophism code of the event
        tsunami_code (str): tsunami code of the event
        seiche_code (str): seiche code of the event
        cultural_effects (str): cultural effetcs code of the event
        unusual_effects (str): unusual effetcs code of the event
        maximum_observed_intensity (str): maximum observed intensity of the event
        maximum_intensity_qualifier (str): maximum intensity qualifier of the event
        intensity_scale (str): intensity scale of the event
        macroseismic_latitude (str): macroseismic latitude of the event
        macroseismic_longitude (str): macroseismic longitude of the event
        macroseismic_magnitude (str): macroseismic magnitude of the event
        type_of_magnitude (str): type of magnitude
        logarithm_of_radius (str): logarithm of radius
        logarithm_of_area_1 (str): logarithm of area 1 
        bordering_intensity_1 (str): bordering intensity 1
        logarithm_of_area_2 (str): logarithm of area 2
        bordering_intensity_2 (str): bordering intensity 2
        quality_rank (str): quality rank of the header
        reporting_agency (str): reporting agency
        event_id (str): event id of relevant nordic event
    """
    def __init__(self, header):
        NordicHeader.__init__(self, 2)  
        self.description = header[5:20].strip()
        self.diastrophism_code = header[22].strip()
        self.tsunami_code = header[23].strip()
        self.seiche_code = header[24].strip()
        self.cultural_effects = header[25].strip()
        self.unusual_effects = header[26].strip()
        self.maximum_observed_intensity = header[27:29].strip()
        self.maximum_intensity_qualifier = header[29].strip()
        self.intensity_scale = header[30:32].strip()
        self.macroseismic_latitude = header[33:39].strip()
        self.macroseismic_longitude = header[40:47].strip()
        self.macroseismic_magnitude = header[48:51].strip()
        self.type_of_magnitude = header[52].strip()
        self.logarithm_of_radius = header[52:56].strip()
        self.logarithm_of_area_1 = header[56:61].strip()
        self.bordering_intensity_1 = header[61:63].strip()
        self.logarithm_of_area_2 = header[63:68].strip()
        self.bordering_intensity_2 = header[68:70].strip()
        self.quality_rank = header[72].strip()
        self.reporting_agency = header[72:75].strip()
        self.event_id = "-1"

class NordicHeaderComment(NordicHeader):
    """
    Class for the nordic header line of type 3. Contains comments of the header file. Inherits class Nordic Header. Contains the raw data of the nordic file without any quarantees that the data is valid. This will be validated with the nordicValidation library afterwards.

    Args:
        header (str): header data string from which all data is cut from

    Attributes:
        h_comment (str): the comment in the header
        event_id (str): event id of relevant nordic event
    """
    def __init__(self, header):
        NordicHeader.__init__(self, 3)
        self.h_comment = header[1:79].strip()
        self.event_id = "-1"
#Class for the nordic header line of type 5. Contains error information of the main header
class NordicHeaderError(NordicHeader):
    """
    Class for the nordic header line of type 5. Contains error header file. Inherits class Nordic Header. Contains the raw data of the nordic file without any quarantees that the data is valid. This will be validated with the nordicValidation library afterwards.

    Args:
        header (str): header data string from which all data is cut from

    Attributes:
        gap (str): Azimuthal gap of the event
        second_error (str): margin of error in the main headers second
        epicenter_latitude_error (str): margin of error in epicenter latitude 
        epicenter_longitude_error (str): margin of error in epicenter longitude
        depth_error (str): margin of error in depth evaluation
        magnitude_error (str): margin of error in magnitude
        header_id (str): id of the main header where this error header refers to
    """
    def __init__(self, header):
        NordicHeader.__init__(self, 5)
        self.gap = header[5:8].strip()
        self.second_error = header[16:20].strip()
        self.epicenter_latitude_error = header[24:30].strip()
        self.epicenter_longitude_error = header[31:38].strip()
        self.depth_error = header[40:43].strip()
        self.magnitude_error = header[56:59].strip()
        self.header_id = "-1"

class NordicHeaderWaveform(NordicHeader):
    """
    Class for the nordic header line of type 6. Contains waveform information of the header file. Inherits class Nordic Header. Contains the raw data of the nordic file without any quarantees that the data is valid. This will be validated with the nordicValidation library afterwards.

    Args:
        header (str): header data string from which all data is cut from

    Attributes:
        waveform_info (str): the waveform location of the event
        event_id (str): event id of relevant nordic event
    """

    def __init__(self, header):
        NordicHeader.__init__(self, 6)
        self.event_id = "-1"
        self.waveform_info = header[1:79].strip()

