CREATE TABLE nordic_modified(
	id SERIAL PRIMARY KEY,
	event_id INTEGER REFERENCES nordic_event(id),
	replacement_event_id INTEGER REFERENCES nordic_event(id),
	old_event_type VARCHAR(1),
	replaced TIMESTAMP
);
