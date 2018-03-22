CREATE TABLE event_type (
    e_type_id VARCHAR(6) PRIMARY KEY,
    e_type_desc VARCHAR(32),
    allow_multiple BOOLEAN
);

INSERT INTO event_type (e_type_id, e_type_desc, allow_multiple) VALUES ('O', 'Other', True);
INSERT INTO event_type (e_type_id, e_type_desc, allow_multiple) VALUES ('A', 'Automatic', True);
INSERT INTO event_type (e_type_id, e_type_desc, allow_multiple) VALUES ('F', 'Final', False);

CREATE TABLE nordic_event (
	id SERIAL PRIMARY KEY,
	root_id INTEGER REFERENCES nordic_event_root(id),
    creation_id INTEGER REFERENCES creation_info(id),
	nordic_file_id INTEGER REFERENCES nordic_file(id),
	event_type VARCHAR(6) REFERENCES event_type(e_type_id),
	author_id VARCHAR(3)
);


