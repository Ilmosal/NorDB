import sys
import os
import pwd
import datetime
import psycopg2

validation_error = False
eventTypeValues = {"O":1, "A":2, "P":3, "R":4, "F":5, "S":6}

def writeToErrorLog(Error):
	global validation_error
	ferr = open("error.log", 'a')

	if not validation_error:
		validation_error = True
		print ("Error in the Validation!!! Read error.log for more info")
	ferr.write(Error + '\n')

	ferr.close()

def validateEvent(event):
	if len(event.headers) < 1:
		writeToErrorLog("Event Validation Error: No headers on the event_file")
	if len(event.author_id) != 3:
		writeToErrorLog("Event Validation Error: Author id not three characters long! Given: " + event.author_id)

def validateMainHeader(header):
	if validateMainHeaderDate(heaeder.date):
		writeToErrorLog("PLAA")
	if header.distance_indicator not in "LRD ":
		writeToErrorLog("Main Header Validation Error: Wrong character given to distance indicator [LRD ]! Given: " + header.distance_indicator)
	if header.depth_control not in "FS ":
		writeToErrorLog("Main Header Validation Error: Wrong character given to depth_control [FS ]! Given: " + header.depth_control)
	if header.locating_indicator not in "FS ":
		writeToErrorLog("Main Header Validation Error: Wrong character given to locating_indicator [FS ]! Given: " + header.locating_indicator)

def validateMainHeaderDate(date):
	if not is_int(date[0:5]):
		return False
	if not is_int(date[6:8]):
		return False
	

#TODO: validateMacroseismicHeader(header) !!!NOT IMPORTANT!!!
def validateMacroseismicHeader(header):
	pass
#TODO: validateErrorHeader(header) !!!NOT IMPORTANT!!!
def validateErrorHeader(header):
	pass
#TODO: validateCommentHeader(header) !!!NOT IMPORTANT!!!
def validateCommentHeader(header):
	pass
#TODO: validateWaveformHeader(header) !!!NOT THAT IMPORTANT!!!
def validateWaveformHeader(header):
	pass

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


def doesEventExist(header, event_type, cur):
	max_latitude_difference = "0.1"
	max_longitude_difference = "0.1"
	max_second_difference = "10.0"

	if header.epicenter_latitude.strip() == "" or header.epicenter_longitude.strip() == "":
		return None
	
	if header.hour == "  ":
		cur.execute("SELECT event_id FROM nordic_header_main WHERE date = '{0}' AND ABS(epicenter_longitude - {1}) < {2} AND ABS(epicenter_latitude - {3}) < {4};".format(header.date, header.epicenter_longitude, max_longitude_difference, header.epicenter_latitude, max_latitude_difference))	
	elif header.minute == "  ":
		cur.execute("SELECT event_id FROM nordic_header_main WHERE date = '{0}'AND minute IS NULL AND second IS NULL AND hour = {1} AND ABS(epicenter_longitude - {2}) < {3} AND ABS(epicenter_latitude - {4}) < {5};".format(header.date, header.hour, header.epicenter_longitude, max_longitude_difference, header.epicenter_latitude, max_latitude_difference))	
	elif header.second == "  ":
		cur.execute("SELECT event_id FROM nordic_header_main WHERE date = '{0}' AND hour = {1} AND minute = {2} AND second IS NULL AND ABS(epicenter_longitude - {3}) < {4} AND ABS(epicenter_latitude - {5}) < {6};".format(header.date, header.hour, header.minute, header.epicenter_longitude, max_longitude_difference, header.epicenter_latitude, max_latitude_difference))	
	else:	
		cur.execute("SELECT event_id FROM nordic_header_main WHERE date = '{0}' AND hour = {1} AND minute = {2} AND ABS(second - {3}) < {4} AND ABS(epicenter_longitude - {5}) < {6} AND ABS(epicenter_latitude - {7}) < {8};".format(header.date, header.hour, header.minute, header.second, max_second_difference, header.epicenter_longitude, max_longitude_difference, header.epicenter_latitude, max_latitude_difference))	
 
	answers = cur.fetchall()

	if len(answers) < 1:
		return None
	else:
		return answers[0]

def validatePhaseData(phase_data):
	if phase_data.sp_instrument_type not in "SBLHEAZ ":
		writeToErrorLog("Phase Data Validation Error: Wrong type given to sp_instrument_type [SBLHEA ]! Given: " + phase_data.sp_instrument_type)
	if phase_data.sp_component not in "ZNEVH ":
		writeToErrorLog("Phase Data Validation Error: Wrong component given to sp_component [ZNE ]. Given: " + phase_data.sp_component)
	if phase_data.weight not in "0123456789 ":
		writeToErrorLog("Phase Data Validation Error: data weight is not a integer! Given: " + phase_data.weight)
	if phase_data.first_motion not in "+-CD1 ":
		writeToErrorLog("Phase Data Validation Error: Incorrect first motion letter given to first_motion [+-CD ]. Given: " + phase_data.first_motion)
	if phase_data.time_info not in "-+ ":
		writeToErrorLog("Phase Data Validation Error: Incorrect time info letter given to time_info [-+ ]. Given: " + phase_data.time_info)

def removeEvent(event_id, cur):
	cur.execute("SELECT FROM nordic_header_main WHERE event_id = '{0}'".format(event_id))

	h_main_ids = cur.fetchall()

	for h_id in h_main_ids:
		cur.execute("DELETE FROM nordic_header_error WHERE header_id = '{0}'".format(h_id))

	cur.execute("DELETE FROM nordic_header_main WHERE event_id = '{0}'".format(event_id))
	cur.execute("DELETE FROM nordic_header_macroseismic WHERE event_id = '{0}'".format(event_id))
	cur.execute("DELETE FROM nordic_header_comment WHERE event_id = '{0}'".format(event_id))
	cur.execute("DELETE FROM nordic_header_waveform WHERE event_id = '{0}'".format(event_id))
	
	cur.execute("DELETE FROM nordic_event WHERE id = '{0}'".format(event_id))

def validateNordic(nordic_event, cur):
	validateEvent(nordic_event)	

	for header in nordic_event.headers:
		if (header.tpe == 1):
			validateMainHeader(header)
		elif (header.tpe == 2):
			validateMacroseismicHeader(header)
		elif (header.tpe == 3):
			validateCommentHeader(header)
		elif (header.tpe == 5):
			validateErrorHeader(header)
		elif (header.tpe == 6):
			validateWaveformHeader(header)

	for phase_data in nordic_event.data:
		validatePhaseData(phase_data)

	return (not validation_error)
