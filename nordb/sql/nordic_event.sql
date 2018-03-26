CREATE TABLE solution_type (
    type_id VARCHAR(6) PRIMARY KEY,
    type_desc VARCHAR(32),
    allow_multiple BOOLEAN
);

INSERT INTO solution_type (type_id, type_desc, allow_multiple) VALUES ('O', 'Other', True);
INSERT INTO solution_type (type_id, type_desc, allow_multiple) VALUES ('A', 'Automatic', True);
INSERT INTO solution_type (type_id, type_desc, allow_multiple) VALUES ('F', 'Final', False);

CREATE TABLE nordic_event (
	id SERIAL PRIMARY KEY,
	root_id INTEGER REFERENCES nordic_event_root(id),
    creation_id INTEGER REFERENCES creation_info(id),
	nordic_file_id INTEGER REFERENCES nordic_file(id),
	solution_type VARCHAR(6) REFERENCES solution_type(type_id),
	author_id VARCHAR(3)
);


