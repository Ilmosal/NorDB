import logging
import os
import sys
import psycopg2

MODULE_PATH = os.path.realpath(__file__)[:-len("sql2nordic.py")]

username = ""
   
from nordb.core import nordicHandler
from nordb.core import usernameUtilities

def nordicEventToNordic(nordic):
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

    nordic_string.append(create_help_header_string())

    for pd in nordic.phase_data:
        nordic_string.append(create_phase_data_string(pd))      

    nordic_string.append("\n")

    return nordic_string

def create_help_header_string():
    h_string = " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n"
    return h_string

def create_main_header_string(hd):
    h_string = " "
    h_string += add_integer_to_string(hd.date.year, 4, '<')
    h_string += " "
    h_string += add_integer_to_string(hd.date.month, 2, '0')
    h_string += add_integer_to_string(hd.date.day, 2, '0')
    h_string += " "
    h_string += add_integer_to_string(hd.hour, 2, '0')
    h_string += add_integer_to_string(hd.minute, 2, '0')
    h_string += " "
    h_string += add_float_to_string(hd.second, 4, 1, '>')
    h_string += add_string_to_string(hd.location_model, 1, '<')
    h_string += add_string_to_string(hd.distance_indicator, 1, '<')
    h_string += add_string_to_string(hd.event_desc_id, 1, '<')
    h_string += add_float_to_string(hd.epicenter_latitude, 7, 3, '>')
    h_string += add_float_to_string(hd.epicenter_longitude, 8, 3, '>')
    h_string += add_float_to_string(hd.depth, 5, 1, '>')
    h_string += add_string_to_string(hd.depth_control, 1, '>')
    h_string += add_string_to_string(hd.locating_indicator, 1, '>')
    h_string += add_string_to_string(hd.epicenter_reporting_agency, 3, '<')
    h_string += add_integer_to_string(hd.stations_used, 3, '>')
    h_string += add_float_to_string(hd.rms_time_residuals, 4, 1, '>')
    h_string += " "
    h_string += add_float_to_string(hd.magnitude_1, 3, 1, '>')
    h_string += add_string_to_string(hd.type_of_magnitude_1, 1, '>')
    h_string += add_string_to_string(hd.magnitude_reporting_agency_1, 3, '>')
    h_string += " "
    h_string += add_float_to_string(hd.magnitude_2, 3, 1, '>')
    h_string += add_string_to_string(hd.type_of_magnitude_2, 1, '>')
    h_string += add_string_to_string(hd.magnitude_reporting_agency_2, 3, '>')
    h_string += " "
    h_string += add_float_to_string(hd.magnitude_3, 3, 1, '>')
    h_string += add_string_to_string(hd.type_of_magnitude_3, 1, '>')
    h_string += add_string_to_string(hd.magnitude_reporting_agency_3, 3, '>')
    h_string += "1\n"

    return h_string

def create_comment_header_string(hd):
    h_string = " "
    h_string += add_string_to_string(hd.h_comment, 78, '<')
    h_string += "3\n"

    return h_string



def create_error_header_string(hd):
    h_string = " "
    h_string += "GAP="
    h_string += add_integer_to_string(hd.gap, 3, '>')
    h_string += "        "
    h_string += add_float_to_string(hd.second_error, 4, 1, '>')
    h_string += "   "   
    h_string += add_float_to_string(hd.epicenter_latitude_error, 7, 3, '>')
    h_string += add_float_to_string(hd.epicenter_longitude_error, 8, 3, '>')
    h_string += add_float_to_string(hd.depth_error, 5, 1, '>')
    h_string += "             " 
    h_string += add_float_to_string(hd.magnitude_error, 3, 1, '>')
    h_string += "                    5\n"
    return h_string

def create_waveform_header_string(hd):
    h_string = " "
    h_string += add_string_to_string(hd.waveform_info, 78, '<')
    h_string += "6\n"

    return h_string

def create_phase_data_string(pd):
    phase_string = " "
    phase_string += add_string_to_string(pd.station_code, 4, '<')
    phase_string += " "
    phase_string += add_string_to_string(pd.sp_instrument_type, 1, '<') 
    phase_string += add_string_to_string(pd.sp_component, 1, '<')
    phase_string += " "
    phase_string += add_string_to_string(pd.quality_indicator, 1, '<')  
    phase_string += add_string_to_string(pd.phase_type, 4, '<')
    phase_string += add_integer_to_string(pd.weight, 1, '<')
    phase_string += " "
    phase_string += add_string_to_string(pd.first_motion, 1, '<')
    phase_string += add_string_to_string(pd.time_info, 1, '<')
    phase_string += add_integer_to_string(pd.hour, 2, '0')
    phase_string += add_integer_to_string(pd.minute, 2, '0')
    phase_string += " "
    phase_string += add_float_to_string(pd.second, 5, 2, '>')
    phase_string += " "
    phase_string += add_integer_to_string(pd.signal_duration, 4, '>')
    phase_string += " "
    phase_string += add_float_to_string(pd.max_amplitude, 6, 1, '>')
    phase_string += " "
    phase_string += add_float_to_string(pd.max_amplitude_period, 4, 1, '>')
    phase_string += " "
    phase_string += add_float_to_string(pd.back_azimuth, 5, 1, '>')
    phase_string += " "
    phase_string += add_float_to_string(pd.apparent_velocity, 4, 2, '>')
    phase_string += add_float_to_string(pd.signal_to_noise, 4, 2, '>')
    phase_string += add_integer_to_string(pd.azimuth_residual, 3, '>')
    phase_string += add_float_to_string(pd.travel_time_residual, 5, 1, '>')
    phase_string += add_integer_to_string(pd.location_weight, 2, '>')   
    phase_string += add_integer_to_string(pd.epicenter_distance, 5, '>')
    phase_string += " "
    phase_string += add_integer_to_string(pd.epicenter_to_station_azimuth, 3, '>')
    phase_string += " \n"

    return phase_string

def add_string_to_string(value, val_len, front):
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

    nordic = nordicHandler.readNordicEvent(cur, nordicEventId)
    
    if nordic == None:
        return False
    
    nordicString = nordicEventToNordic(nordic)

    if output is None:

        filename = "{:d}{:03d}{:02d}{:02d}{:02d}".format(nordic.headers[1][0].date.year, nordic.headers[1][0].date.timetuple().tm_yday, nordic.headers[1][0].hour, nordic.headers[1][0].minute, int(nordic.headers[1][0].second)) + ".nordic"
        
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
    
