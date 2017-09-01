import psycopg2
import sys
import os
import pwd
import time
from datetime import date
import datetime
import math
import fnmatch

import nordicfix

sys.path.insert(0, 'validationLibraries')

import nordicValidation

authorDict = {"ilmosalm": "---"}
validation_error = False

class NordicEvent:
	def __init__(self, event_id, root_id, headers, data, event_type, author_id, locating_program):
		self.event_id = event_id
		self.root_id = root_id
		self.headers = headers
		self.data = data
		self.event_type = event_type
		self.author_id = author_id
		self.locating_program = locating_program

#Class for header lines of the nordic file. Other headers will inherit this class
class NordicHeader:
	def __init__(self, tpe):
		self.tpe = tpe
		self.query_info = QueryInfo()

	#function for getting the header type
	def get_header_type(self):
		return self.tpe

#Class for nordic data lines of the nordic file.
class NordicData:
	def __init__(self, data, event_id):
		self.event_id = str(event_id)
		self.station_code = data[1:5]
		self.sp_instrument_type = data[6]
		self.sp_component = data[7]
		self.quality_indicator = data[9]
		self.phase_type = data[10:14]
		self.weight = data[14]
		self.first_motion = data[16]
		self.time_info = data[17]
		self.hour = data[18:20]
		self.minute = data[20:22]
		self.second = data[23:28]
		self.signal_duration = data[29:33]
		self.max_amplitude = data[34:40]
		self.max_amplitude_period = data[41:45]
		self.back_azimuth = data[46:52]
		self.apparent_velocity = data[52:56]
		self.signal_to_noise = data[56:60]
		self.azimuth_residual = data[60:63]
		self.travel_time_residual = data[63:68]
		self.location_weight = data[68:70]
		self.epicenter_distance = data[70:75]
		self.epicenter_to_station_azimuth = data[76:79]

		#Creating the query information object for the class
		self.query_info = QueryInfo()

#Class for nordic header line of type 1. Contains main information from the event.
class NordicHeaderMain(NordicHeader):
	def __init__(self, header, event_id):
		NordicHeader.__init__(self, 1)
		self.event_id = str(event_id)
		self.date = header[1:5] + "-" + header[5:7] + "-" + header[7:9]
		self.hour = header[11:13]
		self.minute = header[13:15]
		self.second = header[16:20]
		self.location_model = header[20]
		self.distance_indicator = header[21]
		self.event_desc_id = header[22]
		self.epicenter_latitude = header[23:30]
		self.epicenter_longitude = header[30:38]
		self.depth = header[38:43]
		self.depth_control = header[43]
		self.locating_indicator = header[44]
		self.epicenter_reporting_agency = header[45:48] 
		self.stations_used = header[48:51]
		self.rms_time_residuals = header[51:55]
		self.magnitude_1 = header[56:59]
		self.type_of_magnitude_1 = header[59]
		self.magnitude_reporting_agency_1 = header[60:63]
		self.magnitude_2 = header[64:67]
		self.type_of_magnitude_2 = header[67]
		self.magnitude_reporting_agency_2 = header[68:71]
		self.magnitude_3 = header[72:75]
		self.type_of_magnitude_3 = header[75]
		self.magnitude_reporting_agency_3 = header[76:79]

#Class for the nordic header line of type 2. Contains macroseismic information of the event
class NordicHeaderMacroseismic(NordicHeader):
	def __init__(self, header, event_id):
		NordicHeader.__init__(self, 2)	
		self.description = header[5:20]
		self.diastrophism_code = header[22]
		self.tsunami_code = header[23]
		self.seiche_code = header[24]
		self.cultural_effects = header[25]
		self.unusual_effects = header[26]
		self.maximum_observed_intensity = header[27:29]
		self.maximum_intensity_qualifier = header[29]
		self.intensity_scale = header[30:32]
		self.macroseismic_latitude = header[33:39]
		self.macroseismic_longitude = header[40:47]
		self.macroseismic_magnitude = header[48:51]
		self.type_of_magnitude = header[52]
		self.logarithm_of_radius = header[52:56]
		self.logarithm_of_area_1 = header[56:61]
		self.bordering_intensity_1 = header[61:63]
		self.logarithm_of_area_2 = header[63:68]
		self.bordering_intensity_2 = header[68:70]
		self.quality_rank = header[72]
		self.reporting_agency = header[72:75]
		self.event_id = str(event_id)

