/*
+---------------------------+
|NORDIC EVENT TABLE CREATION|
+---------------------------+

This sql file has all the commands for creating a nordic_event table.
*/

--Create nordic_event table
CREATE TABLE nordic_event (
	id SERIAL PRIMARY KEY,
    urn TEXT UNIQUE,
	root_id INTEGER REFERENCES nordic_event_root(id) ON DELETE CASCADE,
    creation_id INTEGER REFERENCES creation_info(id),
	nordic_file_id INTEGER REFERENCES nordic_file(id),
	solution_type VARCHAR(6) REFERENCES solution_type(type_id) ON DELETE CASCADE, 
	author_id VARCHAR(3)
);

--Enable row level security
ALTER TABLE nordic_event ENABLE ROW LEVEL SECURITY;

