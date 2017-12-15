import logging
import os
import sys
import psycopg2

MODULE_PATH = os.path.realpath(__file__)[:-len("sql2nordic.py")]

username = ""

from nordb.core.nordic import NordicMain, NordicMacroseismic, NordicComment
from nordb.core.nordic import NordicError, NordicWaveform, NordicData
from nordb.core import usernameUtilities
from nordb.database import getNordic

def nordicEventToNordic(nordic):
    """
    Method that converts a nordic event object to a nordic file string

    Args:
        nordic (NordicEvent): event data

    Returns:
        nordic file as a string array
    """
    nordic_string = []

    nordic_string.append(create_main_header_string(nordic.headers[1][0]))

    if len(nordic.headers[5]) > 0:
        nordic_string.append(create_error_header_string(nordic.headers[5][0]))

    if len(nordic.headers[6]) > 0:
        nordic_string.append(create_waveform_header_string(nordic.headers[6][0]))

    for hd in nordic.headers[3]:
        nordic_string.append(create_comment_header_string(hd))

    for i in range(1,len(nordic.headers[1])):
        nordic_string.append(create_main_header_string(nordic.headers[1][i]))
        for h_error in nordic.headers[5]:
            if h_error.header[NordicError.HEADER_ID] == nordic.headers[1][i].header[NordicMain.ID]:
                nordic_string.append(create_error_header_string(h_error))

    nordic_string.append(create_help_header_string())

    for pd in nordic.data:
        nordic_string.append(create_phase_data_string(pd))      

    nordic_string.append("\n")

    return nordic_string

def create_help_header_string():
    """
    Function that returns the help header of type 7 as a string. 

    Returns:
        The help header as a string
    """
    h_string = " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n"
    return h_string

def create_main_header_string(hd):
    """
    Function that returns the main header of type 1 as a string.

    Args:
        hd (NordicMain): main header that will be converted

    Returns
    """
    h_string = " "
    h_string += add_integer_to_string(hd.header[NordicMain.DATE].year, 4, '<')
    h_string += " "
    h_string += add_integer_to_string(hd.header[NordicMain.DATE].month, 2, '0')
    h_string += add_integer_to_string(hd.header[NordicMain.DATE].day, 2, '0')
    h_string += " "
    h_string += add_integer_to_string(hd.header[NordicMain.HOUR], 2, '0')
    h_string += add_integer_to_string(hd.header[NordicMain.MINUTE], 2, '0')
    h_string += " "
    h_string += add_float_to_string(hd.header[NordicMain.SECOND], 4, 1, '>')
    h_string += add_string_to_string(hd.header[NordicMain.LOCATION_MODEL], 1, '<')
    h_string += add_string_to_string(hd.header[NordicMain.DISTANCE_INDICATOR], 1, '<')
    h_string += add_string_to_string(hd.header[NordicMain.EVENT_DESC_ID], 1, '<')
    h_string += add_float_to_string(hd.header[NordicMain.EPICENTER_LATITUDE], 7, 3, '>')
    h_string += add_float_to_string(hd.header[NordicMain.EPICENTER_LONGITUDE], 8, 3, '>')
    h_string += add_float_to_string(hd.header[NordicMain.DEPTH], 5, 1, '>')
    h_string += add_string_to_string(hd.header[NordicMain.DEPTH_CONTROL], 1, '>')
    h_string += add_string_to_string(hd.header[NordicMain.LOCATING_INDICATOR], 1, '>')
    h_string += add_string_to_string(hd.header[NordicMain.EPICENTER_REPORTING_AGENCY], 3, '<')
    h_string += add_integer_to_string(hd.header[NordicMain.STATIONS_USED], 3, '>')
    h_string += add_float_to_string(hd.header[NordicMain.RMS_TIME_RESIDUALS], 4, 1, '>')
    h_string += " "
    h_string += add_float_to_string(hd.header[NordicMain.MAGNITUDE_1], 3, 1, '>')
    h_string += add_string_to_string(hd.header[NordicMain.TYPE_OF_MAGNITUDE_1], 1, '>')
    h_string += add_string_to_string(hd.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_1], 3, '>')
    h_string += " "
    h_string += add_float_to_string(hd.header[NordicMain.MAGNITUDE_2], 3, 1, '>')
    h_string += add_string_to_string(hd.header[NordicMain.TYPE_OF_MAGNITUDE_2], 1, '>')
    h_string += add_string_to_string(hd.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_2], 3, '>')
    h_string += " "
    h_string += add_float_to_string(hd.header[NordicMain.MAGNITUDE_3], 3, 1, '>')
    h_string += add_string_to_string(hd.header[NordicMain.TYPE_OF_MAGNITUDE_3], 1, '>')
    h_string += add_string_to_string(hd.header[NordicMain.MAGNITUDE_REPORTING_AGENCY_3], 3, '>')
    h_string += "1\n"

    return h_string