#Class for the nordic header line of type 3. Contains comments of the header file
class NordicHeaderComment(NordicHeader):
	def __init__(self, header, event_id):
		NordicHeader.__init__(self, 3)
		self.h_comment = header[1:79]
		self.event_id = str(event_id)

#Class for the nordic header line of type 5. Contains error information of the main header
class NordicHeaderError(NordicHeader):
	def __init__(self, header):
		NordicHeader.__init__(self, 5)
		self.gap = header[5:8]
		self.second_error = header[16:20]
		self.epicenter_latitude_error = header[24:30]
		self.epicenter_longitude_error = header[31:38]
		self.depth_error = header[40:43]
		self.magnitude_error = header[56:59]
		self.header_id = '-1'

#Class for the nordic header line of type 6. Contains the waveform information of the header file
class NordicHeaderWaveform(NordicHeader):
	def __init__(self, header, event_id):
		NordicHeader.__init__(self, 6)
		self.event_id = str(event_id)
		self.waveform_info = header[1:79]

#Class containing the sql query information of the for sql inserts.
class QueryInfo:
	def __init__(self):
		self.query_parameters = ""
		self.query_values = ""
	
	#method for stripping the last two letters from the query string. Useful for getting rid of additional ", " after parsing the information
	def strip_info(self):
		self.query_parameters = self.query_parameters[:-2]
		self.query_values = self.query_values[:-2]

#method that determines if string s is parseable to sql int
def is_int(s):
	try:
		int(s.strip())
		return True	
	except:
		return False

#method that determines if string s is parseable to sql float
def is_float(s):
	try:
		#SQL doesn't do inf or nAn so remove those
		if (math.isnan(float(s))):
			return False
		if (math.isinf(float(s))):
			return False
		float(s.strip())
		return True	
	except:
		return False

#method that determines if string s is parseable to sql date
def is_date(s):
	try:
		date(year=int(s[:4]), month=int(s[5:7]), day=int(s[8:]))
		return True
	except:
		return False

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
	for x in xrange(0, i):
		if len(nordic[x]) < 80:
			print nordic[x] + "  \n len: " + str(len(nordic[x]))
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
	print "Resetting database: "
	print "-------------------"
	print "Clearing nordic_phase_data..."
	cur.execute("DELETE FROM nordic_phase_data")
	print "Clearing nordic_header_comment..."
	cur.execute("DELETE FROM nordic_header_comment")	
	print "Clearing nordic_header_error..."
	cur.execute("DELETE FROM nordic_header_error")
	print "Clearing nordic_header_macroseismic..."
	cur.execute("DELETE FROM nordic_header_macroseismic")	
	print "Clearing nordic_header_waveform..."
	cur.execute("DELETE FROM nordic_header_waveform")
	print "Clearing nordic_header_main..."
	cur.execute("DELETE FROM nordic_header_main")	
	print "Clearing nordic_modified..."
	cur.execute("DELETE FROM nordic_modified")	
	print "Clearing scandia_header"
	cur.execute("DELETE FROM scandia_header")
	print "Clearing nordic_event"
	cur.execute("DELETE FROM nordic_event")
	print "Clearing nordic_file"
	cur.execute("DELETE FROM nordic_file")
	print "Clearing nordic_event_root"	
	cur.execute("DELETE FROM nordic_event_root")

	print "Altering sequence ids"
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

	print "All done! Time taken: " +  str(end - start) + " seconds!"

