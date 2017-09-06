import psycopg2
import sys
import os
import pwd
import time
from datetime import date
import datetime
import math
import fnmatch
import logging

MODULE_PATH = os.path.realpath(__file__)[:-len("nordic2sql.py")]

if __name__ == "__main__":
	os.chdir("../..")
	sys.path = sys.path + ['']

try:
	f_user = open(MODULE_PATH[:-len("io/")] + "user.config")
	username = f_user.readline()[:-1]
	f_user.close()
except:
	logging.error("No user.config file!! Run the program with -conf flag to initialize the user.conf")
	sys.exit(-1)

from nordb.core.nordicStringClass import *
from nordb.core import nordicFix
from nordb.validation import nordicValidation

authorDict = {"ilmosalm": "---"}

#getting the query information for the nordic data object anf inserting them to its query_info object
def get_data_query_info(data):
	add_to_query_string(data.station_code, "station_code", data.query_info)
	add_to_query_string(data.sp_instrument_type, "sp_instrument_type", data.query_info)
	add_to_query_string(data.sp_component, "sp_component", data.query_info)
	add_to_query_string(data.quality_indicator, "quality_indicator", data.query_info)
	add_to_query_string(data.first_motion, "first_motion", data.query_info)
	add_to_query_string(data.time_info, "time_info", data.query_info)
	add_to_query_string(data.phase_type, "phase_type", data.query_info)

	add_to_query_int(data.event_id, "event_id", data.query_info)
	add_to_query_int(data.weight, "weight", data.query_info)
	add_to_query_int(data.hour, "hour", data.query_info)
	add_to_query_int(data.minute, "minute", data.query_info)
	add_to_query_int(data.signal_duration, "signal_duration", data.query_info)
	add_to_query_int(data.azimuth_residual, "azimuth_residual", data.query_info)
	add_to_query_int(data.location_weight, "location_weight", data.query_info)
	add_to_query_int(data.epicenter_distance, "epicenter_distance", data.query_info)
	add_to_query_int(data.epicenter_to_station_azimuth, "epicenter_to_station_azimuth", data.query_info)

	add_to_query_float(data.second, "second", data.query_info)
	add_to_query_float(data.max_amplitude, "max_amplitude", data.query_info)
	add_to_query_float(data.max_amplitude_period, "max_amplitude_period", data.query_info)
	add_to_query_float(data.apparent_velocity, "apparent_velocity", data.query_info)
	add_to_query_float(data.signal_to_noise, "signal_to_noise", data.query_info)
	add_to_query_float(data.travel_time_residual, "travel_time_residual", data.query_info)
	add_to_query_float(data.back_azimuth, "back_azimuth", data.query_info)	

	#Strip the last two ",  " from the queryInfo object
	data.query_info.strip_info()

#Function for getting the query information from the main header class
def get_main_header_query_info(header):
	add_to_query_date(header.date, "date", header.query_info)

	add_to_query_int(header.event_id, "event_id", header.query_info)
	add_to_query_int(header.hour, "hour", header.query_info)
	add_to_query_int(header.minute, "minute", header.query_info)
	add_to_query_int(header.stations_used, "stations_used", header.query_info)

	add_to_query_float(header.second, "second", header.query_info)
	add_to_query_float(header.epicenter_latitude, "epicenter_latitude", header.query_info)
	add_to_query_float(header.epicenter_longitude, "epicenter_longitude", header.query_info)
	add_to_query_float(header.depth, "depth", header.query_info)
	add_to_query_float(header.rms_time_residuals, "rms_time_residuals", header.query_info)
	add_to_query_float(header.magnitude_1, "magnitude_1", header.query_info)
	add_to_query_float(header.magnitude_2, "magnitude_2", header.query_info)
	add_to_query_float(header.magnitude_3, "magnitude_3", header.query_info)

	add_to_query_string(header.location_model, "location_model", header.query_info)
	add_to_query_string(header.distance_indicator, "distance_indicator", header.query_info)
	add_to_query_string(header.event_desc_id, "event_desc_id", header.query_info)	
	add_to_query_string(header.locating_indicator, "locating_indicator", header.query_info)
	add_to_query_string(header.epicenter_reporting_agency, "epicenter_reporting_agency", header.query_info)
	add_to_query_string(header.type_of_magnitude_1, "type_of_magnitude_1", header.query_info)
	add_to_query_string(header.magnitude_reporting_agency_1, "magnitude_reporting_agency_1", header.query_info)
	add_to_query_string(header.type_of_magnitude_2, "type_of_magnitude_2", header.query_info)
	add_to_query_string(header.magnitude_reporting_agency_2, "magnitude_reporting_agency_2", header.query_info)
	add_to_query_string(header.type_of_magnitude_3, "type_of_magnitude_3", header.query_info)
	add_to_query_string(header.magnitude_reporting_agency_3, "magnitude_reporting_agency_3", header.query_info)

	add_to_query_string(header.depth_control, "depth_control", header.query_info)
	
	#Strip the last two ",  " from the queryInfo object
	header.query_info.strip_info()

