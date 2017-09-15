CREATE TABLE nordic_event (
	id SERIAL PRIMARY KEY,
	root_id INTEGER REFERENCES nordic_event_root(id),
	nordic_file_id INTEGER REFERENCES nordic_file(id),
	event_type VARCHAR(1),
	author_id VARCHAR(3)
);
