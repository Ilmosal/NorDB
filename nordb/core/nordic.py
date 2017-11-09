from datetime import date

class NordicEvent:
    """
    Container object of nordic event information
    """
    def __init__(self, headers, data):
        self.headers = headers
        self.data = data
    
class NordicData:
    header_type = 7
    STATION_CODE = 0
    SP_INSTRUMENT_TYPE = 1
    SP_COMPONENT = 2
    QUALITY_INDICATOR = 3 
    PHASE_TYPE = 4
    WEIGHT = 5
    FIRST_MOTION = 6
    TIME_INFO = 7
    HOUR = 8
    MINUTE = 9 
    SECOND = 10
    SIGNAL_DURATION = 11
    MAX_AMPLITUDE = 12 
    MAX_AMPLITUDE_PERIOD = 13
    BACK_AZIMUTH = 14
    APPARENT_VELOCITY = 15
    SIGNAL_TO_NOISE = 16
    AZIMUTH_RESIDUAL = 17
    TRAVEL_TIME_RESIDUAL = 18
    LOCATION_WEIGHT = 19
    EPICENTER_DISTANCE = 20
    EPICENTER_TO_STATION_AZIMUTH = 21
    EVENT_ID = 22

    def __init__(self, data):
        self.data = data
 
class NordicMain:
    header_type = 1
    DATE = 0
    HOUR = 1
    MINUTE = 2
    SECOND = 3
    LOCATION_MODEL = 4
    DISTANCE_INDICATOR = 5
    EVENT_DESC_ID = 6
    EPICENTER_LATITUDE = 7
    EPICENTER_LONGITUDE = 8
    DEPTH = 9 
    DEPTH_CONTROL = 10
    LOCATING_INDICATOR = 11
    EPICENTER_REPORTING_AGENCY = 12
    STATIONS_USED = 13
    RMS_TIME_RESIDUALS = 14
    MAGNITUDE_1 = 15
    TYPE_OF_MAGNITUDE_1 = 16
    MAGNITUDE_REPORTING_AGENCY_1 = 17
    MAGNITUDE_2 = 18
    TYPE_OF_MAGNITUDE_2 = 19
    MAGNITUDE_REPORTING_AGENCY_2 = 20
    MAGNITUDE_3 = 21
    TYPE_OF_MAGNITUDE_3 = 22
    MAGNITUDE_REPORTING_AGENCY_3 = 23
    EVENT_ID = 24
    O_STRING = 25

    def __init__(self, header):
        self.header = header
 
class NordicMacroseismic:
    header_type = 2
    DESCRIPTION = 0
    DIASTROPHISM_CODE = 1
    TSUNAMI_CODE = 2
    SEICHE_CODE = 3 
    CULTURAL_EFFECTS = 4
    UNUSUAL_EFFECTS = 5
    MAXIMUM_OBSERVED_INTENSITY = 6
    MAXIMUM_INTENSITY_QUALIFIER = 7
    INTENSITY_SCALE = 8
    MACROSEISMIC_LATITUDE = 9
    MACROSEISMIC_LONGITUDE = 10
    MACROSEISMIC_MAGNITUDE = 11
    TYPE_OF_MAGNITUDE = 12
    LOGARITHM_OF_RADIUS = 13
    LOGARITHM_OF_AREA_1 = 14
    BORDERING_INTENSITY_1 = 15
    LOGARITHM_OF_AREA_2 = 16
    BORDERING_INTENSITY_2 = 17
    QUALITY_RANK = 18
    REPORTING_AGENCY = 19
    EVENT_ID = 20

    def __init__(self, header):
        self.header = header
 
class NordicComment:
    header_type = 3
    H_COMMENT = 0
    EVENT_ID = 1

    def __init__(self, header):
        self.header = header

