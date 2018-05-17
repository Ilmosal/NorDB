/*
+-----------------------+
|SITECHAN TABLE CREATION|
+-----------------------+

This sql file has all the commands for creating a sitechan table.

*/

--Create table command for sitechan
CREATE TABLE sitechan(
    id SERIAL PRIMARY KEY,
    css_id INTEGER UNIQUE,
    station_id INTEGER REFERENCES station(id) ON DELETE CASCADE,
    channel_code VARCHAR(8),
    on_date DATE,
    off_date DATE,
    channel_type VARCHAR(4),
    emplacement_depth FLOAT,
    horizontal_angle FLOAT,
    vertical_angle FLOAT,
    description VARCHAR(50),
    load_date DATE
);

--Enable row level security
ALTER TABLE sitechan ENABLE ROW LEVEL SECURITY;
