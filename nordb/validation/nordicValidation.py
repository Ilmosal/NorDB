import sys
import os
import logging

MODULE_PATH = os.path.realpath(__file__)[:-len("nordicValidation.py")]

if __name__=="__main__":
	os.chdir("../..")

from nordb.validation import nordicMainValidation
from nordb.validation import nordicMacroseismicValidation
from nordb.validation import nordicErrorValidation
from nordb.validation import nordicCommentValidation
from nordb.validation import nordicWaveformValidation
from nordb.validation import nordicPhaseDataValidation

from nordb.validation import nordicEventValidation
from nordb.validation import scandiaValidation

eventTypeValues = {"O":1, "A":2, "P":3, "R":4, "F":5, "S":6}

def checkForSameEvents(nordic_event, cur):
	cmd = "SELECT event_id FROM nordic_header_waveform WHERE waveform_info = %s;"
	data = ""
	for h in nordic_event.headers:
		if h.tpe == 6:
			data = h.waveform_info

	if data != "":
		cur.execute(cmd, (data,))
		ans = cur.fetchone()

		if ans:
			return ans[0]
		else:
			return 0
	
	cmd = "SELECT id FROM nordic_header_main WHERE date={0}"
	cmd += "AND minute = {1}"
	cmd += "AND hour = {2}"
	cmd += "AND second = {3}"
	cmd += "AND epicenter_latitude = {4}"
	cmd += "AND epicenter_longitude = {5}"

	cur.execute(cmd, (nordic_event.headers[0].date, 
					nordic_event.headers[0].hour,
					nordic_event.headers[0].minute,
					nordic_event.headers[0].second,
					nordic_event.headers[0].epicenter_latitude,
					nordic_event.headers[0].epicenter_longitude))

	if ans:
		return ans[0]
	else:
		return 0

def checkForSimilarEvents(nordic_event, cur): 
	hour_error = 1
	minute_error = 1
	second_error = 10.0
	epicenter_latitude_error = 0.1
	epicenter_longitude_error = 0.1
	
	cmd = "SELECT id FROM nordic_header_main WHERE date={0}"
	cmd += "AND minute - {1} < {2}"
	cmd += "AND hour - {3} < {4}"
	cmd += "AND second - {5} <{6}"
	cmd += "AND epicenter_latitude - {7} < {8}"
	cmd += "AND epicenter_longitude - {9} < {10}"

	cur.execute(cmd, (nordic_event.headers[0].date, 
					nordic_event.headers[0].hour,
					hour_error,
					nordic_event.headers[0].minute,
					minute_error,
					nordic_event.headers[0].second,
					second_error,
					nordic_event.headers[0].epicenter_latitude,
					epicenter_latititude_error,
					nordic_event.headers[0].epicenter_longitude,
					epicenter_longitude_error))

	if ans:
		return ans[0]
	else:
		return 0


def validateNordic(nordic_event, cur):
	validation_error = False
	if not nordicEventValidation.validateEventHeader(nordic_event):
		validation_error = True

	if nordic_event.headers[0].tpe != 1:
		msg = "Validation Error - Nordic Event: First Header is not of type 1! {0}"
		logging.error(msg.format(nordic_event.headers[0].tpe))
		validation_error = True

	for header in nordic_event.headers:
		if (header.tpe == 1):
			if not nordicMainValidation.validateMainHeader(header):
				validation_error = True
		elif (header.tpe == 2):
			if not nordicMacroseismicValidation.validateMacroseismicHeader(header):
				validation_error = True
		elif (header.tpe == 3):
			if not nordicCommentValidation.validateCommentHeader(header):
				validation_error = True
		elif (header.tpe == 5):
			if not nordicErrorValidation.validateErrorHeader(header):
				validation_error = True
		elif (header.tpe == 6):
			if not nordicWaveformValidation.validateWaveformHeader(header):
				validation_error = True

	for phase_data in nordic_event.data:
		if not nordicPhaseDataValidation.validatePhaseData(phase_data):
			validation_error = True

	old_event_id =  checkForSameEvents(nordic_event, cur)	

	if old_event_id != 0:
		msg = "Old event found with id {0}! Do you want to replace the event? (y/n)\n"
		while True:
			answer = input(msg.format(old_event_id))
			
			if str(answer) == "n":
				validation_error = True
				emsg = "Validation Error - Nordic Event: Event already exists!"
				logging.error(emsg)
				break
			elif str(answer) == "y":
				break

	return not validation_error