class NordicError:
    header_type = 5
    GAP = 0
    SECOND_ERROR = 1
    EPICENTER_LATITUDE_ERROR = 2
    EPICENTER_LONGITUDE_ERROR = 3
    DEPTH_ERROR = 4
    MAGNITUDE_ERROR = 5
    HEADER_ID = 6

    def __init__(self, header, header_pos):
        self.header = header
        self.header_pos = header_pos

    
class NordicWaveform:
    header_type = 6
    WAVEFORM_INFO = 0
    EVENT_ID = 1

    def __init__(self, header):
        self.header = header


def createStringMainHeader(header):
    """
    Function that creates NordicMain list with values being strings
    
    Args:
        header (str): string from where the data is parsed from

    Returns:
        list of values parsed from header
    """

    nordic_main = [None]*26

    nordic_main[NordicMain.DATE] = header[1:5] + "-" + header[6:8] + "-" + header[8:10]
    nordic_main[NordicMain.HOUR ] = header[11:13].strip()
    nordic_main[NordicMain.MINUTE ] = header[13:15].strip()
    nordic_main[NordicMain.SECOND ] = header[16:20].strip()
    nordic_main[NordicMain.LOCATION_MODEL ] = header[20].strip()
    nordic_main[NordicMain.DISTANCE_INDICATOR ] = header[21].strip()
    nordic_main[NordicMain.EVENT_DESC_ID ] = header[22].strip()
    nordic_main[NordicMain.EPICENTER_LATITUDE ] = header[23:30].strip()
    nordic_main[NordicMain.EPICENTER_LONGITUDE ] = header[30:38].strip()
    nordic_main[NordicMain.DEPTH ] = header[38:43].strip()
    nordic_main[NordicMain.DEPTH_CONTROL ] = header[43].strip()
    nordic_main[NordicMain.LOCATING_INDICATOR ] = header[44].strip()
    nordic_main[NordicMain.EPICENTER_REPORTING_AGENCY ] = header[45:48].strip()
    nordic_main[NordicMain.STATIONS_USED ] = header[48:51].strip()
    nordic_main[NordicMain.RMS_TIME_RESIDUALS ] = header[51:55].strip()
    nordic_main[NordicMain.MAGNITUDE_1 ] = header[56:59].strip()
    nordic_main[NordicMain.TYPE_OF_MAGNITUDE_1 ] = header[59].strip()
    nordic_main[NordicMain.MAGNITUDE_REPORTING_AGENCY_1 ] = header[60:63].strip()
    nordic_main[NordicMain.MAGNITUDE_2 ] = header[64:67].strip()
    nordic_main[NordicMain.TYPE_OF_MAGNITUDE_2 ] = header[67].strip()
    nordic_main[NordicMain.MAGNITUDE_REPORTING_AGENCY_2 ] = header[68:71].strip()
    nordic_main[NordicMain.MAGNITUDE_3 ] = header[71:75].strip()
    nordic_main[NordicMain.TYPE_OF_MAGNITUDE_3 ] = header[75].strip()
    nordic_main[NordicMain.MAGNITUDE_REPORTING_AGENCY_3 ] = header[76:79].strip()
    nordic_main[NordicMain.O_STRING] = header

    return NordicMain(nordic_main)

