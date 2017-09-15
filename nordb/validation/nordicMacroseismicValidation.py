import os
import sys

if __name__=="__main__":
	os.chdir("../..")

from nordb.validation import validationTools 
from nordb.validation.validationTools import values

def validateMacroseismicHeader(nordic_event):
	validation = True
	mheader = 2

	if not validationTools.validateInteger(nordic_event.event_id,
											"event id", 
											0,
											values.maxInt,
											True,
											mheader):
		validation = False

	if not validationTools.validateString(nordic_event.description,
											"description",
											0,
											15,
											"",
											False,
											mheader):
		validation = False

	if not validationTools.validateString(nordic_event.diastrophism_code,
											"diastrophism code",
											0,
											1,
											"FUD ",
											True,
											mheader):
		validation = False

	if not validationTools.validateString(nordic_event.tsunami_code,
											"tsunami code",
											0,
											1,
											"TQ ",
											True,
											mheader):
		validation = False

	if not validationTools.validateString(nordic_event.seiche_code,
											"seiche code",
											0,
											1,
											"SQ ",
											True,
											mheader):
		validation = False

	if not validationTools.validateString(nordic_event.cultural_effects,
											"cultural effects",
											0,
											1,
											"CDFH ",
											True,
											mheader):
		validation = False

	if not validationTools.validateString(nordic_event.unusual_effects,
											"unusual effects",
											0,
											1,
											"LGSBCVOM ",
											True,
											mheader):
		validation = False

	if not validationTools.validateInteger(nordic_event.maximum_observed_intensity,
											"maximum observed intensity",
											0,
											20,
											True,
											mheader):
		validation = False

	if not validationTools.validateString(nordic_event.maximum_intensity_qualifier,
											"maximum intensity qualifier",
											0,
											1,
											"+- ",
											True,
											mheader):
		validation = False

	if not validationTools.validateString(nordic_event.intensity_scale,
											"intensity scale",
											0,
											2,
											{"MM", "RF", "CS", "SK"},
											True,
											mheader):
		validation = False

	if not validationTools.validateFloat(nordic_event.macroseismic_latitude,
											"macroseismic latitude",
											-90.0,
											90.0,
											True,
											mheader):
		validation = False

	if not validationTools.validateFloat(nordic_event.macroseismic_longitude,
											"macroseismic longitude",
											-180.0,
											180.0,
											True,
											mheader):
		validation = False

	if not validationTools.validateFloat(nordic_event.macroseismic_magnitude,
											"macroseismic magnitude",
											0.0,
											20.0,
											True,
											mheader):
		validation = False

	if not validationTools.validateString(nordic_event.type_of_magnitude,
											"type of magnitude",
											0,
											1,
											"IAR* ",
											True,
											mheader):
		validation = False

	if not validationTools.validateFloat(nordic_event.logarithm_of_radius,
											"logarithm of radius",
											0.0,
											99.9,
											True,
											mheader):
		validation = False

	if not validationTools.validateFloat(nordic_event.logarithm_of_area_1,
											"logarithm of area 1",
											0.0,
											99.99,
											True,
											mheader):
		validation = False

	if not validationTools.validateInteger(nordic_event.bordering_intensity_1,
											"bordering intensity 1",
											0,
											99,
											True,
											mheader):
		validation = False

	if not validationTools.validateFloat(nordic_event.logarithm_of_area_2,
											"logarithm of area 2",
											0.0,
											99.99,
											True,
											mheader):
		validation = False

	if not validationTools.validateInteger(nordic_event.bordering_intensity_2,
											"bordering intensity 2",
											0,
											99,
											True,
											mheader):
		validation = False

	if not validationTools.validateString(nordic_event.reporting_agency,
											"reporting agency",
											3,
											3,
											"",
											True,
											mheader):
		validation = False

	return validation	
