import psycopg2

#class for the whole event 
class NordicEvent:
	def __init__(self, headers, phase_data):
		self.headers = headers
		self.phase_data = phase_data	
	
	def get_main_headers(self):
		return self.headers[1]

	def get_macroseismic_header(self):
		return self.headers[2]

	def get_comment_headers(self):
		return self.headers[3]

	def get_error_headers(self):
		return self.headers[5]

	def get_waveform_headers(self):
		return self.headers[6]

#Parent class for the header
class NordicHeader:
	def __init__(self, header_type):
		self.header_type = header_type
	
	def get_header_type(self):
		return self.header_type

class NordicPhaseData:
	def __init__(self, query_result):
		self.phase_id = query_result[0]
		self.event_id = query_result[1]
		self.station_code = query_result[2]
		self.sp_instrument_type = query_result[3]
		self.sp_component = query_result[4]
		self.quality_indicator = query_result[5]
		self.phase_type = query_result[6]
		self.weight = query_result[7]
		self.first_motion = query_result[8]
		self.time_info = query_result[9]
		self.hour = query_result[10]
		self.minute = query_result[11]
		self.second = query_result[12]
		self.signal_duration = query_result[13]
		self.max_amplitude= query_result[14]
		self.max_amplitude_period = query_result[15]
		self.back_azimuth = query_result[16]
		self.apparent_velocity = query_result[17]
		self.signal_to_noise = query_result[18]
		self.azimuth_residual = query_result[19]
		self.travel_time_residual = query_result[20]
		self.location_weight = query_result[21]
		self.epicenter_distance = query_result[22] 
		self.epicenter_to_station_azimuth = query_result[23]

	def return_as_string(self):
		output_string = ""
		return output_string

class NordicHeaderMain(NordicHeader):
	def __init__(self, query_result):
		NordicHeader.__init__(self, 1)
		self.header_id = query_result[0]
		self.event_id = query_result[1]
		self.date = query_result[2]
		self.hour = query_result[3]
		self.minute = query_result[4]
		self.second =  query_result[5]
		self.location_model =  query_result[6]
		self.distance_indicator = query_result[7]
		self.event_desc_id = query_result[8]
		self.epicenter_latitude = query_result[9]
		self.epicenter_longitude = query_result[10]
		self.depth = query_result[11]
		self.depth_control = query_result[12]
		self.locating_indicator = query_result[13]
		self.epicenter_reporting_agency = query_result[14]
		self.stations_used = query_result[15]
		self.rms_time_residuals = query_result[16]
		self.magnitude_1 = query_result[17]
		self.type_of_magnitude_1 = query_result[18]
		self.magnitude_reporting_agency_1 = query_result[19]
		self.magnitude_2 = query_result[20]
		self.type_of_magnitude_2 = query_result[21]
		self.magnitude_reporting_agency_2 = query_result[22]
		self.magnitude_3 = query_result[23]
		self.type_of_magnitude_3 = query_result[24]
		self.magnitude_reporting_agency_3 = query_result[25]

	def return_as_string(self):
		output_string = ""
		return output_string

	
class NordicHeaderMacroseismic(NordicHeader):
	def __init__(self):
		NordicHeader.__init__(self, 2)
		self.header_id = query_result[0]
		self.event_id = query_result[1]
		self.description = query_result[2]
		self.diastrophism_code = query_result[3]
		self.tsunami_code = query_result[4]
		self.seiche_code = query_result[5]
		self.cultural_effects = query_result[6]
		self.unusual_effects = query_result[7]
		self.maximum_observed_intensity = query_result[8]
		self.maximum_intensity_qualifier = query_result[9]
		self.intensity_scale = query_result[10]
		self.macroseismic_latitude = query_result[11]
		self.macroseismic_longitude = query_result[12]
		self.macroseismic_magnitude = query_result[13]
		self.type_of_magnitude = query_result[14]
		self.logarithm_of_radius = query_result[15]
		self.logarithm_of_area_1 = query_result[16]
		self.bordering_intensity_1 = query_result[17]
		self.logarithm_of_area_2 = query_result[18]
		self.bordering_intensity_2 = query_result[19]
		self.quality_rank = query_result[20]
		self.reporting_agency = query_result[21]

	def return_as_string(self):
		output_string = ""
		return output_string


class NordicHeaderComment(NordicHeader):
	def __init__(self, query_result):
		NordicHeader.__init__(self, 3)
		self.header_id = query_result[0]
		self.event_id = query_result[1]
		self.h_comment = query_result[2]

	def return_as_string(self):
		output_string = ""
		return output_string


