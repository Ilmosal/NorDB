import psycopg2
import sys
import os
import pwd
import re
from datetime import date
import datetime
import math
import fnmatch
import logging

MODULE_PATH = os.path.realpath(__file__)[:-len("nordic2sql.py")]

username = ""

from nordb.core import nordicRead
from nordb.core import nordicFix
from nordb.core import usernameUtilities
from nordb.core import nordic
from nordb.core.nordic import NordicData, NordicMain, NordicMacroseismic, NordicComment, NordicError, NordicWaveform, NordicEvent
from nordb.validation import nordicValidation
from nordb.validation import nordicFindOld
from nordb.database import sql2nordic, undoRead

EVENT_TYPE_VALUES = {
    "O":1,
    "A":2,
    "R":3,
    "P":4,
    "F":5,
    "S":6
}

INSERT_COMMANDS = {
                    1:  "INSERT INTO " +
                           "nordic_header_main " +
                           "(date, hour, minute, second, location_model, " +
                            "distance_indicator, event_desc_id, epicenter_latitude, " +
                            "epicenter_longitude, depth, depth_control, " +
                            "locating_indicator, epicenter_reporting_agency, " +
                            "stations_used, rms_time_residuals, magnitude_1, " +
                            "type_of_magnitude_1, magnitude_reporting_agency_1, " +
                            "magnitude_2, type_of_magnitude_2, magnitude_reporting_agency_2, " +
                            "magnitude_3, type_of_magnitude_3, magnitude_reporting_agency_3, " +
                            "event_id) " +
                        "VALUES " +
                           "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " +
                            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " +
                        "RETURNING " +
                           "id;",
                    2:  "INSERT INTO " +
                           "nordic_header_macroseismic " +
                           "(description, diastrophism_code, tsunami_code, seiche_code, " +
                            "cultural_effects, unusual_effects, maximum_observed_intensity, " +
                            "maximum_intensity_qualifier, intensity_scale, macroseismic_latitude, " +
                            "macroseismic_longitude, macroseismic_magnitude, type_of_magnitude, " +
                            "logarithm_of_radius, logarithm_of_area_1, bordering_intensity_1, " +
                            "logarithm_of_area_2, bordering_intensity_2, quality_rank, " +
                            "reporting_agency, event_id) " +
                        "VALUES " +
                           "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " +
                           " %s, %s, %s, %s, %s, %s);",
                    3:  "INSERT INTO  " +
                           "nordic_header_comment  " +
                           "(h_comment, event_id)  " +
                        "VALUES  " +
                           "(%s, %s);",
                    5:  "INSERT INTO  " +
                           "nordic_header_error  " +
                           "(gap, second_error, epicenter_latitude_error, " +
                            "epicenter_longitude_error,  depth_error, " +
                            "magnitude_error, header_id)  " +
                        "VALUES  " +
                           "(%s, %s, %s, %s, %s, %s, %s);",
                    6:  "INSERT INTO  " +
                           "nordic_header_waveform  " +
                           "(waveform_info, event_id)  " +
                        "VALUES  " +
                           "(%s, %s);",
                    7:  "INSERT INTO  " +
                           "nordic_phase_data  " +
                           "(station_code, sp_instrument_type, sp_component, quality_indicator, " +
                            "phase_type, weight, first_motion, time_info, hour, minute, second, " +
                            "signal_duration, max_amplitude, max_amplitude_period, back_azimuth, " +
                            "apparent_velocity, signal_to_noise, azimuth_residual, " +
                            "travel_time_residual, location_weight, epicenter_distance, " + 
                            "epicenter_to_station_azimuth, event_id) " +
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " +
                                 "%s, %s, %s, %s, %s, %s, %s, %s, %s);", 
                    8:  "INSERT INTO  " +
                           "creation_info  " +
                        "DEFAULT VALUES  " +
                        "RETURNING id"
}
  
