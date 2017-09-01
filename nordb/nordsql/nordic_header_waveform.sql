CREATE TABLE nordic_header_waveform(
	id SERIAL PRIMARY KEY,
	event_id INTEGER REFERENCES nordic_event(id),
	waveform_info VARCHAR(78)
);