def createStringMacroseismicHeader(header): 
    """
    Function that creates NordicMacroseismic list with values being strings
    
    Args:
        header (str): string from where the data is parsed from

    Returns:
        list of values parsed from header

    """
    nordic_macroseismic = [None]*20

    nordic_macroseismic[NordicMacroseismic.DESCRIPTION] = header[5:20].strip()
    nordic_macroseismic[NordicMacroseismic.DIASTROPHISM_CODE] = header[22].strip()
    nordic_macroseismic[NordicMacroseismic.TSUNAMI_CODE] = header[23].strip()
    nordic_macroseismic[NordicMacroseismic.SEICHE_CODE] = header[24].strip()
    nordic_macroseismic[NordicMacroseismic.CULTURAL_EFFECTS] = header[25].strip()
    nordic_macroseismic[NordicMacroseismic.UNUSUAL_EFFECTS] = header[26].strip()
    nordic_macroseismic[NordicMacroseismic.MAXIMUM_OBSERVED_INTENSITY] = header[27:29].strip()
    nordic_macroseismic[NordicMacroseismic.MAXIMUM_INTENSITY_QUALIFIER] = header[29].strip()
    nordic_macroseismic[NordicMacroseismic.INTENSITY_SCALE] = header[30:32].strip()
    nordic_macroseismic[NordicMacroseismic.MACROSEISMIC_LATITUDE] = header[33:39].strip()
    nordic_macroseismic[NordicMacroseismic.MACROSEISMIC_LONGITUDE] = header[40:47].strip()
    nordic_macroseismic[NordicMacroseismic.MACROSEISMIC_MAGNITUDE] = header[48:51].strip()
    nordic_macroseismic[NordicMacroseismic.TYPE_OF_MAGNITUDE] = header[51].strip()
    nordic_macroseismic[NordicMacroseismic.LOGARITHM_OF_RADIUS] = header[52:56].strip()
    nordic_macroseismic[NordicMacroseismic.LOGARITHM_OF_AREA_1] = header[56:61].strip()
    nordic_macroseismic[NordicMacroseismic.BORDERING_INTENSITY_1] = header[61:63].strip()
    nordic_macroseismic[NordicMacroseismic.LOGARITHM_OF_AREA_2] = header[63:68].strip()
    nordic_macroseismic[NordicMacroseismic.BORDERING_INTENSITY_2] = header[68:70].strip()
    nordic_macroseismic[NordicMacroseismic.QUALITY_RANK] = header[72].strip()
    nordic_macroseismic[NordicMacroseismic.REPORTING_AGENCY] = header[72:75].strip()

    return NordicMacroseismic(nordic_macroseismic)

def createStringCommentHeader(header):
    """
    Function that creates Nordic comment list with values being strings

    Args:
        header (str): string from where the data is parsed from

    Returns:
        list of values parsed from header
    """

    nordic_comment = [None]

    nordic_comment[NordicComment.H_COMMENT] = header[1:79].strip()

    return NordicComment(nordic_comment)


def createStringErrorHeader(header, h_id):
    """
    Function that creates Nordic error list with values being strings

    Args:
        header (str): string from where the data is parsed from

    Returns:
        list of values parsed from header
    """
    nordic_error = [None]*6

    nordic_error[NordicError.GAP] = header[5:8].strip()
    nordic_error[NordicError.SECOND_ERROR] = header[16:20].strip()
    nordic_error[NordicError.EPICENTER_LATITUDE_ERROR] = header[24:30].strip()
    nordic_error[NordicError.EPICENTER_LONGITUDE_ERROR] = header[31:38].strip()
    nordic_error[NordicError.DEPTH_ERROR] = header[40:43].strip()
    nordic_error[NordicError.MAGNITUDE_ERROR] = header[56:59].strip()
   
    return NordicError(nordic_error, h_id)

def createStringWaveformHeader(header):
    """
    Function that creates Nordic waveform list with values being strings

    Args:
        header (str): string from where the data is parsed from

    Returns:
        list of values parsed from header
    """

    nordic_waveform = [None]

    nordic_waveform[NordicWaveform.WAVEFORM_INFO] = header[1:79].strip()

    return NordicWaveform(nordic_waveform)