class NordicHeaderError(NordicHeader):
	def __init__(self, query_result):
		NordicHeader.__init__(self, 5)
		self.header_id = query_result[0]
		self.header_main_id = query_result[1]
		self.gap = query_result[2]
		self.second_error = query_result[3]
		self.epicenter_latitude_error = query_result[4]
		self.epicenter_longitude_error = query_result[5]
		self.depth_error = query_result[6]
		self.magnitude_error = query_result[7]

	def return_as_string(self):
		output_string = ""
		return output_string


class NordicHeaderWaveform(NordicHeader):
	def __init__(self, query_result):
		NordicHeader.__init__(self, 6)
		self.header_id = query_result[0]
		self.event_id = query_result[1]	
		self.waveform_info = query_result[2]

	def return_as_string(self):
		output_string = ""
		return output_string


def queryNordicEventPhaseData(cur, event_id):
	phase_data = []

	cur.execute("SELECT id, event_id, station_code, sp_instrument_type, sp_component, quality_indicator, phase_type, weight, first_motion, time_info, hour, minute, second, signal_duration, max_amplitude, max_amplitude_period, back_azimuth, apparent_velocity, signal_to_noise, azimuth_residual, travel_time_residual, location_weight, epicenter_distance, epicenter_to_station_azimuth FROM nordic_phase_data WHERE event_id = %s", (event_id,))

	query_answers = cur.fetchall()

	for answer in query_answers:
		phase_data.append(NordicPhaseData(answer))

	return phase_data

def queryNordicEventMainHeaders(cur, event_id):
	headers = []

	cur.execute("SELECT id, event_id, date, hour, minute, second, location_model, distance_indicator, event_desc_id, epicenter_latitude, epicenter_longitude, depth, depth_control, locating_indicator, epicenter_reporting_agency, stations_used, rms_time_residuals, magnitude_1, type_of_magnitude_1, magnitude_reporting_agency_1, magnitude_2, type_of_magnitude_2, magnitude_reporting_agency_2, magnitude_3, type_of_magnitude_3, magnitude_reporting_agency_3 FROM nordic_header_main WHERE event_id = %s", (event_id,))

	query_answers = cur.fetchall()

	for answer in query_answers:
		headers.append(NordicHeaderMain(answer))

	return headers

def queryNordicEventMacroseismicHeaders(cur, event_id):
	headers = []

	cur.execute("SELECT id, event_id, description, diastrophism_code, tsunami_code, seiche_code, cultural_effects, unusual_effects, maximum_observed_intensity, maximum_intensity_qualifier, intensity_scale, macroseismic_latitude, macroseismic_longitude, macroseismic_magnitude, type_of_magnitude, logarithm_of_radius, logarithm_of_area_1, bordering_intensity_1, logarithm_of_area_2, bordering_intensity_2, quality_rank, reporting_agency FROM nordic_header_macroseismic WHERE event_id = %s", (event_id,))

	query_answers = cur.fetchall()

	for answer in query_answers:
		headers.append(NordicHeaderMacroseismic(answer))

	return headers

def queryNordicEventCommentHeaders(cur, event_id):
	headers = []

	cur.execute("SELECT id, event_id, h_comment FROM nordic_header_comment WHERE event_id = %s", (event_id,))

	query_answers = cur.fetchall()

	for answer in query_answers:
		headers.append(NordicHeaderComment(answer))

	return headers

def queryNordicEventErrorHeaders(cur, event_id):
	headers = []

	cur.execute("SELECT nordic_header_error.id, nordic_header_error.header_id, gap, second_error, epicenter_latitude_error, epicenter_longitude_error, depth_error, magnitude_error FROM nordic_header_error INNER JOIN nordic_header_main ON nordic_header_main.id = nordic_header_error.header_id WHERE nordic_header_main.event_id = %s", (event_id,))
	query_answers = cur.fetchall()

	for answer in query_answers:
		headers.append(NordicHeaderError(answer))

	return headers

def queryNordicEventWaveformHeaders(cur, event_id):
	headers = []

	cur.execute("SELECT id, event_id, waveform_info FROM nordic_header_waveform WHERE event_id = %s", (event_id,))

	query_answers = cur.fetchall()

	for answer in query_answers:
		headers.append(NordicHeaderWaveform(answer))

	return headers

def readNordicEvent(cur, event_id):
	headers = {}
	phase_data = []

	headers[1] = queryNordicEventMainHeaders(cur, event_id)
	headers[2] = queryNordicEventMacroseismicHeaders(cur, event_id)
	headers[3] = queryNordicEventCommentHeaders(cur, event_id)
	headers[5] = queryNordicEventErrorHeaders(cur, event_id)
	headers[6] = queryNordicEventWaveformHeaders(cur, event_id)

	phase_data = queryNordicEventPhaseData(cur, event_id)

	nordic_event = NordicEvent(headers, phase_data)

	return nordic_event

def getNordicEvent(event_id, cur):
	nordic = readNordicEvent(cur, event_id)
	return nordic	
