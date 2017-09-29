import sys
import psycopg2
import math

from nordic2sql import QueryInfo
from nordic2sql import add_to_query_string
from nordic2sql import add_to_query_float
from nordic2sql import add_to_query_int
from nordic2sql import execute_command

SCANDIA_INSERT = "INSERT INTO () VALUES ();"

class Scandia:
	def __init__(self, scandia_line, scandia_id, cur):
		self.scandia_id = scandia_id
		self.source_ref = return_string(scandia_line[0:3])
		self.origin_questionability = return_string(scandia_line[3]) 
		self.year = return_int(scandia_line[4:8])
		self.month = return_int(scandia_line[8:10])
		self.day = return_int(scandia_line[10:12])
		self.event_desc = return_string(scandia_line[12]) 
		self.hour = return_int(scandia_line[13:15])
		self.minute = return_int(scandia_line[15:17])
		self.second = return_float(scandia_line[17:21].strip())
		self.epicenter_latitude = return_float(scandia_line[21:29])
		self.epicenter_longitude = return_float(scandia_line[29:36]) 
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
		self.query_info = QueryInfo()
		values = (str(self.year) + "-" + str(return_two_char_int(self.month)) + "-" + str(return_two_char_int(self.day)), self.hour, self.minute, self.second, self.epicenter_latitude, self.epicenter_longitude)

		cur.execute("SELECT event_id FROM nordic_header_main, nordic_event WHERE nordic_event.id = nordic_header_main.event_id AND nordic_event.event_type = 'F' AND nordic_header_main.date = %s AND nordic_header_main.hour = %s AND nordic_header_main.minute = %s AND nordic_header_main.second = %s AND nordic_header_main.epicenter_latitude = %s AND nordic_header_main.epicenter_longitude = %s", values)	
		ans = cur.fetchone()
		if ans is not None:
			self.event_id = cur.fetchone()
		else:
			self.event_id = -1
		self.root_id = -1

	def print_scandia(self):
		print self.__dict__

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

def validate_scandia(scandia):
	return True

def make_scandia_query(scandia):
	add_to_query_string(scandia.source_ref, "source_ref", scandia.query_info)
	add_to_query_string(scandia.event_desc, "event_desc", scandia.query_info)
	add_to_query_string(scandia.origin_time_uncertainty, "origin_time_uncertainty", scandia.query_info)
	add_to_query_string(scandia.location_uncertainty, "location_uncertainty", scandia.query_info)
	add_to_query_string(scandia.depth_identification_code, "depth_identification_code", scandia.query_info)
	add_to_query_string(scandia.magnitude_scale_1, "magnitude_scale_1", scandia.query_info)
	add_to_query_string(scandia.magnitude_scale_2, "magnitude_scale_2", scandia.query_info)
	add_to_query_string(scandia.magnitude_scale_3, "magnitude_scale_3", scandia.query_info)
	add_to_query_string(scandia.maximum_intensity, "maximum_intensity", scandia.query_info)
	add_to_query_string(scandia.macroseismic_observation_flag, "macroseismic_observation_flag", scandia.query_info)
	add_to_query_string(scandia.macroseismic_reference, "macroseismic_reference", scandia.query_info)
	add_to_query_string(scandia.region_code, "region_code", scandia.query_info)
	add_to_query_string(scandia.max_azimuth_gap, "max_azimuth_gap", scandia.query_info)
	add_to_query_string(scandia.min_epicenter_to_station_distance, "min_epicenter_to_station_distance", scandia.query_info)

	add_to_query_int(str(scandia.event_id), "event_id", scandia.query_info)
	add_to_query_int(str(scandia.year), "year", scandia.query_info)
	add_to_query_int(str(scandia.month), "month", scandia.query_info)
	add_to_query_int(str(scandia.day), "day", scandia.query_info)
	add_to_query_int(str(scandia.hour), "hour", scandia.query_info)
	add_to_query_int(str(scandia.minute), "minute", scandia.query_info)
	add_to_query_int(str(scandia.focal_depth), "focal_depth", scandia.query_info)
	add_to_query_int(str(scandia.mean_radius_of_area_percetibility), "mean_radius_of_area_percetibility", scandia.query_info)

	add_to_query_float(str(scandia.second), "second", scandia.query_info)
	add_to_query_float(str(scandia.epicenter_latitude), "epicenter_latitude", scandia.query_info)
	add_to_query_float(str(scandia.epicenter_longitude), "epicenter_longitude", scandia.query_info)
	add_to_query_float(str(scandia.magnitude_1), "magnitude_1", scandia.query_info)
	add_to_query_float(str(scandia.magnitude_2), "magnitude_2", scandia.query_info)
	add_to_query_float(str(scandia.magnitude_3), "magnitude_3", scandia.query_info)

	scandia.query_info.strip_info()

def execute_command(cur, command, scandia):
	try:
		cur.execute(command)
	except:
		print "Error in sql command: " + command
		print scandia.print_scandia()
		print "Exiting file..."
		sys.exit()

def read_scandia_file(f, cur):
	scandias = []
	scandia_id = 0
	event_id = 0
	validation = True

	for line in f:
		if line.strip() != "":
			 scandias.append(Scandia(line, scandia_id, cur))

	
	for scandia in scandias:
		if not validate_scandia(scandia):
			validation = False
			
	if validation:
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

				make_scandia_query(scandia)

				command = "INSERT INTO scandia_header (" + scandia.query_info.query_parameters + ") VALUES (" + scandia.query_info.query_values + ")" 
				execute_command(cur, command, scandia)

	return validation

if __name__ == "__main__":
	if (len(sys.argv) < 2):
		print("No filenames given!!")
		sys.exit() 

	try: 
		f = open(sys.argv[1], 'r')
	except:
		print("File: " + sys.argv[1] + "not found!")
		sys.exit()

	conn = psycopg2.connect("dbname=test user=ilmosalm")
	cur = conn.cursor()
	
	read_scandia_file(f, cur)

	f.close()
	conn.commit()
	conn.close()
