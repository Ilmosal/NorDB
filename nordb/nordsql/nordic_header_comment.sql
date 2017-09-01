CREATE TABLE nordic_header_comment(
	id SERIAL PRIMARY KEY,
	event_id INTEGER REFERENCES nordic_event(id),
	h_comment VARCHAR(78)
);
