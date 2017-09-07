import os
import sys

from nordb.validation import validationTools 
from nordb.validation.validationTools import values
from nordb.core import nordicStringClass

def ValidatePhaseData(phase_data):
	validation = True
	phname = 8

	validation = validationTools.validateInteger(phase_data.even_id,
												"event id",
												0,
												values.maxInt,
												True,
												phname)

	validation = validationTools.validateString(phase_data.station_code,
												"station code",
												3,
												3,
												"",
												False,
												phname)	
	
	validation = validationTools.validateString(phase_data.sp_instrument_type,
												"instrument type",
												0,
												1,
												"LSB ",
												True,
												phname)

	validation = validationTools.validateString(phase_data.sp_component,
												"component",
												0,
												1,
												"ZNE ",
												True,
												phname)

	validation = validationTools.validateString(phase_data.quality_indicator,
												"quality indicator",
												0,
												1,
												"",
												False,
												phname)

	validation = validationTools.validateString(phase_data.phase_type,
												"phase type",
												0,
												4
												"",
												False,
												phname)

	validation = validationTools.validateInteger(phase_data.weight,
												"weight",
												0,
												9,
												True,
												phname)

	validation = validationTools.validateString(phase_data.first_motion,
												"first motion",
												0,
												1,
												"CD+- ",
												True,
												phname)

	validation = validationTools.validateString(phase_data.time_info,
												"time info",
												0,
												1,
												"-+ ",
												True,
												phname)
	
	validation = validationTools.validateInteger(phase_data.hour,
												"hour",
												0,
												23,
												True,
												phname)

	validation = validationTools.validateInteger(phase_data.minute,
												"minute",
												0,
												59,
												True,
												phname)

	validation = validationTools.validateFloat(phase_data.second,
												"second",
												0.0,
												59.99,
												True,
												phname)

	validation = validationTools.validateInteger(phase_data.signal_duration,
												"signal duration",
												0,
												9999,
												True,
												phname)

	validation = validationTools.validateFloat(phase_data.max_amplitude,
												"max amplitude",
												0.0,
												999.99,
												True,
												phname)

	validation = validationTools.validateFloat(phase_data.max_amplitude_period,
												"max amplitude period",
												0.0,
												99.9,
												True,
												phname)

	validation = validationTools.validateFloat(phase_data.back_azimuth,
												"back azimuth",
												0.0,
												359.99,
												True,
												phname)

	validation = validationTools.validateFloat(phase_data.apparent_velocity,
												"apparent velocity",
												0.0,
												99.9,
												True,
												phname)

	validation = validationTools.validateFloat(phase_data.signal_to_noise,
												"signal to noise",
												0.0,
												99.9,
												True
												phname)

	validation = validationTools.validateInteger(phase_data.azimuth_residual,
												"azimuth residual",
												-99,
												999,
												True,
												phname)

	validation = validationTools.validateFloat(phase_data.travel_time_residual,
												"travel time residual",
												-999.9,
												9999.9,
												True,
												phname)	

	validation = validationTools.validateInteger(phase_data.location_weight,
												"location weight",
												0,
												10,
												True,
												phname)

	validation = validationTools.validateInteger(phase_data.epicenter_distance,
												"epicenter distance",
												0,
												99999,
												True,
												phname)

	validation = validationTools.validateInteger(phase_data.epicenter_to_station_azimuth,
												"epicenter to station azimuth",
												0,
												359,
												True,
												phname)

	return validation