def createStringPhaseData(data):
    """
    Function that creates Nordic phase data list with values being strings

    Args:
        data (str): string from where the data is parsed from

    Returns:
        list of values parsed from data
    """
    phase_data = [None]*22

    phase_data[NordicData.STATION_CODE] = data[1:5].strip()
    phase_data[NordicData.SP_INSTRUMENT_TYPE] = data[6].strip()
    phase_data[NordicData.SP_COMPONENT] = data[7].strip()
    phase_data[NordicData.QUALITY_INDICATOR] = data[9].strip()
    phase_data[NordicData.PHASE_TYPE] = data[10:14].strip()
    phase_data[NordicData.WEIGHT] = data[14].strip()
    phase_data[NordicData.FIRST_MOTION] = data[16].strip()
    phase_data[NordicData.TIME_INFO] = data[17].strip()
    phase_data[NordicData.HOUR] = data[18:20].strip()
    phase_data[NordicData.MINUTE] = data[20:22].strip()
    phase_data[NordicData.SECOND] = data[23:28].strip()
    phase_data[NordicData.SIGNAL_DURATION] = data[29:33].strip()
    phase_data[NordicData.MAX_AMPLITUDE] = data[34:40].strip()
    phase_data[NordicData.MAX_AMPLITUDE_PERIOD] = data[41:45].strip()
    phase_data[NordicData.BACK_AZIMUTH] = data[46:52].strip()
    phase_data[NordicData.APPARENT_VELOCITY] = data[52:56].strip()
    phase_data[NordicData.SIGNAL_TO_NOISE] = data[56:60].strip()
    phase_data[NordicData.AZIMUTH_RESIDUAL] = data[60:63].strip()
    phase_data[NordicData.TRAVEL_TIME_RESIDUAL] = data[63:68].strip()
    phase_data[NordicData.LOCATION_WEIGHT] = data[68:70].strip()
    phase_data[NordicData.EPICENTER_DISTANCE] = data[70:75].strip()
    phase_data[NordicData.EPICENTER_TO_STATION_AZIMUTH] = data[76:79].strip()

    return NordicData(phase_data)

def nordicStringEvent2NordicEvent(nordic_event):
    """
    Function that turns a validated nordic string event to nordic event
    """

def returnInt(integer):
    """
    Function that casts integer to a int or None if it's empty.

    Args:
        integer(str): integer or empty string

    Returns:
        Integer or None
    """
    try:
        return int(integer)
    except:
        return None

def returnDate(date_s):
    """
    Function that casts date_s to a date or None if it's empty.

    Args:
        date_s(str): date or empty string
        
    Returns:
        Date or None
    """
    try:
        return date(year=int(date_s[:4]), month=int(date_s[5:7]), day=int(date_s[8:]))
    except ValueError:
        return None

def returnFloat(float_s):
    """
    Function that casts float_s to a integer or None if it's empty.

    Args:
        float_s(str): float or empty string

    Returns:
        Float or None
    """
    try:
        return float(float_s)
    except:
        return None

def returnString(string):
    """
    Function that returns string or None if the string is empty.

    Args:
        string(str): the string value
    
    Args:
        string or None
    """
    if string == "":
        return None
    else:
        return string

