/*
+-------------------------------------+
|NORDIC HEADER WAVEFORM TABLE CREATION|
+-------------------------------------+

This sql file has all the commands for creating a nordic_header_waveform table.
*/

--Create the nordic_header_waveform table
CREATE TABLE nordic_header_waveform(
	id SERIAL PRIMARY KEY,
	event_id INTEGER REFERENCES nordic_event(id) ON DELETE CASCADE,
	waveform_info VARCHAR(78)
);

--Enable row level security
ALTER TABLE nordic_header_waveform ENABLE ROW LEVEL SECURITY;
