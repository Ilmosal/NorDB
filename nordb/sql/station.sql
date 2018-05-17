/*
+----------------------+
|STATION TABLE CREATION|
+----------------------+

This sql file has all the commands for creating a station table.

*/

--Create table command for station
CREATE TABLE station(
    id SERIAL PRIMARY KEY,
    network_id INTEGER REFERENCES network(id) ON DELETE CASCADE, 
    station_code VARCHAR(6),
    on_date DATE,
    off_date DATE,
    latitude FLOAT,
    longitude FLOAT,
    elevation FLOAT,
    station_name VARCHAR(50),
    station_type VARCHAR(2),
    reference_station VARCHAR(6),
    north_offset FLOAT,
    east_offset FLOAT,
    load_date DATE
);

--Enable row level security
ALTER TABLE station ENABLE ROW LEVEL SECURITY;
