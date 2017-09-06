import sys
import os

if __name__=="__main__":
	os.chdir("../..")

MODULE_PATH = os.path.realpath(__file__)[:-len("nordicValidation.py")]

from nordb.validation import nordicMainValidation
from nordb.validation import nordicMacroseismicValidation
from nordb.validation import nordicErrorValidation
from nordb.validation import nordicCommentValidation
from nordb.validation import nordicWaveformValidation
from nordb.validation import nordicPhaseDataValidation

from nordb.validation import nordicEventValidation
from nordb.validation import scandiaValidation

eventTypeValues = {"O":1, "A":2, "P":3, "R":4, "F":5, "S":6}

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
	return False
	validation_error = False
	nordicEventValidation.validateEvent(nordic_event, va)	
	
	for header in nordic_event.headers:
		if (header.tpe == 1):
			nordicMainValidation.validateMainHeader(header)
		elif (header.tpe == 2):
			nordicMacroseismicValidation.validateMacroseismicHeader(header)
		elif (header.tpe == 3):
			nordicCommentValidation.validateCommentHeader(header)
		elif (header.tpe == 5):
			nordicErrorValidation.validateErrorHeader(header)
		elif (header.tpe == 6):
			nordicWaveformValidation.validateWaveformHeader(header)

	for phase_data in nordic_event.data:
		nordicPhaseDataValidation.validatePhaseData(phase_data)

	return not validation_error
