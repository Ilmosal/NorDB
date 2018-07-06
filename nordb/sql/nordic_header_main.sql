/*
+---------------------------------+
|NORDIC HEADER MAIN TABLE CREATION|
+---------------------------------+

This sql file has all the commands for creating a nordic_header_main table.

*/

--Create nordic_header_main table
CREATE TABLE nordic_header_main (
	id SERIAL PRIMARY KEY,
	event_id SERIAL REFERENCES nordic_event(id) ON DELETE CASCADE,
	origin_time TIME,
    origin_date DATE,
	location_model VARCHAR(1),
	distance_indicator VARCHAR(1),
	event_desc_id VARCHAR(1),
	epicenter_latitude FLOAT,
	epicenter_longitude FLOAT,
	depth FLOAT,
	depth_control VARCHAR(1),
	locating_indicator VARCHAR(1),
	epicenter_reporting_agency VARCHAR(3),
	stations_used INTEGER,
	rms_time_residuals FLOAT,
	magnitude_1 FLOAT,
	type_of_magnitude_1 VARCHAR(1),
	magnitude_reporting_agency_1 VARCHAR(3),
	magnitude_2 FLOAT,
	type_of_magnitude_2 VARCHAR(1),
	magnitude_reporting_agency_2 VARCHAR(3),
	magnitude_3 FLOAT,
	type_of_magnitude_3 VARCHAR(1),
	magnitude_reporting_agency_3 VARCHAR(3)
);

--Enable row level security
ALTER TABLE nordic_header_main ENABLE ROW LEVEL SECURITY;