def mainString2Main(main_string, event_id):
    """
    Function that converts all values in main string list into main list with correct value types.

    Args:
        main_string(str []): list of all string valus of the main header
        event_id (int): event_id of the main header

    Returns:
        List of all main info in correct order
    """
    main = [None]*25

    main[NordicMain.DATE]                           = returnDate    (main_string.header[NordicMain.DATE])
    main[NordicMain.HOUR]                           = returnInt     (main_string.header[NordicMain.HOUR])
    main[NordicMain.MINUTE]                         = returnInt     (main_string.header[NordicMain.MINUTE])
    main[NordicMain.SECOND]                         = returnFloat   (main_string.header[NordicMain.SECOND])
    main[NordicMain.LOCATION_MODEL]                 = returnString  (main_string.header[NordicMain.LOCATION_MODEL])
    main[NordicMain.DISTANCE_INDICATOR]             = returnString  (main_string.header[NordicMain.DISTANCE_INDICATOR])
    main[NordicMain.EVENT_DESC_ID]                  = returnString  (main_string.header[NordicMain.EVENT_DESC_ID])
    main[NordicMain.EPICENTER_LATITUDE]             = returnFloat   (main_string.header[NordicMain.EPICENTER_LATITUDE])
    main[NordicMain.EPICENTER_LONGITUDE]            = returnFloat   (main_string.header[NordicMain.EPICENTER_LONGITUDE])
    main[NordicMain.DEPTH]                          = returnFloat   (main_string.header[NordicMain.DEPTH])
    main[NordicMain.DEPTH_CONTROL]                  = returnString  (main_string.header[NordicMain.DEPTH_CONTROL])
    main[NordicMain.LOCATING_INDICATOR]             = returnString  (main_string.header[NordicMain.LOCATING_INDICATOR])
    main[NordicMain.EPICENTER_REPORTING_AGENCY]     = returnString  (main_string.header[NordicMain.EPICENTER_REPORTING_AGENCY])
    main[NordicMain.STATIONS_USED]                  = returnInt     (main_string.header[NordicMain.STATIONS_USED])
    main[NordicMain.RMS_TIME_RESIDUALS]             = returnFloat   (main_string.header[NordicMain.RMS_TIME_RESIDUALS])
    main[NordicMain.MAGNITUDE_1]                    = returnFloat   (main_string.header[NordicMain.MAGNITUDE_1])
    main[NordicMain.TYPE_OF_MAGNITUDE_1]            = returnString  (main_string.header[NordicMain.TYPE_OF_MAGNITUDE_1])
    main[NordicMain.MAGNITUDE_REPORTING_AGENCY_1]   = returnString  (main_string.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_1])
    main[NordicMain.MAGNITUDE_2]                    = returnFloat   (main_string.header[NordicMain.MAGNITUDE_2]) 
    main[NordicMain.TYPE_OF_MAGNITUDE_2]            = returnString  (main_string.header[NordicMain.TYPE_OF_MAGNITUDE_2])
    main[NordicMain.MAGNITUDE_REPORTING_AGENCY_2]   = returnString  (main_string.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_2])
    main[NordicMain.MAGNITUDE_3]                    = returnInt     (main_string.header[NordicMain.MAGNITUDE_3])
    main[NordicMain.TYPE_OF_MAGNITUDE_3]            = returnString  (main_string.header[NordicMain.TYPE_OF_MAGNITUDE_3])
    main[NordicMain.MAGNITUDE_REPORTING_AGENCY_3]   = returnString  (main_string.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_3])
    main[NordicMain.EVENT_ID]                       = event_id

    return NordicMain(main) 

