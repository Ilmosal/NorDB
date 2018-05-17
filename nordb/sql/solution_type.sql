/*
+----------------------------+
|SOLUTION TYPE TABLE CREATION|
+----------------------------+

This file contains the commands for creating the solution type table.
*/

--Create solution type table
CREATE TABLE solution_type (
    type_id VARCHAR(6) PRIMARY KEY,
    creation_id INTEGER REFERENCES creation_info(id),
    type_desc VARCHAR(32),
    allow_multiple BOOLEAN
);

--Insert creation_info object
INSERT INTO creation_info (privacy_setting, creation_comment) VALUES ('public', 'Database creation info');

--Insert default solution types
INSERT INTO solution_type (type_id, creation_id, type_desc, allow_multiple) VALUES ('O', 1, 'Other', True);
INSERT INTO solution_type (type_id, creation_id, type_desc, allow_multiple) VALUES ('A', 1, 'Automatic', True);
INSERT INTO solution_type (type_id, creation_id, type_desc, allow_multiple) VALUES ('F', 1, 'Final', False);

--Enable row level security
ALTER TABLE solution_type ENABLE ROW LEVEL SECURITY;