def event2Database(nordic_event, event_type, nordic_filename, ignore_duplicates, no_duplicates, creation_id):
    """
    Function that pushes a validated event to the database
    
    :param NordicEvent nordic_event: Event that will be pushed to the database
    :param int event_type: event type id 
    :param str nordic_filename: name of the file from which the nordic is read from
    :param bool ignore_duplicates: flag for ignoring all events that already are in the database
    :param bool no_duplicates: flag for telling the program that the event is not in the database and checking for old events will be skipped
    :param int creation_id: id of the creation_info entry in the database
    :return: True of False depending on if the operation was succesful or not
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    author_id = None
    
    for header in nordic_event.headers[3]:
        author_id = re.search(r'\[(\w3)\]', header.header[NordicComment.H_COMMENT]) 
        if author_id is not None:
            break

    if author_id is None:
        author_id = '---' 

    filename_id = -1
    cur.execute("SELECT id FROM nordic_file WHERE file_location = %s", (nordic_filename,))
    filenameids = cur.fetchone()
    if filenameids is not None:
        filename_id = filenameids[0]

    e_id = -1
    if not no_duplicates:
        ans = nordicFindOld.checkForSameEvents(nordic_event, cur, ignore_duplicates)
        e_id = ans[0]

        if e_id == -1:
            ans = nordicFindOld.checkForSimilarEvents(nordic_event, cur)
            e_id = ans[0]

        if e_id == -9:
            return False
        if ignore_duplicates and e_id > 0:
            return False
        elif ignore_duplicates:
            ans = nordicFindOld.checkForSameEvents(nordic_event, cur, ignore_duplicates)
        e_id = ans[0]
        if e_id > 0:
            return False

    root_id = -1

    if e_id >= 0:
        cur.execute("SELECT root_id FROM nordic_event WHERE id = %s", (e_id,))
        root_id = cur.fetchone()[0]

    try:
        if e_id == -1:
            cur.execute("INSERT INTO nordic_event_root DEFAULT VALUES RETURNING id;")
            root_id = cur.fetchone()[0]

        if filename_id == -1:
            cur.execute("INSERT INTO nordic_file (file_location) VALUES (%s) RETURNING id", (nordic_filename,))
            filename_id = cur.fetchone()[0]

        cur.execute("INSERT INTO  " +
                       "nordic_event  " +
                       "(event_type, root_id, nordic_file_id, author_id, creation_id)  " +
                    "VALUES  " +
                       "(%s, %s, %s, %s, %s)  " +
                    "RETURNING  " +
                       "id", 
                    (event_type, 
                    root_id, 
                    filename_id, 
                    author_id,
                    creation_id)
                    )
        event_id = cur.fetchone()[0]
        
        if e_id != -1 and EVENT_TYPE_VALUES[event_type] == EVENT_TYPE_VALUES[ans[1]] and event_type not in "AO":
            cur.execute("INSERT INTO  " +
                           "nordic_modified " + 
                           "(event_id, replacement_event_id, old_event_type, replaced)  " +
                        "VALUES  " +
                           "(%s, %s, %s, %s)", 
                        (e_id, 
                        event_id, 
                        event_type, 
                        '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
            cur.execute("UPDATE nordic_event SET event_type = 'O' WHERE id = %s", (e_id,))
    
        main_header_id = -1
        for i in range(0, len(nordic_event.headers[1])):
            h = nordic_event.headers[1][i]
            h.header[NordicMain.EVENT_ID] = event_id

            main_header_id = execute_command(  cur, 
                                               INSERT_COMMANDS[1], 
                                               h.header,
                                               True)

            for h_error in nordic_event.headers[5]:
                if h_error.header[h_error.HEADER_ID] == i:
                    h_error.header[h_error.HEADER_ID] = main_header_id

        for h in nordic_event.headers[2]:
            h.header[NordicMacroseismic.EVENT_ID] = event_id
            execute_command(    cur, 
                                INSERT_COMMANDS[2], 
                                h.header,
                                False)
        for h in nordic_event.headers[3]:
            h.header[NordicComment.EVENT_ID] = event_id
            execute_command(    cur, 
                                INSERT_COMMANDS[3], 
                                h.header,
                                False)
        for h in nordic_event.headers[5]:       
            h.header[NordicError.HEADER_ID] = main_header_id
            execute_command(    cur, 
                                INSERT_COMMANDS[5], 
                                h.header,
                                False)
        for h in nordic_event.headers[6]:
            h.header[NordicWaveform.EVENT_ID] = event_id
            execute_command(    cur, 
                                INSERT_COMMANDS[6], 
                                h.header,
                                False)
        #Adding the data to the database
        for phase_data in nordic_event.data:
            
            phase_data.data[NordicData.EVENT_ID] = event_id
            execute_command(    cur, 
                                INSERT_COMMANDS[7], 
                                phase_data.data,
                                False)

        conn.commit()
        conn.close()
        return True

    except psycopg2.Error as e:
        logging.error("Some error happened with sql-queries that was not detected by validation layer!")
        logging.error(e.pgerror)
        conn.close()
        return False

def create_creation_info():
    """
    Function for creating the creation_info entry to the database.

    Returns:
        The creation id created
    """
    creation_id = -1
    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid!")
        return creation_id

    cur = conn.cursor()

    cur.execute(INSERT_COMMANDS[8])
    creation_id = cur.fetchone()[0]
    
    conn.commit()
    conn.close()

    return creation_id

def delete_creation_info_if_unnecessary(creation_id):
    """
    Function for deleting an unnecessary creation info object
    
    Args:
        creation_id(int): id of the creation_info that needs to be deleted

    Returns:
        creation_id of the deleted object
    """
    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid!")
        return creation_id

    cur = conn.cursor()

    cur.execute("SELECT  " +
                   "COUNT(*)  " +
                "FROM  " +
                   "nordic_event, creation_info  " +
                "WHERE  " +
                   "nordic_event.creation_id = creation_info.id  " +
                   "AND creation_info.id = %s;", 
                (creation_id,))

    if cur.fetchone()[0] == 0:
        cur.execute("DELETE FROM creation_info WHERE id = %s", (creation_id,))
    
    conn.commit()
    conn.close()

    return creation_id

def execute_command(cur, command, vals, returnValue):
    """
    Function for for executing a command with values and handling exceptions

    Args:
        cur (Cursor): cursor object from psycopg2 library
        command (str): the sql command string
        vals (list): list of values for the command
        returnValue (bool): boolean values for if the command returns a value

    Returns:
        Values returned by the query
    """
    try:
        cur.execute(command, vals)
    except psycopg2.Error as e:
        logging.error("Error in sql command: " + command)
        logging.error(e.pgerror)
        sys.exit()
    if returnValue:
        return cur.fetchone()[0]
    else:
        return None

def read2Database(f, event_type, fix_nordic, ignore_duplicates, no_duplicates, error_path):
    """
    Function for reading the whole file and all the events in it to the database.

    :param file f: File object of the nordic file
    :param int event_type: event type id of the nordic event
    :param bool fix_nordic: flag for if fixNordic library needs to be used
    :param bool ignore_duplicates: flag for iignoring all events that already are in the database
    :param bool no_duplicates: flag for if there are no duplicate events in the file compared to dapabase
    :return: True or False if the whole file has been successfully pushed to the database
    """
    username = usernameUtilities.readUsername()
    creation_id = create_creation_info()

    try:
        nordics, nordic_failed = nordic.readNordic(f, fix_nordic)
        if len(nordic_failed) > 0:
             print ("Some errors occurred with nordic file {0}. Check {1} for more details!".format(f.name, error_path.split("/")[-1]))

        for nord in nordics:
            event2Database(nord, event_type, f.name, ignore_duplicates, no_duplicates, creation_id)

    except KeyboardInterrupt:
        print("\n")
        logging.error("Keyboard interrupt by user")

        undoRead.removeEventsWithCreationId(creation_id)            
        delete_creation_info_if_unnecessary(creation_id)
        return False
    
    delete_creation_info_if_unnecessary(creation_id)

    if len(nordic_failed) > 0:
        failed = open("f_" + os.path.basename(f.name), "w")

        for n in nordic_failed:
            for line in n:
                failed.write(line)  
            failed.write("\n")

    return True

def get_author(filename):
    """
    Function for getting the owner of the file from the file. Not used currently

    Args:
        filename(str): Name of the file

    Returns:
        Predefined author id 
    """
    try:
        author_id = pwd.getpwuid(os.stat(filename).st_uid).pw_name
        if author_id in authorDict:
            return authorDict[author_id]
        else:
            return "---"
    except:
        logging.error("Filename given to get Author is false")
        return "---"

