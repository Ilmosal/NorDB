/*
+-------------------------+
|INSTRUMENT TABLE CREATION|
+-------------------------+

This sql file has all the commands for creating a instrument table.

*/

--Create table command for instrument
CREATE TABLE instrument(
    id SERIAL PRIMARY KEY,
    css_id INTEGER UNIQUE,
    instrument_name VARCHAR(50),
    instrument_type VARCHAR(6),
    band VARCHAR(1),
    digital VARCHAR(1),
    samprate FLOAT,
    ncalib FLOAT,
    ncalper FLOAT,
    dir VARCHAR(64),
    dfile VARCHAR(32),
    response_id INTEGER REFERENCES response(id) ON DELETE CASCADE, 
    rsptype VARCHAR(6),
    lddate DATE
);

--Enable row level security
ALTER TABLE instrument ENABLE ROW LEVEL SECURITY;
