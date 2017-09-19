import logging
import psycopg2

def checkForSameEvents(nordic_event, cur):
	cmd = "SELECT event_id FROM nordic_header_waveform WHERE waveform_info = %s;"
	data = ""
	for h in nordic_event.headers:
		if h.tpe == 6:
			data = h.waveform_info

	if data != "":
		cur.execute(cmd, (data,))
		ans = cur.fetchall()

		for a in ans:
			cur.execute("SELECT event_type FROM nordic_event WHERE id = %s", (a[0],))
			tpe = cur.fetchone()[0]
			if tpe == nordic_event.event_type:
				return a[0]

	if nordic_event.headers[0].hour == "":
		return -1
	if nordic_event.headers[0].minute == "":
		return -1
	if nordic_event.headers[0].second == "":
		return -1
	
	cmd = "SELECT event_id FROM nordic_header_main WHERE date=%s"
	cmd += "AND hour = %s "
	cmd += "AND minute = %s "
	cmd += "AND second = %s "
	cmd += "AND epicenter_latitude = %s "
	cmd += "AND epicenter_longitude = %s;"

	cur.execute(cmd, (nordic_event.headers[0].date,
					nordic_event.headers[0].hour,
					nordic_event.headers[0].minute,
					nordic_event.headers[0].second,
					nordic_event.headers[0].epicenter_latitude,
					nordic_event.headers[0].epicenter_longitude))

	ans = cur.fetchall()
	for a in ans:
		cur.execute("SELECT event_type FROM nordic_event WHERE id = %s", (a[0],))
		tpe = cur.fetchone()[0]
		if tpe == nordic_event.event_type:
			return a[0]

	return -1

def checkForSimilarEvents(nordic_event, cur): 
	hour_error = 1
	minute_error = 1
	second_error = 10.0
	epicenter_latitude_error = 0.1
	epicenter_longitude_error = 0.1

	if nordic_event.headers[0].hour == "":
		return 0
	if nordic_event.headers[0].minute == "":
		return 0
	if nordic_event.headers[0].second == "":
		return 0
	
	cmd = "SELECT id, event_id FROM nordic_header_main WHERE date = %s "
	cmd += "AND hour - %s < %s "
	cmd += "AND minute - %s < %s "
	cmd += "AND second - %s < %s "
	cmd += "AND epicenter_latitude - %s < %s "
	cmd += "AND epicenter_longitude - %s < %s;"
 
	cur.execute(cmd, (nordic_event.headers[0].date,
					nordic_event.headers[0].hour,
					hour_error,
					nordic_event.headers[0].minute,
					minute_error,
					nordic_event.headers[0].second,
					second_error,
					nordic_event.headers[0].epicenter_latitude,
					epicenter_latitude_error,
					nordic_event.headers[0].epicenter_longitude,
					epicenter_longitude_error))

	ans = cur.fetchone()

	if not ans:
		return 0

	cmd = "SELECT event_type FROM nordic_event WHERE event_id=%s"
	cur.execute(cmd, (ans[1]))
	eType = cur.fetchone()

	if not eType:
		return 0

	if eType[0] == nordic_event.event_type:
		return ans[0]
	else:
		return 0
