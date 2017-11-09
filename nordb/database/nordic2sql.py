import psycopg2
import sys
import os
import pwd
from datetime import date
import datetime
import math
import fnmatch
import logging

MODULE_PATH = os.path.realpath(__file__)[:-len("nordic2sql.py")]

username = ""

from nordb.core import nordicRead
from nordb.core import nordicHandler
from nordb.core import nordicFix
from nordb.core import usernameUtilities
from nordb.core import nordic
from nordb.core.nordic import NordicData, NordicMain, NordicMacroseismic, NordicComment, NordicError, NordicWaveform, NordicEvent
from nordb.validation import nordicValidation
from nordb.validation import nordicFindOld
from nordb.database import sql2nordic

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

def read_headers(nordic_string):
    """
    Method for reading all the header files from the nordic file and returning them

    Args:
        nordic (str[]): nordic file in string array form

    Returns:
        List of Header objects, amount of headers
    """
    i = 1
    headers = {1:[], 2:[], 3:[], 5:[], 6:[]}
    
    #find where the data starts 
    while (i < len(nordic_string)):
        if (nordic_string[i][79] == ' '):
            i+=1
            break
        i+=1

    if (len(nordic_string) != i):
        i-=1

    mheader_pos = -1

    #read the header lines
    for x in range(0, i):
        if (nordic_string[x][79] == '1'):
            headers[1].append(nordic.createStringMainHeader(nordic_string[x]))
            mheader_pos = len(headers[1])-1
        elif (nordic_string[x][79] == '2'):
            headers[2].append(nordic.createStringMacroseismicHeader(nordic_string[x]))
        elif (nordic_string[x][79] == '3'):
            headers[3].append(nordic.createStringCommentHeader(nordic_string[x]))
        elif (nordic_string[x][79] == '5'):
            headers[5].append(nordic.createStringErrorHeader(nordic_string[x], mheader_pos))
        elif (nordic_string[x][79] == '6'):
            headers[6].append(nordic.createStringWaveformHeader(nordic_string[x]))

    return headers, i
    
def read_event(nordic_string, event_type, nordic_filename, fixNordic, ignore_duplicates, no_duplicates, creation_id):
    """
    Method for reading one event and pushing it to the database

    Args:
        nordic_string (str []): nordic file in string array form
        event_type (int): event type id of the nordic event
        nordic_filename (str): filename of the read nordic file
        fixNordic (bool): flag for if fixNordic library needs to be used
        ignore_duplicates (bool): flag for if the event has no earlier events in the database
        creation_id (int): creation id of the command. Used in the undo function

    Returns:
        True or False if the event has been successfully pushed to the database
    """
    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid!")
        return  False

    cur = conn.cursor()

    if not nordic_string:
        conn.close()
        return False

    headers, headers_size = read_headers(nordic_string)
    data = []

    author_id = "---"
    
    #Get the author_id from the comment header
    for header in headers[3]:
        if header.header_type == 3:
            if fnmatch.fnmatch(header.header[NordicComment.H_COMMENT], "*(???)*"):
                for x in range(0, len(header.header[NordicComment.H_COMMENT])-4):
                    if header.header[NordicComment.H_COMMENT][x] == '(' and header.header[NordicComment.H_COMMENT][x+4] == ')':
                        author_id = header.header[NordicComment.H_COMMENT][x+1:x+4]

    
    #See if the filename already exists in the database
    filename_id = -1
    cur.execute("SELECT id FROM nordic_file WHERE file_location = %s", (nordic_filename,))
    filenameids = cur.fetchone()
    if filenameids is not None:
        filename_id = filenameids[0]

    for x in range(headers_size, len(nordic_string)):
        data.append(nordic.createStringPhaseData(nordic_string[x]))
    
    nordic_event = NordicEvent(headers, data, -1)
   
    if fixNordic:
         nordicFix.fixNordicEvent(nordic_event)
    
    if not nordicValidation.validateNordic(nordic_event, cur):
        logging.error("Nordic validation failed with event: \n" 
                        + headers[1][0].header[NordicMain.O_STRING])
        conn.close()
        return False

    #VALIDATE THE DATA BEFORE PUSHING INTO THE DATABASE. 
    #DONT PUT ANYTHING TO THE DATABASE BEFORE THIS

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
        cur.execute("SELECT root_id from nordic_event WHERE id = %s", (e_id,))
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

        #Add all headers to the database
        
        header_ids = []
        for h in nordic_event.headers[1]:
            header_ids.append(execute_command(  cur, 
                                                INSERT_COMMANDS[1], 
                                                nordic.mainString2Main(h, event_id).header, 
                                                True))
        for h in nordic_event.headers[2]:
            execute_command(    cur, 
                                INSERT_COMMANDS[2], 
                                nordic.macroseismicString2Macroseismic(h, event_id).header,   
                                False)
        for h in nordic_event.headers[3]:
            execute_command(    cur, 
                                INSERT_COMMANDS[3], 
                                nordic.commentString2Comment(h, event_id).header,   
                                False)
        for h in nordic_event.headers[5]:       
            execute_command(    cur, 
                                INSERT_COMMANDS[5], 
                                nordic.errorString2Error(h, header_ids[h.header_pos]).header, 
                                False)
        for h in nordic_event.headers[6]:
            execute_command(    cur, 
                                INSERT_COMMANDS[6], 
                                nordic.waveformString2Waveform(h, event_id).header, 
                                False)

        #Adding the data to the database
        for phase_data in nordic_event.data:
            execute_command(    cur, 
                                INSERT_COMMANDS[7], 
                                nordic.dataString2Data(phase_data, event_id).data, 
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
'       returnValue(bool): boolean values for if the command returns a value
        
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

def read_nordicp(f, event_type, fixNordic, ignore_duplicates, no_duplicates):
    """
    Function for reading the whole file and all the events in it to the database.

    Args:
        f (File): File object of the nordic file
        event_type (int): event type id of the nordic event
        fixNordic (bool): flag for if fixNordic library needs to be used
        ignore_duplicates (bool): flag for iignoring all events that already are in the database
        no_duplicates(bool): flag for if there are no duplicate events in the file compared to dapabase

    Returns:
        True or False if the whole file has been successfully pushed to the database

    """
    username = usernameUtilities.readUsername()
    creation_id = create_creation_info()
    try:
        nordics = nordicRead.readNordicFile(f)

        for nordic in nordics:
            if not read_event(nordic, event_type, f.name, fixNordic, ignore_duplicates, no_duplicates, creation_id):
                if len(nordic) > 0:
                    logging.info("Problem in nordic: " + nordic[0][1:20])
    except KeyboardInterrupt:
        print("\n")
        logging.error("Keyboard interrupt by user")
        delete_creation_info_if_unnecessary(creation_id)
        return False

    delete_creation_info_if_unnecessary(creation_id)
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

