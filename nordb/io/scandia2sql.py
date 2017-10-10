import sys
import os
import psycopg2
import math
import logging
from datetime import date

from nordb.core.nordicHandler import addStringToData, addIntToData, addFloatToData, addDateToData
from nordb.io.nordic2sql import execute_command
from nordb.core import usernameUtilities

MODULE_PATH = os.path.realpath(__file__)[:-len("scandia2sql.py")]

username = ""

SCANDIA_INSERT = "INSERT INTO scandia_header (event_id, source_ref, origin_questionability, year, month, day, hour, minute, second, epicenter_latitude, epicenter_longitude, origin_time_uncertainty, location_uncertainty, focal_depth, depth_identification_code, magnitude_1, magnitude_scale_1, magnitude_2, magnitude_scale_2, magnitude_3, magnitude_scale_3, maximum_intensity, macroseismic_observation_flag, macroseismic_reference, mean_radius_of_area_percetibility, region_code, number_of_stations_used, max_azimuth_gap, min_epicenter_to_station_distance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

SCANDIA_SELECT = "SELECT event_id FROM nordic_header_main, nordic_event WHERE nordic_event.id = nordic_header_main.event_id AND nordic_event.event_type = 'F' AND nordic_header_main.date = %s AND nordic_header_main.hour = %s AND nordic_header_main.minute = %s AND nordic_header_main.second = %s AND nordic_header_main.epicenter_latitude = %s AND nordic_header_main.epicenter_longitude = %s"

class Scandia:
    def __init__(self, scandia_line, cur):
        self.source_ref = return_string(scandia_line[0:3])
        self.origin_questionability = return_string(scandia_line[3]) 
        self.year = return_int(scandia_line[4:8])
        self.month = return_int(scandia_line[8:10])
        self.day = return_int(scandia_line[10:12])
        #self.date = return_date(scandia_line[4:8] + "-" + scandia_line[8:10] + "-" + scandia_line[10:12])
        self.event_desc = return_string(scandia_line[12]) 
        self.hour = return_int(scandia_line[13:15])
        self.minute = return_int(scandia_line[15:17])
        self.second = return_float(scandia_line[17:21].strip())
        self.epicenter_latitude = return_float(scandia_line[22:27])
        self.epicenter_longitude = return_float(scandia_line[29:34]) 
        self.origin_time_uncertainty = return_string(scandia_line[36])
        self.location_uncertainty = return_string(scandia_line[37])
        self.focal_depth =return_int(scandia_line[38:41])
        self.depth_identification_code = return_string(scandia_line[41])
        self.magnitude_1 = return_float(scandia_line[42:45]) 
        self.magnitude_scale_1 = return_string(scandia_line[45:47]) 
        self.magnitude_2 = return_float(scandia_line[47:50]) 
        self.magnitude_scale_2 = return_string(scandia_line[50:52]) 
        self.magnitude_3 = return_float(scandia_line[52:55]) 
        self.magnitude_scale_3 = return_string(scandia_line[55:57]) 
        self.maximum_intensity = return_string(scandia_line[66:70])
        self.macroseismic_observation_flag = return_string(scandia_line[70]) 
        self.macroseismic_reference = return_string(scandia_line[71:74])
        self.mean_radius_of_area_percetibility = return_int(scandia_line[74:77]) 
        self.region_code = return_string(scandia_line[77])
        self.number_of_stations_used =return_int(scandia_line[78:82])
        self.max_azimuth_gap = return_string(scandia_line[83:86]) 
        self.min_epicenter_to_station_distance = return_string(scandia_line[86:90])
        values = (return_date(scandia_line[4:8] + "-" + scandia_line[8:10] + "-" + scandia_line[10:12]), self.hour, self.minute, self.second, self.epicenter_latitude, self.epicenter_longitude)

        cur.execute("SELECT event_id FROM nordic_header_main, nordic_event WHERE nordic_event.id = nordic_header_main.event_id AND nordic_event.event_type = 'F' AND nordic_header_main.date = %s AND nordic_header_main.hour = %s AND nordic_header_main.minute = %s AND nordic_header_main.second = %s AND nordic_header_main.epicenter_latitude = %s AND nordic_header_main.epicenter_longitude = %s", values)   
        ans = cur.fetchone()
        if ans is not None:
            self.event_id = cur.fetchone()
        else:
            self.event_id = -1
        self.root_id = -1

    def print_scandia(self):
        print(self.__dict__)

    #TODO: how does this work? What values are allowed to change?
    def does_scandia_exist(self): # RETURN VALUES: 1 - exists but identical, 2 - exist, but not identical, 3 - doesn't exist
        return 1

