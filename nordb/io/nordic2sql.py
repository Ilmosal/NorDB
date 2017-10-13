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

from nordb.core.nordicStringClass import *
from nordb.core import nordicRead
from nordb.core import nordicHandler
from nordb.core import nordicFix
from nordb.core import usernameUtilities
from nordb.validation import nordicValidation
from nordb.validation import nordicFindOld
from nordb.io import sql2nordic

INSERT_COMMANDS = {
1:"INSERT INTO nordic_header_main (event_id, date, hour, minute, second, location_model, distance_indicator, event_desc_id, epicenter_latitude, epicenter_longitude, depth, depth_control, locating_indicator, epicenter_reporting_agency, stations_used, rms_time_residuals, magnitude_1, type_of_magnitude_1, magnitude_reporting_agency_1, magnitude_2, type_of_magnitude_2, magnitude_reporting_agency_2, magnitude_3, type_of_magnitude_3, magnitude_reporting_agency_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
2:"INSERT INTO nordic_header_macroseismic (event_id, description, diastrophism_code, tsunami_code, seiche_code, cultural_effects, unusual_effects, maximum_observed_intensity, maximum_intensity_qualifier, intensity_scale, macroseismic_latitude, macroseismic_longitude, macroseismic_magnitude, type_of_magnitude, logarithm_of_radius, logarithm_of_area_1, bordering_intensity_1, logarithm_of_area_2, bordering_intensity_2, quality_rank, reporting_agency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
3:"INSERT INTO nordic_header_comment (event_id, h_comment) VALUES (%s, %s);",
5:"INSERT INTO nordic_header_error (header_id, gap, second_error, epicenter_latitude_error, epicenter_longitude_error, depth_error, magnitude_error) VALUES (%s, %s, %s, %s, %s, %s, %s);",
6:"INSERT INTO nordic_header_waveform (event_id, waveform_info) VALUES (%s, %s);",
7:"INSERT INTO nordic_phase_data (event_id, station_code, sp_instrument_type, sp_component, quality_indicator, phase_type, weight, first_motion, time_info, hour, minute, second, signal_duration, max_amplitude, max_amplitude_period, back_azimuth, apparent_velocity, signal_to_noise, azimuth_residual, travel_time_residual, location_weight, epicenter_distance, epicenter_to_station_azimuth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
8:"INSERT INTO creation_info DEFAULT VALUES RETURNING id"
}


#function for reading all the headers
def read_headers(nordic):
    i = 1
    headers = []
    #find where the data starts 
    while (i < len(nordic)):
        if (nordic[i][79] == ' '):
            i+=1
            break
        i+=1

    if (len(nordic) != i):
        i-=1

    #read the header lines
    for x in range(0, i):
        if (nordic[x][79] == '1'):
            headers.append(NordicHeaderMain(nordic[x]))
        elif (nordic[x][79] == '2'):
            headers.append(NordicHeaderMacroseismic(nordic[x]))
        elif (nordic[x][79] == '3'):
            headers.append(NordicHeaderComment(nordic[x]))
        elif (nordic[x][79] == '5'):
            headers.append(NordicHeaderError(nordic[x]))
        elif (nordic[x][79] == '6'):
            headers.append(NordicHeaderWaveform(nordic[x]))

    return headers
    