def create_comment_header_string(hd):
    """
    Function for creating comment header string from a nordicComment list
    
    Args:
        hd(list): comment header list
    Returns:
        comment header in a string format

    """
    h_string = " "
    h_string += add_string_to_string(hd.header[NordicComment.H_COMMENT], 78, '<')
    h_string += "3\n"

    return h_string

def create_error_header_string(hd):
    """
    Function for creating error header string from a nordicError list
    
    Args:
        hd(list): error header list
    Returns:
        error header in a string format
    """
    h_string = " "
    h_string += "GAP="
    h_string += add_integer_to_string(hd.header[NordicError.GAP], 3,'>')
    h_string += "        "
    h_string += add_float_to_string(hd.header[NordicError.SECOND_ERROR], 4, 1, '>')
    h_string += "   "   
    h_string += add_float_to_string(hd.header[NordicError.EPICENTER_LATITUDE_ERROR], 7, 3, '>')
    h_string += add_float_to_string(hd.header[NordicError.EPICENTER_LONGITUDE_ERROR], 8, 3, '>')
    h_string += add_float_to_string(hd.header[NordicError.DEPTH_ERROR], 5, 1, '>')
    h_string += "             " 
    h_string += add_float_to_string(hd.header[NordicError.MAGNITUDE_ERROR], 3, 1, '>')
    h_string += "                    5\n"
    return h_string

def create_waveform_header_string(hd):
    """
    Function for creating waveform header string from a nordicWaveform list
    
    Args:
        hd(list): waveform header list
    Returns:
        waveform header in a string format
    """

    h_string = " "
    h_string += add_string_to_string(hd.header[NordicWaveform.WAVEFORM_INFO], 78, '<')
    h_string += "6\n"

    return h_string

