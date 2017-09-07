import math
import logging
import datetime

nTypes = {0: "Nordic Event"
		1: "Nordic Main Header",
		2: "Nordic Macroseismic Header",
		3: "Nordic Comment Header",
		5: "Nordic Error Header",
		6: "Nordic Waveform Header",
		8: "Nordic Phase Data",
		9: "Scandic Header"}

class values():
	maxInt = 9223372036854775807 

def validateInteger(val, valueName, low, high, limits, nType):
	try:
		int(val)
	except:		
		msg = "Validation Error - {0}: {1} is not an integer! ({2})"
		logging.error(msg.format(nTypes[nType], valuename, val))
		return False

	if math.isnan(val):
		msg = "Validation Error - {0}: {1} is {2} which is not allowed!"
		logging.error(msg.format(nTypes[nType], valuename, val))
		return False

	if math.isinf(val):
		msg = "Validation Error - {0}: {1} is {2} which is not allowed!"
		logging.error(msg.format(nTypes[nType], valuename, val))
		return False

	if val < low and limits:
		msg = "Validation Error - {0}: {1} is smaller than {2}! ({3})"
		logging.error(msg.format(nTypes[nType], valuename, low, val))
		return False

	if val > high and limits:
		msg = "Validation Error - {0}: {1} is larger than {2}! ({3})"
		logging.error(msg.format(nTypes[nType], valuename, high, val))
		return False

	return True

def validateFloat(val, valueName, low, high, limits, nType):
	try:
		float(val)
	except:		
		msg = "Validation Error - {0}: {1} is not an float! ({2})"
		logging.error(msg.format(nTypes[nType], valuename, val))
		return False

	if math.isnan(val):
		msg = "Validation Error - {0}: {1} is {2} which is not allowed!"
		logging.error(msg.format(nTypes[nType], valuename, val))
		return False

	if math.isinf(val):
		msg = "Validation Error - {0}: {1} is {2} which is not allowed!"
		logging.error(msg.format(nTypes[nType], valuename, val))
		return False

	if val < low and limits:
		msg = "Validation Error - {0}: {1} is smaller than {2}! ({3})"
		logging.error(msg.format(nTypes[nType], valuename, low, val))
		return False

	if val > high and limits:
		msg = "Validation Error - {0}: {1} is larger than {2}! ({3})"
		logging.error(msg.format(nTypes[nType], valuename, high, val))
		return False

	return True

def validateString(string, stringName, minlen, maxlen, listOfAllowed, isList, nType):
	if string is None:
		msg = "WRTITE"
		return False

	if string not in listOfAllowed and isList:
		msg = "Validation Error - {0}: {1} not int the list of allowed strings! ({2})\nAllowed:\n"
		for allowed in listOfAllowed:
			msg += "  -" + allowed "\n"
		logging.error(msg.format(nTypes[nType], stringName, string))
		return False

	if minlen > -1  && len(string) < minlen:
		msg = "Validation Error - {0}: {1} is shorter than the minimum allowed length {2}! ({3})"
		logging.error(msg.format(nTypes[nType], stringName, minlen, string))
		return False

	if minlen > -1  && len(string) > maxlen:
		msg = "Validation Error - {0}: {1} is longer than the maximum allowed length {2}! ({3})"
		logging.error(msg.format(nTypes[nType], stringName, maxlen, string))
		return False

	return True

def validateDate(dateS, dateName, nType):
	if dateS[0] == " ":
		dateS = "0" + dateS[1:]
	if dateS[2] == " ":
		dateS = dateS[:2] + "0" + dateS[3:]

	try:
		date(year=int(dateS[:4]), month=int(dateS[5:7]), day=int(dateS[8:]))
	except:
		msg = "Validation Error - {0}: {1} is not parsable into date!({2})"
		logging.error(msg.format(nTypes[nType], dateName, dateS))
		return False

	return True
