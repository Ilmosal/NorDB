CREATE TYPE E_TYPE AS ENUM('O', 'A', 'R', 'P', 'F', 'S');
CREATE TABLE nordic_event (
	id SERIAL PRIMARY KEY,
	root_id INTEGER REFERENCES nordic_event_root(id),
    creation_id INTEGER REFERENCES creation_info(id),
	nordic_file_id INTEGER REFERENCES nordic_file(id),
	event_type E_TYPE,
	author_id VARCHAR(3)
);