#function for getting the query information from the error header class
def get_error_header_query_info(header, header_id):
	add_to_query_int(str(header_id), "header_id", header.query_info)
	add_to_query_int(header.gap, "gap", header.query_info)

	add_to_query_float(header.second_error, "second_error", header.query_info)
	add_to_query_float(header.epicenter_latitude_error, "epicenter_latitude_error", header.query_info)
	add_to_query_float(header.epicenter_longitude_error, "epicenter_longitude_error", header.query_info)
	add_to_query_float(header.depth_error, "depth_error", header.query_info)
	add_to_query_float(header.magnitude_error, "magnitude_error", header.query_info)	
	
	#Strip the last two ",  " from the queryInfo object
	header.query_info.strip_info()

#function for getting the query information from the comment header class
def get_comment_header_query_info(header):
	add_to_query_int(header.event_id, "event_id", header.query_info)

	add_to_query_string(header.h_comment, "h_comment", header.query_info)

	#Strip the last two ",  " from the queryInfo object
	header.query_info.strip_info()

#function for getting query information from the macroseismic header class
def get_macroseismic_header_query_info(header):
	add_to_query_int(header.event_id, "event_id", header.query_info)
	add_to_query_int(header.maximum_observed_intensity, "maximum_observed_intensity", header.query_info)
	add_to_query_int(header.bordering_intensity_1, "bordering_intensity_1", header.query_info)
	add_to_query_int(header.bordering_intensity_2, "bordering_intensity_2", header.query_info)
	
	add_to_query_string(header.description, "description", header.query_info)
	add_to_query_string(header.diastrophism_code, "diastrophism_code", header.query_info)
	add_to_query_string(header.tsunami_code, "tsunami_code", header.query_info)
	add_to_query_string(header.seiche_code, "seiche_code", header.query_info)
	add_to_query_string(header.unusual_effects, "unusual_effects", header.query_info)
	add_to_query_string(header.cultural_effects, "cultural_effects", header.query_info)
	add_to_query_string(header.maximum_intensity_qualifier, "maximum_intensity_qualifier", header.query_info)
	add_to_query_string(header.intensity_scale, "intensity_scale", header.query_info)
	add_to_query_string(header.type_of_magnitude, "type_of_magnitude", header.query_info)
	add_to_query_string(header.quality_rank, "quality_rank", header.query_info)
	add_to_query_string(header.reporting_agency, "reporting_agency", header.query_info)
	
	add_to_query_float(header.macroseismic_latitude, "macroseismic_latitude", header.query_info)
	add_to_query_float(header.macroseismic_longitude, "macroseismic_longitude", header.query_info)
	add_to_query_float(header.macroseismic_magnitude, "macroseismic_magnitude", header.query_info)
	add_to_query_float(header.logarithm_of_radius, "logarithm_of_radius", header.query_info)
	add_to_query_float(header.logarithm_of_area_1, "logarithm_of_area_1", header.query_info)
	add_to_query_float(header.logarithm_of_area_2, "logarithm_of_area_2", header.query_info)

	#Strip the last two ",  " from the queryInfo object
	header.query_info.strip_info()

#function for getting query information from the waveform header class
def get_waveform_header_query_info(header):
	add_to_query_int(header.event_id, "event_id", header.query_info)
	
	add_to_query_string(header.waveform_info, "waveform_info", header.query_info)

	#Strip the last two ",  " from the queryInfo object
	header.query_info.strip_info()

#Adding an integer the the query_info
def add_to_query_int(string, tpe, query_info):
	query_info.query_parameters += tpe + ", "
	query_info.query_values += string + ", "

#Adding a float to the query info
def add_to_query_float(string, tpe, query_info):
	query_info.query_parameters += tpe + ", "
	query_info.query_values += string + ", "

