CREATE TABLE nordic_header_error (
	id SERIAL PRIMARY KEY,
	header_id INTEGER REFERENCES nordic_header_main(id),
	gap INTEGER,
	second_error FLOAT,
	epicenter_latitude_error FLOAT,
	epicenter_longitude_error FLOAT,
	depth_error FLOAT,
	magnitude_error FLOAT
);
