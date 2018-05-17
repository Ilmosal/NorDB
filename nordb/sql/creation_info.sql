/*
+----------------------------+
|CREATION INFO TABLE CREATION|
+----------------------------+

This file contains the commands for creating the creation info table.
*/

--Create Privacy setting type enum
CREATE TYPE privacy_level as ENUM ('public', 'secure', 'private');

--Create creation_info table
CREATE TABLE creation_info(
    id SERIAL PRIMARY KEY,
    creation_date TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc'),
    owner VARCHAR(32) REFERENCES nordb_user(username) DEFAULT CURRENT_USER,
    privacy_setting PRIVACY_LEVEL DEFAULT 'private',
    creation_comment TEXT DEFAULT NULL
);

--Enable row level security
ALTER TABLE creation_info ENABLE ROW LEVEL SECURITY 