#function for reading one event and pushing it to the database
def read_event(nordic, cur, event_type, author_id, nordic_filename):
	#Getting the nordic_event id from the database
	if (len(nordic) < 1):
		return False

	cur.execute("SELECT COUNT(*) FROM nordic_event_root;")
	root_id = 1 + cur.fetchone()[0]
	cur.execute("SELECT COUNT(*) FROM nordic_event;")
	event_id = 1 + cur.fetchone()[0]
	header_id = -1
	
	#Reading headers and data 
	headers = read_headers(nordic, event_id)
	data = []

	waveform_info = ""

	for header in headers:
		if header.tpe == 6:
			waveform_info = header.waveform_info.strip()

	cur.execute("SELECT root_id FROM nordic_event, nordic_header_waveform WHERE nordic_event.id = nordic_header_waveform.event_id AND nordic_header_waveform.waveform_info LIKE %s", (waveform_info,))
	ans = cur.fetchone()

	if ans is not None:
		root_id = ans[0]

	cur.execute("SELECT event_type, id FROM nordic_event WHERE root_id = %s", (str(root_id),))
	common_events = cur.fetchall()
	
	update_this_event = -1
	for event in common_events:
		if event[0] == event_type and nordicValidation.eventTypeValues[event_type] > 3:
			update_this_event = event[1]

	for header in headers:
		if header.tpe == 3:
			if fnmatch.fnmatch(header.h_comment, "*(???)*"):
				for x in xrange(0, len(header.h_comment)-4):
					if header.h_comment[x] == '(' and header.h_comment[x+4] == ')':
						author_id = header.h_comment[x+1:x+4]

	filename_id = -1
	cur.execute("SELECT id FROM nordic_file WHERE file_location = %s", (nordic_filename,))
	filenameids = cur.fetchone()
	if filenameids is not None:
		filename_id = filenameids[0]

	for x in xrange(len(headers), len(nordic)):
		data.append(NordicData(nordic[x], event_id))

	nordic_event = NordicEvent(event_id, root_id, headers, data, event_type, author_id, "NOPROGRAM")

	#VALIDATE THE DATA BEFORE PUSHING INTO THE DATABASE. DONT PUT ANYTHING TO THE DATABASE BEFORE THIS
	if not nordicValidation.validateNordic(nordic_event, cur):
		return False
	else:
		if ans is None:
			cur.execute("INSERT INTO nordic_event_root DEFAULT VALUES;")

		if filename_id == -1:
			cur.execute("SELECT COUNT(*) FROM nordic_file")
			filename_id = 1 + cur.fetchone()[0]
			cur.execute("INSERT INTO nordic_file (file_location) VALUES (%s)", (nordic_filename,))

		#Add a new nordic_event to the db
		cur.execute("INSERT INTO nordic_event (event_type, root_id, nordic_file_id, author_id) VALUES (%s, %s, %s, %s)", (nordic_event.event_type, root_id, str(filename_id), nordic_event.author_id))
	
		if update_this_event != -1:
			cur.execute("INSERT INTO nordic_modified (event_id, replacement_event_id, old_event_type, replaced) VALUES (%s, %s, %s, %s)", (str(update_this_event), str(event_id), event_type, '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),))
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
			print "Error in sql command: " + command
			for line in nordic:
				print line
			print "Exiting file.."
			sys.exit()

#function for reading a nordicp file
def read_nordicp(f, cur, event_type, author_id, old_nordic):
	nordics = nordicfix.read_fix_nordicp_file(f, old_nordic)

	for nordic in nordics:
		if not read_event(nordic, cur, event_type, author_id, f.name):
			if len(nordic) > 0:
				print "Problem in nordic: " + nordic[0][1:20]

#function for getting the authorID of the last person who edited the file
def get_author(filename):
	try:
		author_id = pwd.getpwuid(os.stat(filename).st_uid).pw_name
		if author_id in authorDict:
			return authorDict[author_id]
		else:
			return "---"
	except:
		print "Filename given to get Author is false"
		return "---"

if __name__ == "__main__":
	open("error.log", 'w').close()

	#Test if the user has given an argument for the program1
	if (len(sys.argv) < 2):
		print "Give a filename for the program!!"
		sys.exit()

	#resetting the database with 'reset' argument
	if (sys.argv[1] == "reset"):
		#initializing psycopg
		conn = psycopg2.connect("dbname=test user=ilmosalm")
		#function for reading one event and pushing it to the database)
		cur = conn.cursor()

		reset_database(cur)
		conn.commit()
		conn.close()
		sys.exit()

	if (len(sys.argv) < 3):
		print "Give the event type for the program: 'F' - final, 'R' - reviewed,'P' - preliminary, 'A' - automatic, 'O' - other"
		sys.exit()

	if sys.argv[2] not in "FRPAO":
		print "Event type not correct: 'F' - final, 'R' - revieved, 'P' - preliminary, 'A' - automatic, 'O' - other"
		sys.exit()

	old_nordic = False

	if (len(sys.argv) > 3):
		if sys.argv[3] == 'O':
			print "Nordic file is old"
			old_nordic = True

	author_id = get_author(sys.argv[1].strip())

	#opening the given line
	try:
		f = open(sys.argv[1], 'r') 
	except:
		print("File: " + sys.argv[1] + " not found!")
		sys.exit()

	#initializing psycopg
	conn = psycopg2.connect("dbname=test user=ilmosalm")
	#function for reading one event and pushing it to the database)
	cur = conn.cursor()

	#print the file
	print f.name

	read_nordicp(f, cur, sys.argv[2], author_id, old_nordic)
		
	#committing and closing psycopq	
	f.close()
	conn.commit()
	conn.close()
