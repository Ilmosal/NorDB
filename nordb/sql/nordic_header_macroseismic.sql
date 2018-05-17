/*
+-----------------------------------------+
|NORDIC HEADER MACROSEISMIC TABLE CREATION|
+-----------------------------------------+

This sql file has all the commands for creating a nordic_header_macroseismic table.
*/

--Create the nordic_header_macroseismic table
CREATE TABLE nordic_header_macroseismic(
	id SERIAL PRIMARY KEY,
	event_id INTEGER REFERENCES nordic_event(id) ON DELETE CASCADE,
	description VARCHAR(15),
	diastrophism_code VARCHAR(1),
	tsunami_code VARCHAR(1),
	seiche_code VARCHAR(1),
	cultural_effects VARCHAR(1),
	unusual_effects VARCHAR(1),
	maximum_observed_intensity INTEGER,
	maximum_intensity_qualifier VARCHAR(1),
	intensity_scale VARCHAR(2),
	macroseismic_latitude FLOAT,
	macroseismic_longitude FLOAT,
	macroseismic_magnitude FLOAT,
	type_of_magnitude VARCHAR(1),
	logarithm_of_radius FLOAT,
	logarithm_of_area_1 FLOAT,
	bordering_intensity_1 INTEGER,
	logarithm_of_area_2 FLOAT,
	bordering_intensity_2 INTEGER,
	quality_rank VARCHAR(1),
	reporting_agency VARCHAR(3)	
);

--Enable row level security
ALTER TABLE nordic_header_macroseismic ENABLE ROW LEVEL SECURITY;