def macroseismicString2Macroseismic(macro_string, event_id):
    """
    Function that converts all values in macroseismic string list into macroseismic list with correct value types.

    Args:
        macro_string.header(str []): list of all string valus of the macroseismic header
        event_id (int): event_id of the macroseismic header

    Returns:
        List of all macroseismic info in correct order
    """
    macro = [None]*21

    macro[NordicMacroseismic.DESCRIPTION]                   = returnString  (macro_string.header[NordicMacroseismic.DESCRIPTION])
    macro[NordicMacroseismic.DIASTROPHISM_CODE]             = returnString  (macro_string.header[NordicMacroseismic.DIASTROPHISM_CODE])
    macro[NordicMacroseismic.TSUNAMI_CODE]                  = returnString  (macro_string.header[NordicMacroseismic.TSUNAMI_CODE])
    macro[NordicMacroseismic.SEICHE_CODE]                   = returnString  (macro_string.header[NordicMacroseismic.SEICHE_CODE])
    macro[NordicMacroseismic.CULTURAL_EFFECTS]              = returnString  (macro_string.header[NordicMacroseismic.CULTURAL_EFFECTS])
    macro[NordicMacroseismic.UNUSUAL_EFFECTS]               = returnString  (macro_string.header[NordicMacroseismic.UNUSUAL_EFFECTS])
    macro[NordicMacroseismic.MAXIMUM_OBSERVED_INTENSITY]    = returnFloat   (macro_string.header[NordicMacroseismic.MAXIMUM_OBSERVED_INTENSITY])
    macro[NordicMacroseismic.MAXIMUM_INTENSITY_QUALIFIER]   = returnString  (macro_string.header[NordicMacroseismic.MAXIMUM_INTENSITY_QUALIFIER])
    macro[NordicMacroseismic.INTENSITY_SCALE]               = returnString  (macro_string.header[NordicMacroseismic.INTENSITY_SCALE])
    macro[NordicMacroseismic.MACROSEISMIC_LATITUDE]         = returnFloat   (macro_string.header[NordicMacroseismic.MACROSEISMIC_LATITUDE])
    macro[NordicMacroseismic.MACROSEISMIC_LONGITUDE]        = returnFloat   (macro_string.header[NordicMacroseismic.MACROSEISMIC_LONGITUDE])
    macro[NordicMacroseismic.MACROSEISMIC_MAGNITUDE]        = returnFloat   (macro_string.header[NordicMacroseismic.MACROSEISMIC_MAGNITUDE])
    macro[NordicMacroseismic.TYPE_OF_MAGNITUDE]             = returnString  (macro_string.header[NordicMacroseismic.TYPE_OF_MAGNITUDE])
    macro[NordicMacroseismic.LOGARITHM_OF_RADIUS]           = returnFloat   (macro_string.header[NordicMacroseismic.LOGARITHM_OF_RADIUS])
    macro[NordicMacroseismic.LOGARITHM_OF_AREA_1]           = returnFloat   (macro_string.header[NordicMacroseismic.LOGARITHM_OF_AREA_1])
    macro[NordicMacroseismic.BORDERING_INTENSITY_1]         = returnFloat   (macro_string.header[NordicMacroseismic.BORDERING_INTENSITY_1])
    macro[NordicMacroseismic.LOGARITHM_OF_AREA_2]           = returnFloat   (macro_string.header[NordicMacroseismic.LOGARITHM_OF_AREA_2])
    macro[NordicMacroseismic.BORDERING_INTENSITY_2]         = returnFloat   (macro_string.header[NordicMacroseismic.BORDERING_INTENSITY_2])
    macro[NordicMacroseismic.QUALITY_RANK]                  = returnString  (macro_string.header[NordicMacroseismic.QUALITY_RANK])
    macro[NordicMacroseismic.REPORTING_AGENCY]              = returnString  (macro_string.header[NordicMacroseismic.REPORTING_AGENCY])
    macro[NordicMacroseismic.EVENT_ID]                      = event_id

    return NordicMacroseismic(macro)

def commentString2Comment(comment_string, event_id):
    """
    Function that converts all values in comment string list into comment list with correct value types.

    Args:
        comment_string.header(str []): list of all string valus of the comment header
        event_id (int): event_id of the comment header

    Returns:
        List of all comment info in correct order
    """
    comment = [None]*2

    comment[NordicComment.H_COMMENT] = returnString (comment_string.header[NordicComment.H_COMMENT])
    comment[NordicComment.EVENT_ID]  = event_id

    return NordicComment(comment)

def errorString2Error(error_string, header_id):
    """
    Function that converts all values in comment string list into comment list with correct value types.

    Args:
        comment_string.header(str []): list of all string valus of the comment header
        header_id (int): header_id of the comment header

    Returns:
        List of all error info in correct order
    """
    error = [None]*7

    error[NordicError.GAP]                          = returnInt     (error_string.header[NordicError.GAP]) 
    error[NordicError.SECOND_ERROR]                 = returnFloat   (error_string.header[NordicError.SECOND_ERROR]) 
    error[NordicError.EPICENTER_LATITUDE_ERROR]     = returnFloat   (error_string.header[NordicError.EPICENTER_LATITUDE_ERROR]) 
    error[NordicError.EPICENTER_LONGITUDE_ERROR]    = returnFloat   (error_string.header[NordicError.EPICENTER_LONGITUDE_ERROR]) 
    error[NordicError.DEPTH_ERROR]                  = returnFloat   (error_string.header[NordicError.DEPTH_ERROR]) 
    error[NordicError.MAGNITUDE_ERROR]              = returnFloat   (error_string.header[NordicError.MAGNITUDE_ERROR]) 
    error[NordicError.HEADER_ID]                    = header_id

    return NordicError(error, error_string.header_pos)

