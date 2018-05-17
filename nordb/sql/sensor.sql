/*
+---------------------+
|SENSOR TABLE CREATION|
+---------------------+

This sql file has all the commands for creating a sensor table.

*/

--Create table command for sensor
CREATE TABLE sensor(
    id SERIAL PRIMARY KEY,
    instrument_id INTEGER REFERENCES instrument(id) ON DELETE CASCADE,
    sitechan_id INTEGER REFERENCES sitechan(id) ON DELETE CASCADE,
    time FLOAT,
    endtime FLOAT,
    jdate DATE,
    calratio FLOAT,
    calper FLOAT,
    tshift FLOAT,
    instant VARCHAR(1),
    lddate DATE
);

--Enable row level security
ALTER TABLE sensor ENABLE ROW LEVEL SECURITY;
