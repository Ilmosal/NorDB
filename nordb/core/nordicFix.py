def fixMainData(header):
	pass

def fixPhaseData(data):
	if data.epicenter_to_station_azimuth == "360":
		data.epicenter_to_station_azimuth = "0"

	if data.back_azimuth == "360.0":
		data.back_azimuth = "0.0"

	if data.second == "60.00":
		data.second = "0.00"
		if data.minute == "60":
			data.minute = 0
			if data.hour == "23":
				data.hour = "0"
				data.time_info = "+"
			else:
				data.hour = str(int(data.hour) + 1)
		else:
			data.minute = str(int(data.minute) + 1)


def fixNordicEvent(nordicEvent):
	for data in nordicEvent.data:
		fixPhaseData(data)

	return True
