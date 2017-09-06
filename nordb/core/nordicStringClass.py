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

