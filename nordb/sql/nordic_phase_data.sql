/*
+--------------------------------+
|NORDIC PHASE DATA TABLE CREATION|
+--------------------------------+

This sql file has all the commands for creating a nordic_phase_data table.
*/

--Create the nordic_phase_data table
CREATE TABLE nordic_phase_data(
	id SERIAL PRIMARY KEY,
	event_id INTEGER REFERENCES nordic_event(id) ON DELETE CASCADE,
	station_code VARCHAR(6),
	sp_instrument_type VARCHAR(1),
	sp_component VARCHAR(1),  
	quality_indicator VARCHAR(1),
	phase_type VARCHAR(4),
	weight INTEGER,
	first_motion VARCHAR(1),
    observation_time timestamp,
	signal_duration INTEGER,
	max_amplitude FLOAT,
	max_amplitude_period FLOAT,
	back_azimuth FLOAT,
	apparent_velocity FLOAT,
	signal_to_noise FLOAT,
	azimuth_residual INTEGER,
	travel_time_residual FLOAT,
	location_weight INTEGER, 
	epicenter_distance INTEGER,
	epicenter_to_station_azimuth INTEGER
);

--Enable row level security
ALTER TABLE nordic_phase_data ENABLE ROW LEVEL SECURITY;