def return_two_char_int(i):
    if i < 10:
        return '0' + str(i)
    else:
        return str(i)

def return_int(s):
    try:
        return int(s)
    except:
        return None

def return_float(s):
    try:
        if math.isnan(float(s)) or math.isinf(float(s)):
            return None
        return float(s)
    except:
        return None

def return_string(s):
    if s.strip == "":
        return None
    else:
        return s.strip()

def return_date(s):
    try:
        d = date(year=int(s[:4].strip()), 
                month=int(s[5:7].strip()), 
                day=int(s[8:].strip())) 
        return d
    except:
        return None

def validate_scandia(scandia):
    return True

def createScandiaList(scandia):
    scandData = ()

    scandData += (scandia.event_id,)
    scandData += (scandia.source_ref,)
    scandData += (scandia.origin_questionability,)
    scandData += (scandia.year,)
    scandData += (scandia.month,)
    scandData += (scandia.day,)
    scandData += (scandia.hour,)
    scandData += (scandia.minute,)
    scandData += (scandia.second,)
    scandData += (scandia.epicenter_latitude,)
    scandData += (scandia.epicenter_longitude,)
    scandData += (scandia.origin_time_uncertainty,)
    scandData += (scandia.location_uncertainty,)
    scandData += (scandia.focal_depth,)
    scandData += (scandia.depth_identification_code,)
    scandData += (scandia.magnitude_1,)
    scandData += (scandia.magnitude_scale_1,)
    scandData += (scandia.magnitude_2,)
    scandData += (scandia.magnitude_scale_2,)
    scandData += (scandia.magnitude_3,)
    scandData += (scandia.magnitude_scale_3,)
    scandData += (scandia.maximum_intensity,)
    scandData += (scandia.macroseismic_observation_flag,)
    scandData += (scandia.macroseismic_reference,)
    scandData += (scandia.mean_radius_of_area_percetibility,)
    scandData += (scandia.region_code,)
    scandData += (scandia.number_of_stations_used,)
    scandData += (scandia.max_azimuth_gap,)
    scandData += (scandia.min_epicenter_to_station_distance,)

    return scandData

def execute_command(cur, command, vals, scandia):
    try:
        cur.execute(command, vals)
    except psycopg2.Error as e:
        logging.error("Error in sql command: " + command)
        logging.error(e.pgerror)
        logging.error("Exiting file...")
        sys.exit(-1)

def read_scandia_file(f):
    username = usernameUtilities.readUsername()
    scandias = []
    validation = True

    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid!")
        return False

    cur = conn.cursor()

    for line in f:
        if line.strip() != "":
             scandias.append(Scandia(line, cur))

    
    for scandia in scandias:
        if not validate_scandia(scandia):
            return False
            
            
    for scandia in scandias:
            if scandia.event_id == -1:
                cur.execute("INSERT INTO nordic_event_root DEFAULT VALUES")
                cur.execute("SELECT COUNT(*) FROM nordic_event_root")
                root_id = cur.fetchone()[0]
                cur.execute("INSERT INTO nordic_event (root_id, event_type) VALUES (%s, 'S')", (root_id,))
                cur.execute("SELECT COUNT(*) FROM nordic_event")
                scandia.event_id = cur.fetchone()[0]
            else:
                pass
                #If you want to change the header type then uncomment
                #cur.execute("UPDATE nordic_event SET event_type = 'S' WHERE id = %s", (str(scandia.event_id),))
            vals = createScandiaList(scandia)
            execute_command(cur, SCANDIA_INSERT, vals, scandia)
    
    conn.commit()
    conn.close()
    return True
