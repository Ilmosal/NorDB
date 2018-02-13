"""
This module contains all information for pushing a NordicEvent object into the database.


Functions and Classes
---------------------
"""

import psycopg2
import os
import pwd
import re
import datetime

from nordb.core import usernameUtilities

EVENT_TYPE_VALUES = {
    "O":1,
    "A":2,
    "R":3,
    "P":4,
    "F":5,
    "S":6
}

INSERT_COMMANDS = {
                    1:  (
                        "INSERT INTO " 
                        "   nordic_header_main " 
                        "   (date, hour, minute, second, location_model, " 
                        "   distance_indicator, event_desc_id, epicenter_latitude, " 
                        "   epicenter_longitude, depth, depth_control, " 
                        "   locating_indicator, epicenter_reporting_agency, " 
                        "   stations_used, rms_time_residuals, magnitude_1, " 
                        "   type_of_magnitude_1, magnitude_reporting_agency_1, " 
                        "   magnitude_2, type_of_magnitude_2, magnitude_reporting_agency_2, " 
                        "   magnitude_3, type_of_magnitude_3, magnitude_reporting_agency_3, " 
                        "   event_id) " 
                        "VALUES " 
                        "   (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " 
                        "   %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " 
                        "RETURNING " 
                        "   id;"
                        )
                    2:  (
                        "INSERT INTO " 
                           "nordic_header_macroseismic " 
                           "(description, diastrophism_code, tsunami_code, seiche_code, " 
                            "cultural_effects, unusual_effects, maximum_observed_intensity, " 
                            "maximum_intensity_qualifier, intensity_scale, macroseismic_latitude, " 
                            "macroseismic_longitude, macroseismic_magnitude, type_of_magnitude, " 
                            "logarithm_of_radius, logarithm_of_area_1, bordering_intensity_1, " 
                            "logarithm_of_area_2, bordering_intensity_2, quality_rank, " 
                            "reporting_agency, event_id) " 
                        "VALUES " 
                           "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " 
                           " %s, %s, %s, %s, %s, %s);",
                        )
                    3:  (
                        "INSERT INTO  " 
                           "nordic_header_comment  " 
                           "(h_comment, event_id)  " 
                        "VALUES  " 
                           "(%s, %s);",
                        )
                    5:  (
                        "INSERT INTO  " 
                           "nordic_header_error  " 
                           "(gap, second_error, epicenter_latitude_error, " 
                            "epicenter_longitude_error,  depth_error, " 
                            "magnitude_error, header_id)  " 
                        "VALUES  " 
                           "(%s, %s, %s, %s, %s, %s, %s);",
                        )
                    6:  (
                        "INSERT INTO  " 
                           "nordic_header_waveform  " 
                           "(waveform_info, event_id)  " 
                        "VALUES  " 
                           "(%s, %s);",
                        )
                    7:  (
                        "INSERT INTO  " 
                           "nordic_phase_data  " 
                           "(station_code, sp_instrument_type, sp_component, quality_indicator, " 
                            "phase_type, weight, first_motion, time_info, hour, minute, second, " 
                            "signal_duration, max_amplitude, max_amplitude_period, back_azimuth, " 
                            "apparent_velocity, signal_to_noise, azimuth_residual, " 
                            "travel_time_residual, location_weight, epicenter_distance, "  
                            "epicenter_to_station_azimuth, event_id) " 
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " 
                                 "%s, %s, %s, %s, %s, %s, %s, %s, %s);", 
                        )
                    8:  (
                        "INSERT INTO  " 
                           "creation_info  " 
                        "DEFAULT VALUES  " 
                        "RETURNING id"
                        )
}
  
def event2Database(nordic_event, event_type, nordic_filename, creation_id, e_id):
    """
    Function that pushes a NordicEvent object to the database
    
    :param NordicEvent nordic_event: Event that will be pushed to the database
    :param int event_type: event type id 
    :param str nordic_filename: name of the file from which the nordic is read from
    :param int creation_id: id of the creation_info entry in the database
    :param int e_id: id of the event to which this event will be attached to by event_root. If -1 then this event will not be attached to aything.
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    author_id = None

    for header in nordic_event.headers[3]:
        author_id = re.search(r'\[(\w3)\]', header.h_comment) 
        if author_id is not None:
            break

    if author_id is None:
        author_id = '---' 

    filename_id = -1
    cur.execute("SELECT id FROM nordic_file WHERE file_location = %s", (nordic_filename,))
    filenameids = cur.fetchone()
    if filenameids is not None:
        filename_id = filenameids[0]

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
        
        if e_id != -1 and EVENT_TYPE_VALUES[event_type] == EVENT_TYPE_VALUES[event_id[1]] and event_type not in "AO":
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
            h.event_id = event_id

            main_header_id = executeCommand(  cur, 
                                               INSERT_COMMANDS[1], 
                                               h.getAsList(),
                                               True)

            for h_error in nordic_event.headers[5]:
                if h_error.header_pos == i:
                    h_error.header_id = main_header_id

        for h in nordic_event.headers[2]:
            h.event_id = event_id
            executeCommand(    cur, 
                                INSERT_COMMANDS[2], 
                                h.getAsList(),
                                False)
        for h in nordic_event.headers[3]:
            h.event_id = event_id
            executeCommand(    cur, 
                                INSERT_COMMANDS[3], 
                                h.getAsList(),
                                False)
        for h in nordic_event.headers[5]:       
            executeCommand(    cur, 
                                INSERT_COMMANDS[5], 
                                h.getAsList(),
                                False)
        for h in nordic_event.headers[6]:
            h.event_id = event_id
            executeCommand(    cur, 
                                INSERT_COMMANDS[6], 
                                h.getAsList(),
                                False)

        for phase_data in nordic_event.data:
            phase_data.event_id = event_id
            executeCommand(    cur, 
                                INSERT_COMMANDS[7], 
                                phase_data.getAsList(),
                                False)

        conn.commit()
        conn.close()

    except Exception as e:
        conn.close()
        raise e

def createCreationInfo():
    """
    Function for creating the creation_info entry to the database.

    :returns: The creation id of the creation_info entry created
    """
    creation_id = -1
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(INSERT_COMMANDS[8])
    creation_id = cur.fetchone()[0]
    
    conn.commit()
    conn.close()

    return creation_id

def deleteCreationInfoIfUnnecessary(creation_id):
    """
    Function for deleting an unnecessary creation info object
    
    :param int creation_id: id of the creation_info that needs to be deleted
    :returns: creation_id of the deleted object
    """
    conn = usernameUtilities.log2nordb()
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

def executeCommand(cur, command, vals, returnValue):
    """
    Function for for executing a command with values and handling exceptions

    :param Psycopg.Cursor cur: cursor object from psycopg2 library
    :param str command: the sql command string
    :param list vals: list of values for the command
    :param bool returnValue: boolean values for if the command returns a value

    :returns: Values returned by the query or None if returnValue is False
    """
    try:
        cur.execute(command, vals)
    except psycopg2.Error as e:
        raise e
    if returnValue:
        return cur.fetchone()[0]
    else:
        return None