def waveformString2Waveform(waveform_string, event_id):
    """
    Function that converts all values in waveform string list into waveform list with correct value types.

    Args:
        waveform_string.header(str []): list of all string valus of the waveform header
        header_id (int): header_id of the waveform header

    Returns:
        List of all waveform info in correct order
    """
    waveform = [None]*2

    waveform[NordicWaveform.WAVEFORM_INFO]  = returnString  (waveform_string.header[NordicWaveform.WAVEFORM_INFO])
    waveform[NordicWaveform.EVENT_ID]       = event_id

    return NordicWaveform(waveform)

def dataString2Data(data_string, event_id):
    """
    Function that converts all values in data string list into data list with correct value types.

    Args:
        data_string.header(str []): list of all string valus of the data header
        header_id (int): header_id of the data header

    Returns:
        List of all data info in correct order
    """
    data = [None]*23

    data[NordicData.STATION_CODE]                   = returnString  (data_string.data[NordicData.STATION_CODE])
    data[NordicData.SP_INSTRUMENT_TYPE]             = returnString  (data_string.data[NordicData.SP_INSTRUMENT_TYPE])
    data[NordicData.SP_COMPONENT]                   = returnString  (data_string.data[NordicData.SP_COMPONENT])
    data[NordicData.QUALITY_INDICATOR]              = returnString  (data_string.data[NordicData.QUALITY_INDICATOR])
    data[NordicData.PHASE_TYPE]                     = returnString  (data_string.data[NordicData.PHASE_TYPE])
    data[NordicData.WEIGHT]                         = returnInt     (data_string.data[NordicData.WEIGHT])
    data[NordicData.FIRST_MOTION]                   = returnString  (data_string.data[NordicData.FIRST_MOTION])
    data[NordicData.TIME_INFO]                      = returnString  (data_string.data[NordicData.TIME_INFO])
    data[NordicData.HOUR]                           = returnInt     (data_string.data[NordicData.HOUR])
    data[NordicData.MINUTE]                         = returnInt     (data_string.data[NordicData.MINUTE])
    data[NordicData.SECOND]                         = returnFloat   (data_string.data[NordicData.SECOND])
    data[NordicData.SIGNAL_DURATION]                = returnInt     (data_string.data[NordicData.SIGNAL_DURATION])
    data[NordicData.MAX_AMPLITUDE]                  = returnFloat   (data_string.data[NordicData.MAX_AMPLITUDE])
    data[NordicData.MAX_AMPLITUDE_PERIOD]           = returnFloat   (data_string.data[NordicData.MAX_AMPLITUDE_PERIOD])
    data[NordicData.BACK_AZIMUTH]                   = returnFloat   (data_string.data[NordicData.BACK_AZIMUTH])
    data[NordicData.APPARENT_VELOCITY]              = returnFloat   (data_string.data[NordicData.APPARENT_VELOCITY])
    data[NordicData.SIGNAL_TO_NOISE]                = returnFloat   (data_string.data[NordicData.SIGNAL_TO_NOISE])
    data[NordicData.AZIMUTH_RESIDUAL]               = returnInt     (data_string.data[NordicData.AZIMUTH_RESIDUAL])
    data[NordicData.TRAVEL_TIME_RESIDUAL]           = returnFloat   (data_string.data[NordicData.TRAVEL_TIME_RESIDUAL])
    data[NordicData.LOCATION_WEIGHT]                = returnInt     (data_string.data[NordicData.LOCATION_WEIGHT])
    data[NordicData.EPICENTER_DISTANCE]             = returnInt     (data_string.data[NordicData.EPICENTER_DISTANCE])
    data[NordicData.EPICENTER_TO_STATION_AZIMUTH]   = returnInt     (data_string.data[NordicData.EPICENTER_TO_STATION_AZIMUTH])
    data[NordicData.EVENT_ID]                       = event_id

    return NordicData(data)