#Adding a string to the query info
def add_to_query_string(string, tpe, query_info):
	#Check if the string is empty
	if (not (string.isspace())):
		query_info.query_parameters += tpe + ", "
		query_info.query_values += "'" + string.strip()+ "', "

#Adding a date to query info
def add_to_query_date(string, tpe, query_info):
	query_info.query_parameters += tpe + ", "
	query_info.query_values += "'" + string + "', "

#function for reading all the headers
def read_headers(nordic, header_id):
	i = 1
	headers = []
	#find where the data starts 
	while (i < len(nordic)):
		if (nordic[i][79] == ' '):
			i+=1
			break
		i+=1

	if (len(nordic) > 1):
		i-=1

	#read the header lines
	for x in range(0, i):
		if (nordic[x][79] == '1'):
			headers.append(NordicHeaderMain(nordic[x], header_id))
		elif (nordic[x][79] == '2'):
			headers.append(NordicHeaderMacroseismic(nordic[x], header_id))
		elif (nordic[x][79] == '3'):
			headers.append(NordicHeaderComment(nordic[x], header_id))
		elif (nordic[x][79] == '5'):
			headers.append(NordicHeaderError(nordic[x]))
		elif (nordic[x][79] == '6'):
			headers.append(NordicHeaderWaveform(nordic[x], header_id))

	return headers
	
#Clearing the database
def reset_database(cur):
	start =  time.time()
	print("Resetting database: ")
	print("-------------------")
	print("Clearing nordic_phase_data...")
	cur.execute("DELETE FROM nordic_phase_data")
	print("Clearing nordic_header_comment...")
	cur.execute("DELETE FROM nordic_header_comment")	
	print("Clearing nordic_header_error...")
	cur.execute("DELETE FROM nordic_header_error")
	print("Clearing nordic_header_macroseismic...")
	cur.execute("DELETE FROM nordic_header_macroseismic")	
	print("Clearing nordic_header_waveform...")
	cur.execute("DELETE FROM nordic_header_waveform")
	print("Clearing nordic_header_main...")
	cur.execute("DELETE FROM nordic_header_main")	
	print("Clearing nordic_modified...")
	cur.execute("DELETE FROM nordic_modified")	
	print("Clearing scandia_header")
	cur.execute("DELETE FROM scandia_header")
	print("Clearing nordic_event")
	cur.execute("DELETE FROM nordic_event")
	print("Clearing nordic_file")
	cur.execute("DELETE FROM nordic_file")
	print("Clearing nordic_event_root")
	cur.execute("DELETE FROM nordic_event_root")

	print ("Altering sequence ids")
	cur.execute("ALTER SEQUENCE nordic_event_root_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE nordic_file_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE nordic_event_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE nordic_modified_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE scandia_header_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE nordic_phase_data_id_seq RESTART WITH 1")	
	cur.execute("ALTER SEQUENCE nordic_header_main_id_seq RESTART WITH 1")	
	cur.execute("ALTER SEQUENCE nordic_header_comment_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE nordic_header_error_id_seq RESTART WITH 1")	
	cur.execute("ALTER SEQUENCE nordic_header_macroseismic_id_seq RESTART WITH 1")	
	cur.execute("ALTER SEQUENCE nordic_header_waveform_id_seq RESTART WITH 1")	
	
	end = time.time()

	print("All done! Time taken: {0} seconds!".format(end))