#function for reading one event and pushing it to the database
def read_event(nordic, event_type, nordic_filename, fixNordic, ignore_duplicates, no_duplicates, creation_id):
    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid!")
        return  False

    cur = conn.cursor()

    #Getting the nordic_event id from the database
    if not nordic:
        conn.close()
        return False

    #Reading headers and data 
    headers = read_headers(nordic)
    data = []

    author_id = "---"
    
    #Get the author_id from the comment header
    for header in headers:
        if header.tpe == 3:
            if fnmatch.fnmatch(header.h_comment, "*(???)*"):
                for x in range(0, len(header.h_comment)-4):
                    if header.h_comment[x] == '(' and header.h_comment[x+4] == ')':
                        author_id = header.h_comment[x+1:x+4]

    
    #See if the filename already exists in the database
    filename_id = -1
    cur.execute("SELECT id FROM nordic_file WHERE file_location = %s", (nordic_filename,))
    filenameids = cur.fetchone()
    if filenameids is not None:
        filename_id = filenameids[0]

    #Read the data
    for x in range(len(headers), len(nordic)):
        data.append(NordicData(nordic[x]))

    #Generate the event
    nordic_event = NordicEvent(headers, data, event_type, author_id, "NOPROGRAM")
    
    if fixNordic:
        nordicFix.fixNordicEvent(nordic_event)

    #VALIDATE THE DATA BEFORE PUSHING INTO THE DATABASE. DONT PUT ANYTHING TO THE DATABASE BEFORE THIS
    if not nordicValidation.validateNordic(nordic_event, cur):
        logging.error("Nordic validation failed with event: \n" + headers[0].getHeaderString())
        conn.close()
        return False

    e_id = nordicFindOld.checkForSameEvents(nordic_event, cur)
    i_ans = ""
    
    if no_duplicates:
        pass
    elif ignore_duplicates:
        conn.close()
        return False
    elif e_id != -1:
        while i_ans != "n" and i_ans != "y":
            print("Same event found with id {0}. Is it the same event: ".format(e_id))
            print("New: " + headers[0].getHeaderString(), end='')
            print("Old: " + sql2nordic.nordicEventToNordic(nordicHandler.readNordicEvent(cur, e_id))[0], end='')
            i_ans = input("Answer(y/n): ")

            if (i_ans == "y"):
                while i_ans != "y":
                    print("Do you want to replace the file in the root?")
                    i_ans = input("Answer(y/n): ")
                    if (i_ans == "n"):
                        conn.close()
                        return False
   
    if e_id != -1:
        e_id = nordicFindOld.checkForSimilarEvents(nordic_event, cur)
        if no_duplicates:
            pass
        elif ignore_duplicates:
            conn.close()
            return False
        elif e_id != -1:
            print("Similar event found with id {0}. Is it the same event: ".format(e_id))
            print("New: " + headers[0].getHeaderString(), end='')
            print("Old: " + sql2nordic.nordicEventToNordic(nordicHandler.readNordicEvent(cur, e_id))[0], end='')
            i_ans = input("Answer(y/n): ")

            if (i_ans == "y"):
                while i_ans != "y":
                    print("Do you want to replace the file in the root?")
                    i_ans = input("Answer(y/n): ")
                    if (i_ans == "n"):
                        conn.close()
                        return False

 
    root_id = -1
    #GET THE ROOT ID HERE
    if i_ans == "y":
        cur.execute("SELECT root_id from nordic_event WHERE id = %s", (e_id,))
        root_id = cur.fetchone()[0]

    try:
        if i_ans != "y":
            cur.execute("INSERT INTO nordic_event_root DEFAULT VALUES RETURNING id;")
            root_id = cur.fetchone()[0]

        if filename_id == -1:
            cur.execute("INSERT INTO nordic_file (file_location) VALUES (%s) RETURNING id", (nordic_filename,))
            filename_id = cur.fetchone()[0]


        #Add a new nordic_event to the db
        cur.execute("INSERT INTO nordic_event (event_type, root_id, nordic_file_id, author_id, creation_id) VALUES (%s, %s, %s, %s, %s) RETURNING id", 
                    (nordic_event.event_type, 
                    root_id, 
                    filename_id, 
                    nordic_event.author_id,
                    creation_id)
                    )
        event_id = cur.fetchone()[0]
            

        if e_id != -1 and i_ans == "y" and event_type not in "OA":
            cur.execute("INSERT INTO nordic_modified (event_id, replacement_event_id, old_event_type, replaced) VALUES (%s, %s, %s, %s)", 
                        (e_id, 
                        event_id, 
                        event_type, 
                        '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
            cur.execute("UPDATE nordic_event SET event_type = 'O' WHERE id = %s", (str(e_id),))

        #Add all headers to the database
        for h in nordic_event.headers:
            if h.tpe == 1:
                h.event_id = str(event_id)
                mheader_id = execute_command(cur, INSERT_COMMANDS[1], nordicHandler.createMainHeaderList(h), True)[0]
            elif h.tpe == 2:
                h.event_id = str(event_id)
                execute_command(cur, INSERT_COMMANDS[2], nordicHandler.createMacroseismicHeaderList(h), False)
            elif h.tpe == 3:
                h.event_id = str(event_id)
                execute_command(cur, INSERT_COMMANDS[3], nordicHandler.createCommentHeaderList(h), False)
            elif h.tpe == 5:
                h.header_id = str(mheader_id)
                execute_command(cur, INSERT_COMMANDS[5], nordicHandler.createErrorHeaderList(h), False)
            elif h.tpe == 6:
                h.event_id = str(event_id)
                execute_command(cur, INSERT_COMMANDS[6], nordicHandler.createWaveformHeaderList(h), False)

        #Adding the data to the database
        for phase_data in nordic_event.data:
            phase_data.event_id = str(event_id)
            execute_command(cur, INSERT_COMMANDS[7], nordicHandler.createPhaseDataList(phase_data), False)

        conn.commit()
        conn.close()
        return True

    except psycopg2.Error as e:
        logging.error("Some error happened with sql-queries that was not detected by validation layer!")
        logging.error(e.pgerror)
        conn.close()
        return False

def create_creation_info():
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
    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid!")
        return creation_id

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) from nordic_event, creation_info WHERE nordic_event.creation_id = creation_info.id AND creation_info.id = %s;", (creation_id,))

    if cur.fetchone()[0] == 0:
        cur.execute("DELETE FROM creation_info WHERE id = %s", (creation_id,))
    
    conn.commit()
    conn.close()

    return creation_id

#function for performing the sql commands
def execute_command(cur, command, vals, returnValue):
        try:
            cur.execute(command, vals)
        except psycopg2.Error as e:
            logging.error("Error in sql command: " + command)
            logging.error(e.pgerror)
            sys.exit()
        if returnValue:
            return cur.fetchone()
        else:
            return None
#function for reading a nordicp file
def read_nordicp(f, event_type, fix, ignore_duplicates, no_duplicates):
    username = usernameUtilities.readUsername()
    creation_id = create_creation_info()
    try:
        nordics = nordicRead.readNordicFile(f)

        for nordic in nordics:
            if not read_event(nordic, event_type, f.name, fix, ignore_duplicates, no_duplicates, creation_id):
                if len(nordic) > 0:
                    logging.info("Problem in nordic: " + nordic[0][1:20])
    except KeyboardInterrupt:
        print("\n")
        logging.error("Keyboard interrupt by user")
        delete_creation_info_if_unnecessary(creation_id)
        return False

    delete_creation_info_if_unnecessary(creation_id)
    return True

#function for getting the authorID of the last person who edited the file
def get_author(filename):
    try:
        author_id = pwd.getpwuid(os.stat(filename).st_uid).pw_name
        if author_id in authorDict:
            return authorDict[author_id]
        else:
            return "---"
    except:
        logging.error("Filename given to get Author is false")
        return "---"

