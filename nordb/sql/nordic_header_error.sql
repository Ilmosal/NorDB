/*
+----------------------------------+
|NORDIC HEADER ERROR TABLE CREATION|
+----------------------------------+

This sql file has all the commands for creating a nordic_header_error table.
*/

--Create the nordic_header_error table
CREATE TABLE nordic_header_error (
	id SERIAL PRIMARY KEY,
	header_id INTEGER REFERENCES nordic_header_main(id) ON DELETE CASCADE,
	gap INTEGER,
	second_error FLOAT,
	epicenter_latitude_error FLOAT,
	epicenter_longitude_error FLOAT,
	depth_error FLOAT,
	magnitude_error FLOAT
);

--Enable row level security
ALTER TABLE nordic_header_error ENABLE ROW LEVEL SECURITY;