#TODO: DO THIS AGAIN!!!
#function for reading one event and pushing it to the database
def read_event(nordic, cur, event_type, nordic_filename):
	#Getting the nordic_event id from the database
	if not nordic:
		return False

	#Getting the root_id and event_id 
	cur.execute("SELECT COUNT(*) FROM nordic_event_root;")
	root_id = 1 + cur.fetchone()[0]
	cur.execute("SELECT COUNT(*) FROM nordic_event;")
	event_id = 1 + cur.fetchone()[0]
	header_id = -1
	
	#Reading headers and data 
	headers = read_headers(nordic, event_id)
	data = []

	#Reading the waveform info for searching for same nordics in the database
	waveform_info = ""
	for header in headers:
		if header.tpe == 6:
			waveform_info = header.waveform_info.strip()

	cur.execute("SELECT root_id FROM nordic_event, nordic_header_waveform WHERE nordic_event.id = nordic_header_waveform.event_id AND nordic_header_waveform.waveform_info LIKE %s", (waveform_info,))
	ans = cur.fetchone()

	if ans is not None:
		root_id = ans[0]

	#Check if there is a event that shares the event event_type if this event could replace the old event
	cur.execute("SELECT event_type, id FROM nordic_event WHERE root_id = %s", (str(root_id),))
	common_events = cur.fetchall()
	
	update_this_event = -1
	for event in common_events:
		if event[0] == event_type and nordicValidation.eventTypeValues[event_type] > 3:
			update_this_event = event[1]

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
		data.append(NordicData(nordic[x], event_id))

	#Generate the event
	nordic_event = NordicEvent(event_id, root_id, headers, data, event_type, author_id, "NOPROGRAM")

	#VALIDATE THE DATA BEFORE PUSHING INTO THE DATABASE. DONT PUT ANYTHING TO THE DATABASE BEFORE THIS
	if not nordicValidation.validateNordic(nordic_event, cur):
		return False
	else:
		return True		

		if ans is None:
			cur.execute("INSERT INTO nordic_event_root DEFAULT VALUES;")

		if filename_id == -1:
			cur.execute("SELECT COUNT(*) FROM nordic_file")
			filename_id = 1 + cur.fetchone()[0]
			cur.execute("INSERT INTO nordic_file (file_location) VALUES (%s)", (nordic_filename,))

		#Add a new nordic_event to the db
		cur.execute("INSERT INTO nordic_event (event_type, root_id, nordic_file_id, author_id) VALUES (%s, %s, %s, %s)", 
					(nordic_event.event_type, 
					root_id, 
					str(filename_id), 
					nordic_event.author_id)
					)
	
		if update_this_event != -1:
			cur.execute("INSERT INTO nordic_modified (event_id, replacement_event_id, old_event_type, replaced) VALUES (%s, %s, %s, %s)", 
						(str(update_this_event), 
						str(event_id), 
						event_type, 
						'{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),)
						)
			cur.execute("UPDATE nordic_event SET event_type = 'O' WHERE id = %s", (str(update_this_event),))

		#Add all the headers to the database
		for header in nordic_event.headers:
			if (header.tpe == 1):
				get_main_header_query_info(header)
				command = "INSERT INTO nordic_header_main (" + header.query_info.query_parameters + ") VALUES (" + header.query_info.query_values + ");"
				cur.execute("SELECT COUNT(*) FROM nordic_header_main;")
				header_id = cur.fetchone()[0] + 1
				execute_command(cur, command, nordic)
			elif (header.tpe == 2):
				get_macroseismic_header_query_info(header)
				command = "INSERT INTO nordic_header_macroseismic (" + header.query_info.query_parameters + ") VALUES (" + header.query_info.query_values + ");"
				execute_command(cur, command, nordic)
			elif (header.tpe == 3):
				get_comment_header_query_info(header)
				command = "INSERT INTO nordic_header_comment (" + header.query_info.query_parameters + ") VALUES (" + header.query_info.query_values + ");"
				execute_command(cur, command, nordic)
			elif (header.tpe == 5):
				get_error_header_query_info(header, header_id)
				command = "INSERT INTO nordic_header_error (" + header.query_info.query_parameters + ") VALUES (" + header.query_info.query_values + ");"
				execute_command(cur, command, nordic)
			elif (header.tpe == 6):
				get_waveform_header_query_info(header)
				command = "INSERT INTO nordic_header_waveform (" + header.query_info.query_parameters + ") VALUES (" + header.query_info.query_values + ");"
				execute_command(cur, command, nordic)

		#Adding the data to the database
		for phase_data in nordic_event.data:
			get_data_query_info(phase_data)		
			command = "INSERT INTO nordic_phase_data (" + phase_data.query_info.query_parameters + ") VALUES (" + phase_data.query_info.query_values + ");"
			execute_command(cur, command, nordic)

		return True

#function for performing the sql commands
def execute_command(cur, command, nordic):
		try:
			cur.execute(command)
		except:
			logging.error("Error in sql command: " + command)
			sys.exit()

#function for reading a nordicp file
def read_nordicp(f, event_type, old_nordic):
	nordics = nordicFix.read_fix_nordicp_file(f, old_nordic)

	try:
		conn = psycopg2.connect("dbname = nordb user={0}".format(username))
	except:
		logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid!")
		return 

	cur = conn.cursor()

	for nordic in nordics:
		if not read_event(nordic, cur, event_type, f.name):
			if len(nordic) > 0:
				logging.error("Problem in nordic: " + nordic[0][1:20])
	
	conn.commit()
	conn.close()

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