def create_phase_data_string(pd):
    """
    Function for creating data header string from a nordicData list
    
    Args:
        hd(list): data header list
    Returns:
        data header in a string format
    """
    phase_string = " "
    phase_string += add_string_to_string(pd.data[NordicData.STATION_CODE], 4, '<')
    phase_string += " "
    phase_string += add_string_to_string(pd.data[NordicData.SP_INSTRUMENT_TYPE], 1, '<') 
    phase_string += add_string_to_string(pd.data[NordicData.SP_COMPONENT], 1, '<')
    phase_string += " "
    phase_string += add_string_to_string(pd.data[NordicData.QUALITY_INDICATOR], 1, '<')  
    phase_string += add_string_to_string(pd.data[NordicData.PHASE_TYPE], 4, '<')
    phase_string += add_integer_to_string(pd.data[NordicData.WEIGHT], 1, '<')
    phase_string += " "
    phase_string += add_string_to_string(pd.data[NordicData.FIRST_MOTION], 1, '<')
    phase_string += add_string_to_string(pd.data[NordicData.TIME_INFO], 1, '<')
    phase_string += add_integer_to_string(pd.data[NordicData.HOUR], 2, '0')
    phase_string += add_integer_to_string(pd.data[NordicData.MINUTE], 2, '0')
    phase_string += " "
    phase_string += add_float_to_string(pd.data[NordicData.SECOND], 5, 2, '>')
    phase_string += " "
    phase_string += add_integer_to_string(pd.data[NordicData.SIGNAL_DURATION], 4, '>')
    phase_string += " "
    phase_string += add_float_to_string(pd.data[NordicData.MAX_AMPLITUDE], 6, 1, '>')
    phase_string += " "
    phase_string += add_float_to_string(pd.data[NordicData.MAX_AMPLITUDE_PERIOD], 4, 1, '>')
    phase_string += " "
    phase_string += add_float_to_string(pd.data[NordicData.BACK_AZIMUTH], 5, 1, '>')
    phase_string += " "
    phase_string += add_float_to_string(pd.data[NordicData.APPARENT_VELOCITY], 4, 2, '>')
    phase_string += add_float_to_string(pd.data[NordicData.SIGNAL_TO_NOISE], 4, 2, '>')
    phase_string += add_integer_to_string(pd.data[NordicData.AZIMUTH_RESIDUAL], 3, '>')
    phase_string += add_float_to_string(pd.data[NordicData.TRAVEL_TIME_RESIDUAL], 5, 1, '>')
    phase_string += add_integer_to_string(pd.data[NordicData.LOCATION_WEIGHT], 2, '>')   
    phase_string += add_integer_to_string(pd.data[NordicData.EPICENTER_DISTANCE], 5, '>')
    phase_string += " "
    phase_string += add_integer_to_string(pd.data[NordicData.EPICENTER_TO_STATION_AZIMUTH], 3, '>')
    phase_string += " \n"

    return phase_string

def add_string_to_string(value, val_len, front):
    """
    Function for parsing a string into correct format. Front works as the parser character which tells some small details on how the string has to be formatted.
    
    >> add_string_to_string("test, 6, '<'")
        "test  "
    
    Args:
        value(str): string value that will be formatted
        val_len(int): int on how long the string needs to be
        front (str): formatting character

    Returns:
        formatted string
    """
    string = ""
    parser = "{:" + front + str(val_len) + "s}"
    if value is not None:
        string += parser.format(value)
    else:
        string = val_len * " "

    return string

def add_integer_to_string(value, val_len, front):
    string = ""
    parser = "{:" + front + str(val_len) + "d}"
    if value is not None:
        string += parser.format(value)
    else:
        string = val_len * " "

    return string

def add_float_to_string(value, val_len, decimal_len, front):
    string = ""
    parser = "{:" + front + str(val_len) + "." + str(decimal_len)  + "f}"
    if value is not None:
        string += parser.format(value)
    else:
        string = val_len * " "
    if value is None:
        return string 
    if float(value) < 0 and val_len == len(string) - 1:
        string = string[0] + string[2:]
        
    return string

def writeNordicEvent(nordicEventId, usr_path, output):
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
        return

    cur = conn.cursor()

    nordic = getNordic.readNordicEvent(cur, nordicEventId)
   
    if nordic == None:
        return False
    
    nordicString = nordicEventToNordic(nordic)

    if output is None:

        filename = "{:d}{:03d}{:02d}{:02d}{:02d}".format(
                        nordic.headers[1][0].header[NordicMain.DATE].year, 
                        nordic.headers[1][0].header[NordicMain.DATE].timetuple().tm_yday, 
                        nordic.headers[1][0].header[NordicMain.HOUR], 
                        nordic.headers[1][0].header[NordicMain.MINUTE], 
                        int(nordic.headers[1][0].header[NordicMain.SECOND])) + ".nordic"
        
        print(filename + " has been created!")
    
        f = open(usr_path + '/' + filename, 'w')
        
        for line in nordicString:   
            f.write(line)

        f.close()
    else:
        f = open(usr_path + "/" + output, "a")

        for line in nordicString:
            f.write(line)

        f.close()

    conn.commit()
    conn.close()

    return True
    
