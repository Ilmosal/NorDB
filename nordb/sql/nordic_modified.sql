CREATE TABLE nordic_modified(
	id SERIAL PRIMARY KEY,
	event_id INTEGER REFERENCES nordic_event(id),
	replacement_event_id INTEGER REFERENCES nordic_event(id),
	old_solution_type VARCHAR(6) REFERENCES solution_Type,
	replaced TIMESTAMP
);
